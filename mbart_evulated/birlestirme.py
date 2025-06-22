import json
import os

# JSON dosyalarının bulunduğu klasör
klasor_yolu = "C:\\Users\\rose\\Desktop\\bitirme\\mbart_evulated"


# Birleştirilecek veriler burada toplanacak
birlesik_veri = []

# Klasördeki tüm JSON dosyalarını sırayla oku
for dosya_adi in os.listdir(klasor_yolu):
    if dosya_adi.endswith(".json"):
        dosya_yolu = os.path.join(klasor_yolu, dosya_adi)
        with open(dosya_yolu, "r", encoding="utf-8") as f:
            veri = json.load(f)
            birlesik_veri.append(veri)

# Tüm JSON verilerini tek bir dosyada yaz
with open("mbart_evaluated_modern.json", "w", encoding="utf-8") as f:
    json.dump(birlesik_veri, f, indent=4, ensure_ascii=False)

print("Tüm JSON dosyaları 'birlesik.json' dosyasında birleştirildi.")
