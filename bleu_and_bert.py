import json
import pandas as pd
import matplotlib.pyplot as plt

# Dosyayı yükle
with open("classic_scores.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Model bazlı skorları topla
model_scores = {}

for entry in data:
    model = entry.get("model")
    bleu = entry.get("bleu")
    bert = entry.get("bertscore_f1")

    if model not in model_scores:
        model_scores[model] = {"bleu": [], "bertscore": []}

    if bleu is not None:
        model_scores[model]["bleu"].append(bleu)
    if bert is not None:
        model_scores[model]["bertscore"].append(bert)

# Ortalama skorları hesapla
results = []
for model, scores in model_scores.items():
    avg_bleu = sum(scores["bleu"]) / len(scores["bleu"]) if scores["bleu"] else 0
    avg_bert = sum(scores["bertscore"]) / len(scores["bertscore"]) if scores["bertscore"] else 0
    results.append({"model": model, "BLEU": avg_bleu, "BERTScore": avg_bert})

# DataFrame oluştur
df_avg = pd.DataFrame(results)
from tabulate import tabulate

# Ortalama skorları yazdır
print("\nModel Based Average Scores:\n")
print(tabulate(df_avg, headers="keys", tablefmt="fancy_grid", showindex=False))

import matplotlib.pyplot as plt

# Sadece BLEU için çizgi grafik
plt.figure(figsize=(8, 5))
plt.plot(df_avg["model"], df_avg["BLEU"], marker='o', color='#FF5733', label="BLEU")
plt.title("Model Based BLEU Scores")
plt.xlabel("Model")
plt.ylabel("BLEU")
plt.ylim(0, 1)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

# Sadece BERTScore için çizgi grafik
plt.figure(figsize=(8, 5))
plt.plot(df_avg["model"], df_avg["BERTScore"], marker='o', color='purple', label="BERTScore")
plt.title("Model Based BERTScores ")
plt.xlabel("Model")
plt.ylabel("BERTScore")
plt.ylim(0, 1)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
