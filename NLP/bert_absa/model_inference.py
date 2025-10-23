from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import torch
import torch.nn as nn
from transformers import AutoTokenizer, AutoModel
from typing import Dict, List
import os


# =========================================================================
# 1. KONFIGURACJA
# =========================================================================

class Config:
    MODEL_DIR = "./models/bert_absa_restaurant"
    MODEL_NAME = "allegro/herbert-base-cased"
    MAX_LENGTH = 256
    ASPECTS = ["jedzenie", "cena", "obsługa", "atmosfera"]
    NUM_CLASSES_PER_ASPECT = 5
    DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


config = Config()


# =========================================================================
# 2. MODEL - PROSTA ARCHITEKTURA (zgodna z Colabem!)
# =========================================================================

class BERTABSAModel(nn.Module):
    """Model BERT dla ABSA - PROSTA ARCHITEKTURA (768 -> 256 -> 5)"""

    def __init__(self, model_name: str, num_aspects: int, num_classes: int):
        super(BERTABSAModel, self).__init__()
        self.bert = AutoModel.from_pretrained(model_name)
        hidden_size = self.bert.config.hidden_size
        self.dropout = nn.Dropout(0.2)

        # ✅ PROSTA ARCHITEKTURA - zgodna z train_model_colab.py
        # 768 -> 256 -> 5
        self.aspect_classifiers = nn.ModuleList([
            nn.Sequential(
                nn.Linear(hidden_size, 256),  # 768 -> 256
                nn.ReLU(),
                nn.Dropout(0.2),
                nn.Linear(256, num_classes)    # 256 -> 5
            )
            for _ in range(num_aspects)
        ])

    def forward(self, input_ids, attention_mask):
        outputs = self.bert(input_ids=input_ids, attention_mask=attention_mask)
        pooled_output = outputs.pooler_output
        pooled_output = self.dropout(pooled_output)

        aspect_logits = []
        for classifier in self.aspect_classifiers:
            logits = classifier(pooled_output)
            aspect_logits.append(logits)

        return aspect_logits


# =========================================================================
# 3. ŁADOWANIE MODELU
# =========================================================================

def load_trained_model():
    """Wczytaj wytrenowany model"""
    print("🔄 Ładowanie modelu...")

    # Check if model exists
    model_path = f"{config.MODEL_DIR}/model.pth"
    if not os.path.exists(model_path):
        raise FileNotFoundError(
            f"❌ Model nie znaleziony w {model_path}!\n"
            f"Najpierw wytrenuj model używając train_model_colab.py"
        )

    # Load tokenizer
    tokenizer = AutoTokenizer.from_pretrained(config.MODEL_DIR)

    # Load model
    model = BERTABSAModel(
        model_name=config.MODEL_NAME,
        num_aspects=len(config.ASPECTS),
        num_classes=config.NUM_CLASSES_PER_ASPECT
    )

    # Load weights
    model.load_state_dict(torch.load(model_path, map_location=config.DEVICE))
    model.to(config.DEVICE)
    model.eval()

    print(f"✅ Model wczytany z {config.MODEL_DIR}")
    print(f"🖥️  Urządzenie: {config.DEVICE}")

    return model, tokenizer


# Wczytaj model przy starcie aplikacji
try:
    model, tokenizer = load_trained_model()
    MODEL_LOADED = True
    print("✅ Model gotowy do użycia!")
except Exception as e:
    print(f"⚠️  Nie udało się wczytać modelu: {e}")
    print("⚠️  API będzie działać w trybie demonstracyjnym")
    MODEL_LOADED = False
    model, tokenizer = None, None

# =========================================================================
# 4. FASTAPI
# =========================================================================

app = FastAPI(
    title="BERT ABSA Restaurant Review API",
    description="Zaawansowana analiza sentymentu recenzji restauracji z użyciem BERT",
    version="2.1.0 - BERT Production (Simple Architecture - Fixed)"
)


class ReviewRequest(BaseModel):
    text: str


class AspectScore(BaseModel):
    score: int
    confidence: float


class AnalysisResponse(BaseModel):
    food_score: int
    price_score: int
    service_score: int
    atmosphere_score: int
    overall_sentiment_label: str
    confidence_scores: Dict[str, float]
    model_type: str


# =========================================================================
# 5. FUNKCJE INFERENCE
# =========================================================================

