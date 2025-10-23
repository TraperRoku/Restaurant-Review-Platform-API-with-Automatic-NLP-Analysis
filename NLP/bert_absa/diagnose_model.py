

import torch
import json
from model_inference import predict_sentiment, config
from typing import List, Dict
import numpy as np
from colorama import init, Fore, Style

# Inicjalizacja kolorów
init(autoreset=True)


# =========================================================================
# PRZYPADKI TESTOWE
# =========================================================================

TEST_CASES = [
    # === POZYTYWNE ===
    {
        "text": "Jedzenie było absolutnie wyśmienite",
        "expected": {"jedzenie": 5, "cena": 3, "obsługa": 3, "atmosfera": 3},
        "category": "Pozytywne - jedzenie"
    },
    {
        "text": "Pizza pyszna, obsługa świetna, tanio i klimatycznie",
        "expected": {"jedzenie": 5, "cena": 5, "obsługa": 5, "atmosfera": 5},
        "category": "Pozytywne - wszystko"
    },
    {
        "text": "Super burger, kelnerzy pomocni, ładne wnętrze",
        "expected": {"jedzenie": 5, "cena": 3, "obsługa": 5, "atmosfera": 4},
        "category": "Pozytywne - mix"
    },

    # === NEGATYWNE ===
    {
        "text": "Jedzenie okropne i zimne",
        "expected": {"jedzenie": 1, "cena": 3, "obsługa": 3, "atmosfera": 3},
        "category": "Negatywne - jedzenie"
    },
    {
        "text": "Wszystko fatalne - jedzenie niesmaczne, obsługa niegrzeczna, drogo i brudno",
        "expected": {"jedzenie": 1, "cena": 1, "obsługa": 1, "atmosfera": 1},
        "category": "Negatywne - wszystko"
    },
    {
        "text": "Pizza zimna, kelnerzy aroganccy, ceny kosmiczne",
        "expected": {"jedzenie": 1, "cena": 1, "obsługa": 1, "atmosfera": 3},
        "category": "Negatywne - mix"
    },

    # === MIESZANE (TRUDNE!) ===
    {
        "text": "Jedzenie pyszne, ale obsługa fatalna",
        "expected": {"jedzenie": 5, "cena": 3, "obsługa": 1, "atmosfera": 3},
        "category": "Mieszane - pozytyw + negatyw"
    },
    {
        "text": "Super kuchnia, ale ceny absurdalnie wysokie",
        "expected": {"jedzenie": 5, "cena": 1, "obsługa": 3, "atmosfera": 3},
        "category": "Mieszane - dobra jakość, zła cena"
    },
    {
        "text": "Tanio i smacznie, ale czekaliśmy godzinę",
        "expected": {"jedzenie": 4, "cena": 5, "obsługa": 1, "atmosfera": 3},
        "category": "Mieszane - dobra cena, zła obsługa"
    },
    {
        "text": "Piękne wnętrze i miła obsługa, ale jedzenie mdłe",
        "expected": {"jedzenie": 2, "cena": 3, "obsługa": 4, "atmosfera": 5},
        "category": "Mieszane - zła jakość, dobra reszta"
    },

    # === NEUTRALNE ===
    {
        "text": "Przeciętnie, nic specjalnego",
        "expected": {"jedzenie": 3, "cena": 3, "obsługa": 3, "atmosfera": 3},
        "category": "Neutralne"
    },
    {
        "text": "Normalnie, ani dobrze ani źle",
        "expected": {"jedzenie": 3, "cena": 3, "obsługa": 3, "atmosfera": 3},
        "category": "Neutralne"
    },

    # === ASPEKT: CENA ===
    {
        "text": "Ceny bardzo przystępne i rozsądne",
        "expected": {"jedzenie": 3, "cena": 5, "obsługa": 3, "atmosfera": 3},
        "category": "Cena - tanie"
    },
    {
        "text": "Ceny drapiężne i wygórowane",
        "expected": {"jedzenie": 3, "cena": 1, "obsługa": 3, "atmosfera": 3},
        "category": "Cena - drogie"
    },

    # === ASPEKT: OBSŁUGA ===
    {
        "text": "Kelnerzy super profesjonalni i pomocni",
        "expected": {"jedzenie": 3, "cena": 3, "obsługa": 5, "atmosfera": 3},
        "category": "Obsługa - dobra"
    },
    {
        "text": "Czekaliśmy 40 minut, obsługa beznadziejna",
        "expected": {"jedzenie": 3, "cena": 3, "obsługa": 1, "atmosfera": 3},
        "category": "Obsługa - zła"
    },

    # === ASPEKT: ATMOSFERA ===
    {
        "text": "Piękne wnętrze, eleganckie i stylowe",
        "expected": {"jedzenie": 3, "cena": 3, "obsługa": 3, "atmosfera": 5},
        "category": "Atmosfera - dobra"
    },
    {
        "text": "Hałaśliwie, brudno i ciasno",
        "expected": {"jedzenie": 3, "cena": 3, "obsługa": 3, "atmosfera": 1},
        "category": "Atmosfera - zła"
    },

    # === EDGE CASES ===
    {
        "text": "Najlepsza pizza w życiu! Absolutnie rewelacyjna!",
        "expected": {"jedzenie": 5, "cena": 3, "obsługa": 3, "atmosfera": 3},
        "category": "Edge - superlatywy"
    },
    {
        "text": "Tragedia, najgorsza restauracja ever",
        "expected": {"jedzenie": 1, "cena": 1, "obsługa": 1, "atmosfera": 1},
        "category": "Edge - skrajnie negatywne"
    },
]


