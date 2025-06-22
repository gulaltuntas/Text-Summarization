import json
from tqdm import tqdm
import evaluate
from bert_score import score as bert_score_fn

# Gerekli metrik yükleyicileri
bleu = evaluate.load("bleu")

# Giriş ve çıkış dosya adları
input_path = "rogue_scor_for_all.json"  # burada senin verdiğin JSON dosyası olacak
output_path = "full_scores_bleu_bertscore.json"

# JSON verisini yükle
with open(input_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Tüm makaleler ve modeller için işlem yap
for entry in tqdm(data, desc="Skorlar hesaplanıyor"):
    reference = entry.get("reference", "").strip()
    models = entry.get("models", {})

    for model_name, model_data in models.items():
        summary = model_data.get("summary", "").strip()

        if not reference or not summary:
            continue

        try:
            # BLEU skoru
            bleu_score = bleu.compute(predictions=[summary], references=[[reference]])["bleu"]

            # BERTScore (Türkçe varsayıldı)
            _, _, F1 = bert_score_fn([summary], [reference], lang="tr", verbose=False)
            bert_f1 = float(F1[0])

            # Skorları modele ekle
            model_data["bleu"] = bleu_score
            model_data["bertscore"] = bert_f1

        except Exception as e:
            print(f"{model_name} için hata: {e}")
            continue

# Sonuçları yeni bir JSON dosyasına kaydet
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"✅ BLEU ve BERTScore hesaplandı. Kaydedilen dosya: {output_path}")
