import os
import json
from collections import defaultdict

# JSON dosyalarının bulunduğu klasör
klasor_yolu = "C:\\Users\\rose\\Desktop\\bitirme\\mt5_evulated"  # burayı senin klasör yoluna göre değiştir

dosya_listesi = [f for f in os.listdir(klasor_yolu) if f.endswith(".json")]

# Hedef metrik isimleri
hedef_metrikler = [
    "relevance", "coherence", "consistency", "fluency",
    "conciseness", "quotation_score", "overall_score"
]

# Her metrik için: dosya ortalamaları listesi
tum_metrik_ortalamalari = defaultdict(list)

def extract_scores_average(dosya_yolu):
    with open(dosya_yolu, "r", encoding="utf-8") as f:
        data = json.load(f)

    # JSON formatına göre entries listesi çıkar
    if isinstance(data, list) and len(data) == 1 and isinstance(data[0], list):
        entries = data[0]
    elif isinstance(data, list) and all(isinstance(i, dict) for i in data):
        entries = data
    else:
        raise ValueError("Beklenmeyen JSON formatı")

    metrik_toplamlari = defaultdict(float)
    metrik_sayilari = defaultdict(int)

    for entry in entries:
        scores = entry.get("scores", {})
        if isinstance(scores, dict):
            for metrik in hedef_metrikler:
                if isinstance(scores.get(metrik), (int, float)):
                    metrik_toplamlari[metrik] += scores[metrik]
                    metrik_sayilari[metrik] += 1

    ortalamalar = {}
    for metrik in hedef_metrikler:
        if metrik_sayilari[metrik] > 0:
            ortalamalar[metrik] = metrik_toplamlari[metrik] / metrik_sayilari[metrik]

    return ortalamalar

# Her dosya için işle
for dosya in dosya_listesi:
    yol = os.path.join(klasor_yolu, dosya)
    try:
        ortalamalar = extract_scores_average(yol)
        if ortalamalar:
            print(f"\n{dosya}:")
            for metrik, ort in ortalamalar.items():
                print(f"  {metrik}: {ort:.2f}")
                tum_metrik_ortalamalari[metrik].append(ort)
        else:
            print(f"{dosya}: skor bulunamadı.")
    except Exception as e:
        print(f"{dosya}: HATA - {e}")

# Her metrik için genel ortalama
print("\n📊 HER METRİK İÇİN GENEL ORTALAMA:")
for metrik in hedef_metrikler:
    skorlar = tum_metrik_ortalamalari[metrik]
    if skorlar:
        genel = sum(skorlar) / len(skorlar)
        print(f"  {metrik}: {genel:.2f}")
    else:
        print(f"  {metrik}: veri yok")
