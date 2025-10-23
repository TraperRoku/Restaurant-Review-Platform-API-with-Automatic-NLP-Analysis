import torch.optim as optim
import torch
import torch.nn as nn
from torch.optim import AdamW
from torch.utils.data import Dataset, DataLoader
from transformers import (
    AutoTokenizer,
    AutoModel,
    get_linear_schedule_with_warmup
)
#from transformers.optimization import AdamW
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import json
import numpy as np
from tqdm import tqdm
import os
from typing import Dict, List, Tuple
import pandas as pd


# =========================================================================
# 1. KONFIGURACJA
# =========================================================================

class Config:
    # Model
    MODEL_NAME = "allegro/herbert-base-cased"  # Polski BERT
    MAX_LENGTH = 256
    BATCH_SIZE = 16
    LEARNING_RATE = 2e-5
    EPOCHS = 5

    # Aspekty (4 aspekty * 5 klas = 20 neuronów wyjściowych)
    ASPECTS = ["jedzenie", "cena", "obsługa", "atmosfera"]
    NUM_CLASSES_PER_ASPECT = 5  # 1-5 gwiazdek

    # Ścieżki
    DATA_DIR = "./data"
    MODEL_DIR = "./models/bert_absa_restaurant"
    TRAINING_FILE = f"{DATA_DIR}/training_data.json"
    VALIDATION_FILE = f"{DATA_DIR}/validation_data.json"

    # Urządzenie
    DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Early stopping
    PATIENCE = 3
    MIN_DELTA = 0.001


config = Config()


# =========================================================================
# 2. DATASET
# =========================================================================

class RestaurantReviewDataset(Dataset):
    """Dataset dla recenzji restauracji z ocenami ABSA"""

    def __init__(self, data: List[Dict], tokenizer, max_length: int):
        self.data = data
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        item = self.data[idx]
        text = item["text"]

        # Tokenizacja
        encoding = self.tokenizer(
            text,
            max_length=self.max_length,
            padding="max_length",
            truncation=True,
            return_tensors="pt"
        )

        # Labels: [jedzenie, cena, obsługa, atmosfera] (każdy 1-5)
        labels = torch.tensor([
            item["labels"]["jedzenie"] - 1,  # 0-4 (dla CrossEntropyLoss)
            item["labels"]["cena"] - 1,
            item["labels"]["obsługa"] - 1,
            item["labels"]["atmosfera"] - 1
        ], dtype=torch.long)

        return {
            "input_ids": encoding["input_ids"].squeeze(0),
            "attention_mask": encoding["attention_mask"].squeeze(0),
            "labels": labels
        }


# =========================================================================
# 3. MODEL ARCHITEKTURY
# =========================================================================

class BERTABSAModel(nn.Module):
    """
    Model BERT dla ABSA z wieloma głowami klasyfikacyjnymi
    Każdy aspekt ma osobną głowę (4 aspekty × 5 klas)
    """

    def __init__(self, model_name: str, num_aspects: int, num_classes: int):
        super(BERTABSAModel, self).__init__()

        # BERT encoder
        self.bert = AutoModel.from_pretrained(model_name)
        hidden_size = self.bert.config.hidden_size

        # Dropout dla regularyzacji
        self.dropout = nn.Dropout(0.3)

        # Osobna głowa klasyfikacyjna dla każdego aspektu
        self.aspect_classifiers = nn.ModuleList([
            nn.Sequential(
                nn.Linear(hidden_size, 256),
                nn.ReLU(),
                nn.Dropout(0.2),
                nn.Linear(256, num_classes)
            )
            for _ in range(num_aspects)
        ])

    def forward(self, input_ids, attention_mask):
        # BERT encoding
        outputs = self.bert(
            input_ids=input_ids,
            attention_mask=attention_mask
        )

        # Weź [CLS] token (pooled output)
        pooled_output = outputs.pooler_output
        pooled_output = self.dropout(pooled_output)

        # Klasyfikacja dla każdego aspektu
        aspect_logits = []
        for classifier in self.aspect_classifiers:
            logits = classifier(pooled_output)
            aspect_logits.append(logits)

        return aspect_logits


