import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap

# 📥 JSON dosyaları ve model adları
file_model_pairs = [
    ("original_summary_modern.json", "original"),
    ("chat_gpt4_evaluated_modern.json", "gpt4"),
    ("lama_evaluated_modern.json", "lama"),
    ("mt5_evaluated_modern.json", "mt5"),
    ("mbart_evaluated_modern.json", "mbart")
]

all_data = []

# 🔄 Tüm dosyaları oku ve skorları topla
for file_path, model_name in file_model_pairs:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            model_data = json.load(f)
    except Exception as e:
        print(f"❌ {model_name} dosyası okunamadı: {e}")
        continue

    for entry in model_data:
        if isinstance(entry, dict):
            scores = entry.get("scores", {})
            if scores and all(isinstance(v, (int, float)) for v in scores.values() if v is not None):
                scores["model"] = model_name
                all_data.append(scores)
        elif isinstance(entry, list):  # bazı dosyalarda liste olabilir
            for subentry in entry:
                if isinstance(subentry, dict):
                    scores = subentry.get("scores", {})
                    if scores and all(isinstance(v, (int, float)) for v in scores.values() if v is not None):
                        scores["model"] = model_name
                        all_data.append(scores)

# 📊 DataFrame'e dönüştür
df = pd.DataFrame(all_data)

# 📌 Ortalama skorları hesapla
score_columns = ["relevance", "coherence", "consistency", "fluency",
                 "conciseness", "quotation_score", "overall_score"]
grouped_scores = df.groupby("model")[score_columns].mean().reset_index()

# 🔢 Model sırasını sabitle
model_order = ["original", "gpt4", "lama", "mt5", "mbart"]
grouped_scores["model"] = pd.Categorical(grouped_scores["model"],
                                         categories=model_order,
                                         ordered=True)
grouped_scores = grouped_scores.sort_values("model")

# 🎨 Renk skalası: beyaz → pembe → koyu kırmızı (yüksek skora kırmızı ver)
custom_cmap = LinearSegmentedColormap.from_list(
    "custom_white_pink_red", ["white", "#ffc0cb", "#8b0000"]
)

# 🔥 Heatmap çizimi
plt.figure(figsize=(12, 6))
sns.heatmap(grouped_scores.set_index("model").round(2),
            annot=True, fmt=".2f", cmap=custom_cmap,
            linewidths=0.5, cbar=True)

plt.title("Model Based Average Scores", fontsize=14)
plt.yticks(rotation=0)
plt.tight_layout()
plt.show()
