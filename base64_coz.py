"""
MakiNakarat Studio — Base64 Çözücü
====================================
Bu script index.html içindeki tüm base64 görsellerini
ayrı dosyalara çıkarır ve HTML'i küçültür.

Sonuçta klasör yapısı şöyle olur:
  index.html        (~küçük)
  assets/
    taslak.jpg
    spiderman_character.png
    deadpool.png
    ... vb

KULLANIM:
  1. Bu scripti index.html ile AYNI klasöre koy
  2. python3 base64_coz.py
  3. Çıkan "assets" klasörü ve yeni index.html'i birlikte Cloudflare'e yükle
"""

import re, base64, os, shutil

HTML_FILE = "index.html"
ASSETS_DIR = "assets"

os.makedirs(ASSETS_DIR, exist_ok=True)
shutil.copy(HTML_FILE, "index_yedek.html")

with open(HTML_FILE, "r", encoding="utf-8") as f:
    html = f.read()

print(f"Orijinal boyut: {len(html)//1024} KB")

# Tüm data URI'leri bul: data:image/TYPE;base64,DATA
pattern = re.compile(r'data:(image/[a-zA-Z+]+);base64,([A-Za-z0-9+/=]+)')
matches = list(pattern.finditer(html))
print(f"{len(matches)} adet base64 görsel bulundu.")

# Her birini dosyaya çıkar
ext_map = {
    "image/png": "png",
    "image/jpeg": "jpg",
    "image/jpg": "jpg",
    "image/webp": "webp",
    "image/svg+xml": "svg",
}

replaced = {}  # data_uri -> dosya_yolu (aynı görseli iki kez yazma)
counter = 1

for m in matches:
    mime = m.group(1)
    b64data = m.group(2)
    data_uri = m.group(0)
    
    if data_uri in replaced:
        continue  # zaten işlendi
    
    ext = ext_map.get(mime, "bin")
    
    # Dosya adını tahmin et — JS içindeki label'dan bulmaya çalış
    # Örn: label:'Deadpool',file:'deadpool.png',src:'data:...'
    pos = m.start()
    snippet = html[max(0, pos-200):pos]
    
    fname_match = re.search(r"file:'([^']+)'[^']*$", snippet)
    if fname_match:
        fname = fname_match.group(1)
        # Türkçe karakter temizle
        fname = fname.replace("ı","i").replace("ş","s").replace("ğ","g")
        fname = fname.replace("ü","u").replace("ö","o").replace("ç","c")
    else:
        fname = f"asset_{counter:03d}.{ext}"
    
    out_path = os.path.join(ASSETS_DIR, fname)
    
    # Aynı isimde dosya varsa numara ekle
    if os.path.exists(out_path):
        base, dotext = os.path.splitext(out_path)
        out_path = f"{base}_{counter}{dotext}"
    
    with open(out_path, "wb") as f:
        f.write(base64.b64decode(b64data))
    
    replaced[data_uri] = out_path.replace("\\", "/")
    print(f"  ✓ {out_path}  ({os.path.getsize(out_path)//1024} KB)")
    counter += 1

# HTML içindeki data URI'leri dosya yollarıyla değiştir
# CSS background:url("data:...") -> background:url("assets/...")
# JS src:'data:...' -> src:'assets/...'
new_html = html
for data_uri, file_path in replaced.items():
    new_html = new_html.replace(data_uri, file_path)

with open(HTML_FILE, "w", encoding="utf-8") as f:
    f.write(new_html)

print(f"\nYeni index.html boyutu: {len(new_html)//1024} KB")
print(f"Toplam {len(replaced)} dosya 'assets/' klasörüne çıkarıldı.")
print("\nCloudflare'e yüklenecek dosyalar:")
print("  index.html")
print("  assets/ (tüm klasör)")
print("  taslak.jpg, greenbox-*.jpeg, otocar-*.jpg (varsa)")