# =========================================================================
# 4. TRENING
# =========================================================================

class ABSATrainer:
    """Klasa do trenowania modelu ABSA"""

    def __init__(self, model, train_loader, val_loader, config):
        self.model = model.to(config.DEVICE)
        self.train_loader = train_loader
        self.val_loader = val_loader
        self.config = config

        # Optimizer i scheduler
        self.optimizer = AdamW(model.parameters(), lr=config.LEARNING_RATE)
        total_steps = len(train_loader) * config.EPOCHS
        self.scheduler = get_linear_schedule_with_warmup(
            self.optimizer,
            num_warmup_steps=total_steps // 10,
            num_training_steps=total_steps
        )

        # Loss function (osobna dla każdego aspektu)
        self.criterion = nn.CrossEntropyLoss()

        # Early stopping
        self.best_val_loss = float('inf')
        self.patience_counter = 0

    def train_epoch(self) -> float:
        """Trenuj jeden epoch"""
        self.model.train()
        total_loss = 0

        progress_bar = tqdm(self.train_loader, desc="Training")
        for batch in progress_bar:
            # Przenieś dane na GPU
            input_ids = batch["input_ids"].to(self.config.DEVICE)
            attention_mask = batch["attention_mask"].to(self.config.DEVICE)
            labels = batch["labels"].to(self.config.DEVICE)  # [batch_size, 4]

            # Forward pass
            self.optimizer.zero_grad()
            aspect_logits = self.model(input_ids, attention_mask)

            # Oblicz loss dla każdego aspektu
            loss = 0
            for i, logits in enumerate(aspect_logits):
                aspect_labels = labels[:, i]
                loss += self.criterion(logits, aspect_labels)

            # Backward pass
            loss.backward()
            torch.nn.utils.clip_grad_norm_(self.model.parameters(), 1.0)
            self.optimizer.step()
            self.scheduler.step()

            total_loss += loss.item()
            progress_bar.set_postfix({"loss": loss.item()})

        return total_loss / len(self.train_loader)

    def validate(self) -> Tuple[float, Dict]:
        """Walidacja modelu"""
        self.model.eval()
        total_loss = 0
        all_predictions = {aspect: [] for aspect in self.config.ASPECTS}
        all_labels = {aspect: [] for aspect in self.config.ASPECTS}

        with torch.no_grad():
            for batch in tqdm(self.val_loader, desc="Validation"):
                input_ids = batch["input_ids"].to(self.config.DEVICE)
                attention_mask = batch["attention_mask"].to(self.config.DEVICE)
                labels = batch["labels"].to(self.config.DEVICE)

                aspect_logits = self.model(input_ids, attention_mask)

                loss = 0
                for i, (logits, aspect) in enumerate(zip(aspect_logits, self.config.ASPECTS)):
                    aspect_labels = labels[:, i]
                    loss += self.criterion(logits, aspect_labels)

                    # Predykcje
                    preds = torch.argmax(logits, dim=1)
                    all_predictions[aspect].extend(preds.cpu().numpy())
                    all_labels[aspect].extend(aspect_labels.cpu().numpy())

                total_loss += loss.item()

        avg_loss = total_loss / len(self.val_loader)

        # Oblicz metryki dla każdego aspektu
        metrics = {}
        for aspect in self.config.ASPECTS:
            preds = np.array(all_predictions[aspect])
            labels = np.array(all_labels[aspect])
            accuracy = (preds == labels).mean()
            metrics[aspect] = {
                "accuracy": accuracy,
                "predictions": preds,
                "labels": labels
            }

        return avg_loss, metrics

    def train(self):
        """Główna pętla treningowa"""
        print(f"🚀 Rozpoczynam trening na {self.config.DEVICE}")
        print(f"📊 Epochs: {self.config.EPOCHS}, Batch size: {self.config.BATCH_SIZE}")
        print("=" * 60)

        for epoch in range(self.config.EPOCHS):
            print(f"\n📅 Epoch {epoch + 1}/{self.config.EPOCHS}")

            # Trening
            train_loss = self.train_epoch()
            print(f"📉 Training Loss: {train_loss:.4f}")

            # Walidacja
            val_loss, metrics = self.validate()
            print(f"📈 Validation Loss: {val_loss:.4f}")

            # Wyświetl metryki dla każdego aspektu
            print("\n🎯 Accuracy per aspect:")
            for aspect, metric in metrics.items():
                print(f"  {aspect}: {metric['accuracy']:.4f}")

            # Early stopping
            if val_loss < self.best_val_loss - self.config.MIN_DELTA:
                self.best_val_loss = val_loss
                self.patience_counter = 0
                self.save_model()
                print("💾 Model saved (best so far)!")
            else:
                self.patience_counter += 1
                print(f"⏳ Patience: {self.patience_counter}/{self.config.PATIENCE}")

                if self.patience_counter >= self.config.PATIENCE:
                    print("🛑 Early stopping triggered!")
                    break

        print("\n✅ Trening zakończony!")

    def save_model(self):
        """Zapisz model"""
        os.makedirs(self.config.MODEL_DIR, exist_ok=True)
        model_file_path = f"{self.config.MODEL_DIR}/model.pth"
        torch.save(self.model.state_dict(), model_file_path)

        # DODANA LINIA: Sprawdzamy pełną ścieżkę
        full_path = os.path.abspath(model_file_path)

        print(f"💾 Model zapisany w {self.config.MODEL_DIR}")
        print(f"   (Lokalizacja pliku: {full_path})")