# =========================================================================
# FUNKCJE TESTOWE
# =========================================================================

def get_color_for_score(score: int) -> str:
    """Zwróć kolor dla oceny"""
    if score >= 4:
        return Fore.GREEN
    elif score >= 3:
        return Fore.YELLOW
    else:
        return Fore.RED


def get_emoji_for_score(score: int) -> str:
    """Zwróć emoji dla oceny"""
    emojis = {1: "😡", 2: "😞", 3: "😐", 4: "🙂", 5: "😍"}
    return emojis.get(score, "❓")


def calculate_accuracy(predicted: int, expected: int, tolerance: int = 1) -> bool:
    """Sprawdź czy predykcja jest poprawna (z tolerancją)"""
    return abs(predicted - expected) <= tolerance


def test_single_case(case: Dict) -> Dict:
    """Testuj pojedynczy przypadek"""
    text = case["text"]
    expected = case["expected"]

    # Predykcja
    result = predict_sentiment(text)
    scores = result["scores"]
    confidences = result["confidences"]

    # Mapowanie
    predictions = {
        config.ASPECTS[i]: scores[i]
        for i in range(len(config.ASPECTS))
    }

    confidence_dict = {
        config.ASPECTS[i]: confidences[i]
        for i in range(len(config.ASPECTS))
    }

    # Sprawdź accuracy
    results = {}
    all_correct = True

    for aspect in config.ASPECTS:
        pred = predictions[aspect]
        exp = expected[aspect]
        correct = calculate_accuracy(pred, exp, tolerance=1)

        results[aspect] = {
            "predicted": pred,
            "expected": exp,
            "correct": correct,
            "confidence": confidence_dict[aspect]
        }

        if not correct:
            all_correct = False

    return {
        "text": text,
        "category": case["category"],
        "results": results,
        "all_correct": all_correct,
        "avg_confidence": np.mean(list(confidence_dict.values()))
    }


def print_test_result(test_result: Dict):
    """Wyświetl wynik testu"""
    text = test_result["text"]
    category = test_result["category"]
    results = test_result["results"]
    all_correct = test_result["all_correct"]
    avg_conf = test_result["avg_confidence"]

    # Status
    status = f"{Fore.GREEN}✓ PASS" if all_correct else f"{Fore.RED}✗ FAIL"

    print(f"\n{status}{Style.RESET_ALL}")
    print(f"Kategoria: {Fore.CYAN}{category}{Style.RESET_ALL}")
    print(f"Tekst: \"{text}\"")
    print(f"Avg Confidence: {avg_conf:.2%}")

    # Szczegóły per aspekt
    print("\nWyniki:")
    for aspect, data in results.items():
        pred = data["predicted"]
        exp = data["expected"]
        conf = data["confidence"]
        correct = data["correct"]

        color = Fore.GREEN if correct else Fore.RED
        check = "✓" if correct else "✗"
        emoji_pred = get_emoji_for_score(pred)
        emoji_exp = get_emoji_for_score(exp)

        print(f"  {color}{check}{Style.RESET_ALL} {aspect:12s}: "
              f"pred={emoji_pred} {pred} | exp={emoji_exp} {exp} | "
              f"conf={conf:.2%}")


