import json

with open("mt5_evaluated_modern.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Tüm entry'ler aslında data[0] içinde
entries = data[0]

relevance_scores = []

for entry in entries:
    scores = entry.get("scores", [])
    for score_item in scores:
        if isinstance(score_item, dict):
            if score_item.get("metric") == "Relevance":
                score_value = score_item.get("score")
                if isinstance(score_value, (int, float)):
                    relevance_scores.append(score_value)

# Sonuç
if relevance_scores:
    ortalama = sum(relevance_scores) / len(relevance_scores)
    print(f"Relevance skorlarının ortalaması: {ortalama:.2f}")
else:
    print("Relevance skoru bulunamadı.")