def predict_sentiment(text: str) -> Dict:
    """Predykcja sentymentu dla tekstu"""

    if not MODEL_LOADED:
        # Fallback - zwróć neutralne wartości
        return {
            "scores": [3, 3, 3, 3],
            "confidences": [0.0, 0.0, 0.0, 0.0],
            "model_type": "fallback"
        }

    # Tokenizacja
    encoding = tokenizer(
        text,
        max_length=config.MAX_LENGTH,
        padding="max_length",
        truncation=True,
        return_tensors="pt"
    )

    input_ids = encoding["input_ids"].to(config.DEVICE)
    attention_mask = encoding["attention_mask"].to(config.DEVICE)

    # Predykcja
    with torch.no_grad():
        aspect_logits = model(input_ids, attention_mask)

    # Konwersja logitów na oceny (1-5) i confidence
    scores = []
    confidences = []

    for logits in aspect_logits:
        probs = torch.softmax(logits, dim=1)
        pred_class = torch.argmax(probs, dim=1).item()
        confidence = probs[0, pred_class].item()

        scores.append(pred_class + 1)  # 0-4 -> 1-5
        confidences.append(confidence)

    return {
        "scores": scores,
        "confidences": confidences,
        "model_type": "bert"
    }


def get_overall_sentiment(scores: List[int]) -> str:
    """Oblicz ogólny sentyment na podstawie ocen"""
    avg_score = sum(scores) / len(scores)

    if avg_score >= 4.0:
        return "Bardzo Pozytywny"
    elif avg_score >= 3.5:
        return "Pozytywny"
    elif avg_score >= 2.5:
        return "Neutralny"
    elif avg_score >= 2.0:
        return "Negatywny"
    else:
        return "Bardzo Negatywny"


# =========================================================================
# 6. ENDPOINTY
# =========================================================================

@app.get("/")
def root():
    """Status API"""
    return {
        "message": "BERT ABSA Restaurant Review API",
        "version": "2.1.0 (Simple Architecture - Fixed)",
        "model_loaded": MODEL_LOADED,
        "model_type": "allegro/herbert-base-cased (Polish BERT)",
        "aspects": config.ASPECTS,
        "device": str(config.DEVICE)
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": MODEL_LOADED,
        "device": str(config.DEVICE)
    }


@app.post("/analyze", response_model=AnalysisResponse)
def analyze_review(request: ReviewRequest):
    """
    Analizuje sentyment recenzji restauracji używając BERT.

    Zwraca oceny 1-5 dla każdego aspektu:
    - jedzenie (food_score)
    - cena (price_score)
    - obsługa (service_score)
    - atmosfera (atmosphere_score)
    """

    if not request.text or len(request.text.strip()) == 0:
        raise HTTPException(status_code=400, detail="Tekst recenzji nie może być pusty")

    # Predykcja
    result = predict_sentiment(request.text)

    scores = result["scores"]
    confidences = result["confidences"]

    # Mapowanie scores na aspekty
    aspect_scores = {
        config.ASPECTS[i]: scores[i]
        for i in range(len(config.ASPECTS))
    }

    confidence_dict = {
        config.ASPECTS[i]: round(confidences[i], 4)
        for i in range(len(config.ASPECTS))
    }

    # Ogólny sentyment
    overall_label = get_overall_sentiment(scores)

    return AnalysisResponse(
        food_score=aspect_scores["jedzenie"],
        price_score=aspect_scores["cena"],
        service_score=aspect_scores["obsługa"],
        atmosphere_score=aspect_scores["atmosfera"],
        overall_sentiment_label=overall_label,
        confidence_scores=confidence_dict,
        model_type=result["model_type"]
    )


@app.post("/batch_analyze")
def batch_analyze(reviews: List[ReviewRequest]):
    """Analizuj wiele recenzji jednocześnie"""

    if len(reviews) > 100:
        raise HTTPException(
            status_code=400,
            detail="Maksymalnie 100 recenzji na raz"
        )

    results = []
    for review in reviews:
        result = analyze_review(review)
        results.append(result)

    return {
        "count": len(results),
        "results": results
    }


@app.get("/model_info")
def model_info():
    """Informacje o modelu"""
    if not MODEL_LOADED:
        return {
            "error": "Model nie został wczytany",
            "status": "not_loaded"
        }

    total_params = sum(p.numel() for p in model.parameters())
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)

    return {
        "model_name": config.MODEL_NAME,
        "model_path": config.MODEL_DIR,
        "architecture": "768 -> 256 -> 5 (simple)",
        "total_parameters": f"{total_params:,}",
        "trainable_parameters": f"{trainable_params:,}",
        "aspects": config.ASPECTS,
        "num_classes": config.NUM_CLASSES_PER_ASPECT,
        "max_length": config.MAX_LENGTH,
        "device": str(config.DEVICE)
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)