# =========================================================================
# 5. ŁADOWANIE DANYCH
# =========================================================================

def load_data(file_path: str) -> List[Dict]:
    """Wczytaj dane treningowe z JSON"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def prepare_dataloaders(config) -> Tuple[DataLoader, DataLoader]:
    """Przygotuj DataLoadery"""
    print("📂 Ładowanie danych...")

    # Wczytaj dane
    train_data = load_data(config.TRAINING_FILE)
    val_data = load_data(config.VALIDATION_FILE)

    print(f"📊 Training samples: {len(train_data)}")
    print(f"📊 Validation samples: {len(val_data)}")

    # Tokenizer
    tokenizer = AutoTokenizer.from_pretrained(config.MODEL_NAME)

    # Datasety
    train_dataset = RestaurantReviewDataset(train_data, tokenizer, config.MAX_LENGTH)
    val_dataset = RestaurantReviewDataset(val_data, tokenizer, config.MAX_LENGTH)

    # DataLoadery
    train_loader = DataLoader(
        train_dataset,
        batch_size=config.BATCH_SIZE,
        shuffle=True,
        num_workers=2
    )

    val_loader = DataLoader(
        val_dataset,
        batch_size=config.BATCH_SIZE,
        shuffle=False,
        num_workers=2
    )

    return train_loader, val_loader, tokenizer


# =========================================================================
# 6. GŁÓWNA FUNKCJA
# =========================================================================

def main():
    """Główna funkcja treningowa"""

    # Ustaw seed dla reproducibility
    torch.manual_seed(42)
    np.random.seed(42)

    # Przygotuj dane
    train_loader, val_loader, tokenizer = prepare_dataloaders(config)

    # Zapisz tokenizer
    os.makedirs(config.MODEL_DIR, exist_ok=True)
    tokenizer.save_pretrained(config.MODEL_DIR)

    # Stwórz model
    print(f"\n🤖 Inicjalizacja modelu: {config.MODEL_NAME}")
    model = BERTABSAModel(
        model_name=config.MODEL_NAME,
        num_aspects=len(config.ASPECTS),
        num_classes=config.NUM_CLASSES_PER_ASPECT
    )

    # Informacje o modelu
    total_params = sum(p.numel() for p in model.parameters())
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"📊 Total parameters: {total_params:,}")
    print(f"📊 Trainable parameters: {trainable_params:,}")

    # Trening
    trainer = ABSATrainer(model, train_loader, val_loader, config)
    trainer.train()

    print("\n🎉 Proces treningowy zakończony!")
    print(f"📁 Model zapisany w: {config.MODEL_DIR}")


if __name__ == "__main__":
    main()