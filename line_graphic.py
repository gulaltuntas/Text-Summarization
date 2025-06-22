import json
import pandas as pd
import matplotlib.pyplot as plt

# Dosya ve model eşleşmeleri
file_model_pairs = [
    ("mt5_evaluated_modern.json", "mt5"),
    ("mbart_evaluated_modern.json", "mbart"),
    ("lama_evaluated_modern.json", "lama"),
    ("chat_gpt4_evaluated_modern.json", "gpt4"),
    ("original_summary_modern.json", "original")
]

all_data = []

for file_path, model_name in file_model_pairs:
    with open(file_path, "r", encoding="utf-8") as f:
        model_data = json.load(f)
    for entry in model_data:
        if isinstance(entry, dict):
            scores = entry.get("scores", {})
            if scores and all(isinstance(v, (int, float)) for v in scores.values() if v is not None):
                scores["model"] = model_name
                all_data.append(scores)
        elif isinstance(entry, list):
            for subentry in entry:
                if isinstance(subentry, dict):
                    scores = subentry.get("scores", {})
                    if scores and all(isinstance(v, (int, float)) for v in scores.values() if v is not None):
                        scores["model"] = model_name
                        all_data.append(scores)

# DataFrame ve metrikler
df = pd.DataFrame(all_data)
score_columns = ["relevance", "coherence", "consistency", "fluency", "conciseness", "quotation_score", "overall_score"]
grouped_scores = df.groupby("model")[score_columns].mean().reset_index()
grouped_scores.set_index("model", inplace=True)

# 👇 Bu satırı ekle
custom_order = ["original", "mbart", "mt5", "gpt4", "lama"]
grouped_scores = grouped_scores.loc[custom_order]
from scipy.interpolate import make_interp_spline
import numpy as np

plt.figure(figsize=(12, 6))
x_labels = grouped_scores.index.tolist()
x = np.arange(len(x_labels))

for metric in score_columns:
    y = grouped_scores[metric].values
    if len(x) >= 4:  # Spline için yeterli nokta gerekebilir
        spline = make_interp_spline(x, y, k=3)
        x_smooth = np.linspace(x.min(), x.max(), 300)
        y_smooth = spline(x_smooth)
        plt.plot(x_smooth, y_smooth, label=metric)
    else:
        plt.plot(x, y, marker='o', label=metric)


plt.xticks(x, x_labels)
plt.title("Model Scores Based On Semantic Evaluation Criterias")
plt.xlabel("Model")
plt.ylabel("Average Score")
plt.legend(title="Metrics", bbox_to_anchor=(1.05, 1), loc="upper left")
plt.grid(True)
plt.tight_layout()
plt.show()
