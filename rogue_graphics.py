import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline

# 1. Dosya adları ve hangi modele ait oldukları
file_model_pairs = [
    ("mt5_rouge_skorlu.xlsx", "mt5"),
    ("mbart_rouge_skorlu.xlsx", "mbart"),
    ("llama_rouge_skorlu.xlsx", "lama"),
    ("chat_gpt4o_rouge_skorlu.xlsx", "gpt4")
]

# 2. Dosyaları oku ve model isimlerini ekle
rouge_data = []
for file_path, model_name in file_model_pairs:
    df = pd.read_excel(file_path)
    df["model"] = model_name
    rouge_data.append(df)

# 3. Tüm verileri birleştir
combined_df = pd.concat(rouge_data, ignore_index=True)

# 4. Model bazlı ortalama ROUGE skorları
score_columns = ["rouge_1", "rouge_2", "rouge_L"]
grouped = combined_df.groupby("model")[score_columns].mean().reset_index()
grouped.set_index("model", inplace=True)

# 5. Özel model sırası (görsellik için isteğe bağlı)
custom_order = ["mbart", "mt5", "gpt4", "lama"]
grouped = grouped.loc[custom_order]

# 6. Spline ile yumuşatılmış grafik
plt.figure(figsize=(10, 6))
x_labels = grouped.index.tolist()
x = np.arange(len(x_labels))

for metric in score_columns:
    y = grouped[metric].values
    if len(x) >= 4:
        spline = make_interp_spline(x, y, k=3)
        x_smooth = np.linspace(x.min(), x.max(), 300)
        y_smooth = np.clip(spline(x_smooth), 0, 1)  # ROUGE skorları 0-1 aralığında
        plt.plot(x_smooth, y_smooth, label=metric)
    else:
        plt.plot(x, y, marker='o', label=metric)

plt.xticks(x, x_labels)
plt.ylim(0, 1)
plt.title("Model Based ROGUE Scores")
plt.xlabel("Model")
plt.ylabel("Average Rogue Score")
plt.grid(True)
plt.legend(title="Metrics", bbox_to_anchor=(1.05, 1), loc="upper left")
plt.tight_layout()
plt.show()