def run_all_tests():
    """Uruchom wszystkie testy"""
    print("=" * 80)
    print(f"{Fore.CYAN}🧪 SZCZEGÓŁOWE TESTY MODELU BERT ABSA{Style.RESET_ALL}")
    print("=" * 80)

    all_results = []
    categories_stats = {}

    # Uruchom testy
    for i, case in enumerate(TEST_CASES, 1):
        print(f"\n{Fore.YELLOW}{'─'*80}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Test {i}/{len(TEST_CASES)}{Style.RESET_ALL}")

        result = test_single_case(case)
        print_test_result(result)

        all_results.append(result)

        # Statystyki per kategoria
        category = result["category"].split(" - ")[0]
        if category not in categories_stats:
            categories_stats[category] = {"pass": 0, "total": 0}

        categories_stats[category]["total"] += 1
        if result["all_correct"]:
            categories_stats[category]["pass"] += 1

    # PODSUMOWANIE
    print(f"\n\n{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}📊 PODSUMOWANIE WYNIKÓW{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}")

    # Ogólne statystyki
    total_tests = len(all_results)
    passed_tests = sum(1 for r in all_results if r["all_correct"])
    overall_accuracy = passed_tests / total_tests

    avg_confidence = np.mean([r["avg_confidence"] for r in all_results])

    print(f"\n📈 Ogólne statystyki:")
    print(f"   Testy: {passed_tests}/{total_tests} ({overall_accuracy:.1%})")
    print(f"   Średnia pewność: {avg_confidence:.1%}")

    # Per kategoria
    print(f"\n📋 Statystyki per kategoria:")
    for category, stats in sorted(categories_stats.items()):
        pass_rate = stats["pass"] / stats["total"]
        color = Fore.GREEN if pass_rate >= 0.7 else Fore.YELLOW if pass_rate >= 0.5 else Fore.RED
        print(f"   {color}{category:20s}: {stats['pass']}/{stats['total']} ({pass_rate:.1%}){Style.RESET_ALL}")

    # Per aspekt
    print(f"\n🎯 Accuracy per aspekt:")
    aspect_accuracy = {aspect: [] for aspect in config.ASPECTS}

    for result in all_results:
        for aspect, data in result["results"].items():
            aspect_accuracy[aspect].append(1 if data["correct"] else 0)

    for aspect in config.ASPECTS:
        acc = np.mean(aspect_accuracy[aspect])
        color = Fore.GREEN if acc >= 0.7 else Fore.YELLOW if acc >= 0.5 else Fore.RED
        print(f"   {color}{aspect:12s}: {acc:.1%}{Style.RESET_ALL}")

    # Rekomendacje
    print(f"\n💡 Rekomendacje:")
    if overall_accuracy >= 0.75:
        print(f"   {Fore.GREEN}✅ Model działa ŚWIETNIE! Gotowy do produkcji.{Style.RESET_ALL}")
    elif overall_accuracy >= 0.60:
        print(f"   {Fore.YELLOW}🟡 Model działa DOBRZE. Można użyć, ale są przestrzenie do poprawy.{Style.RESET_ALL}")
    else:
        print(f"   {Fore.RED}❌ Model wymaga więcej treningu lub lepszych danych.{Style.RESET_ALL}")

    if avg_confidence < 0.5:
        print(f"   {Fore.YELLOW}⚠️  Niska pewność modelu - rozważ więcej epok treningowych.{Style.RESET_ALL}")

    print(f"\n{Fore.CYAN}{'='*80}{Style.RESET_ALL}")

    return all_results, overall_accuracy


# =========================================================================
# MAIN
# =========================================================================

if __name__ == "__main__":
    try:
        results, accuracy = run_all_tests()

        # Zapisz wyniki
        output_file = "./test_results.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                "overall_accuracy": accuracy,
                "total_tests": len(results),
                "passed_tests": sum(1 for r in results if r["all_correct"]),
                "results": [
                    {
                        "text": r["text"],
                        "category": r["category"],
                        "correct": r["all_correct"],
                        "confidence": r["avg_confidence"]
                    }
                    for r in results
                ]
            }, f, ensure_ascii=False, indent=2)

        print(f"\n💾 Wyniki zapisane w {output_file}")

    except Exception as e:
        print(f"\n{Fore.RED}❌ BŁĄD: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()