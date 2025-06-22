import json
import pandas as pd
import nltk
nltk.download('punkt')
from rouge_score import rouge_scorer
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from bert_score import score as bert_score_fn

# Dosya yolu
file_path = "999_summaries.json"

# JSON oku
with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Veriyi tabloya aktar
rows = []
for entry in data:
    reference = entry["original_summary"]
    for model_name in ["chatgpt", "llama", "mt5", "mbart"]:
        rows.append({
            "model": model_name,
            "reference": reference,
            "summary": entry["summaries"][model_name]
        })

df = pd.DataFrame(rows)

# ROUGE hesaplayıcı
rouge = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)

# Skor hesapla
def calculate_scores(reference, summary):
    r_scores = rouge.score(reference, summary)
    rouge1 = r_scores["rouge1"].fmeasure
    rouge2 = r_scores["rouge2"].fmeasure
    rougeL = r_scores["rougeL"].fmeasure
    smoothie = SmoothingFunction().method4
    bleu = sentence_bleu([reference.split()], summary.split(), smoothing_function=smoothie)
    return rouge1, rouge2, rougeL, bleu

rouge1s, rouge2s, rougeLs, bleus = [], [], [], []
for _, row in df.iterrows():
    r1, r2, rl, bleu = calculate_scores(row["reference"], row["summary"])
    rouge1s.append(r1)
    rouge2s.append(r2)
    rougeLs.append(rl)
    bleus.append(bleu)

df["rouge1"] = rouge1s
df["rouge2"] = rouge2s
df["rougeL"] = rougeLs
df["bleu"] = bleus

# BERTScore hesapla
P, R, F1 = bert_score_fn(df["summary"].tolist(), df["reference"].tolist(), lang="tr", verbose=True)
df["bertscore_f1"] = F1.tolist()

# Excel ve JSON çıktı
df.to_excel("classic_scores.xlsx", index=False)

results_json = df.to_dict(orient="records")
with open("classic_scores.json", "w", encoding="utf-8") as f:
    json.dump(results_json, f, ensure_ascii=False, indent=2)

print("Skorlar başarıyla hesaplandı ve dosyalar oluşturuldu.")
