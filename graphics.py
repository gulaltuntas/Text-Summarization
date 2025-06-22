import json
import pandas as pd
import matplotlib.pyplot as plt

file_model_pairs = [
    ("original_summary_modern.json", "original"),
    ("mt5_evaluated_modern.json", "mt5"),
    ("mbart_evaluated_modern.json", "mbart"),
    ("lama_evaluated_modern.json", "lama"),
    ("chat_gpt4_evaluated_modern.json", "gpt4")    
]

all_data = []

for file_path, model_name in file_model_pairs:
    with open(file_path, "r", encoding="utf-8") as f:
        model_data = json.load(f)
    
    # Düz liste mi? Liste içinde liste mi?
    for entry in model_data:
        # Eğer entry doğrudan dict ise
        if isinstance(entry, dict):
            scores = entry.get("scores", {})
            if scores and all(isinstance(v, (int, float)) for v in scores.values() if v is not None):
                scores["model"] = model_name
                all_data.append(scores)

        # Eğer entry liste ise (örneğin [[{...}], [{...}]])
        elif isinstance(entry, list):
            for subentry in entry:
                if isinstance(subentry, dict):
                    scores = subentry.get("scores", {})
                    if scores and all(isinstance(v, (int, float)) for v in scores.values() if v is not None):
                        scores["model"] = model_name
                        all_data.append(scores)

df = pd.DataFrame(all_data)

score_columns = ["relevance", "coherence", "consistency", "fluency", "conciseness", "quotation_score", "overall_score"]
grouped_scores = df.groupby("model")[score_columns].mean().reset_index()
# İstenilen sıralama
model_order = ["original", "gpt4", "lama", "mt5", "mbart"]

# Mevcut kodun devamı...
grouped_scores = df.groupby("model")[score_columns].mean().reset_index()
# Tüm skorları 0–100 aralığına ölçekle (her skoru 20 ile çarp)

# Model sırasını belirle
grouped_scores["model"] = pd.Categorical(grouped_scores["model"], categories=model_order, ordered=True)

# Yeniden sıralayıp index'i ayarla
grouped_scores = grouped_scores.sort_values("model").set_index("model")

# Grafik çizimi
grouped_scores.plot(kind="bar", figsize=(12, 6))
plt.title("Model Based Modern Metrics Average Scores Comparasion")
plt.ylabel("Average Scores")
plt.xlabel("Model")
plt.xticks(rotation=0)
plt.legend(title="Metrics", bbox_to_anchor=(1.05, 1), loc="upper left")
plt.tight_layout()
plt.show()
