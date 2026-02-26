#!/usr/bin/env python3
"""
MakiNakarat Studio — Yeni Logo Ekleme Scripti
==============================================
KULLANIM:
1. Bu script'i index.html ile AYNI klasöre koy
2. Eklemek istediğin PNG dosyalarını da AYNI klasöre koy
3. Terminalde çalıştır:  python3 logo_ekle.py

Script, klasördeki tüm PNG/JPG dosyalarını bulur ve
henüz HTML'e eklenmemişleri otomatik olarak ekler.
"""

import os, base64, re, sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_FILE  = os.path.join(SCRIPT_DIR, "index.html")
BACKUP_FILE = os.path.join(SCRIPT_DIR, "index_yedek.html")

# Desteklenen uzantılar
EXTENSIONS = ('.png', '.jpg', '.jpeg', '.webp')

def dosya_adi_to_id(filename):
    """'spider-logo kırmızı.png' → 'spider_logo_kirmizi'"""
    name = os.path.splitext(filename)[0]
    name = name.lower()
    replacements = {
        'ı':'i','ş':'s','ğ':'g','ü':'u','ö':'o','ç':'c',
        'İ':'i','Ş':'s','Ğ':'g','Ü':'u','Ö':'o','Ç':'c',
        ' ':'_','-':'_','(':'',')':'','[':'',']':'',"'":'',
    }
    for old, new in replacements.items():
        name = name.replace(old, new)
    # Birden fazla alt çizgiyi tekle
    name = re.sub(r'_+', '_', name)
    return name.strip('_')

def guzellestir_label(filename):
    """'fast_and_furious.png' → 'Fast And Furious'"""
    name = os.path.splitext(filename)[0]
    return name.replace('_',' ').replace('-',' ').title()

def mime_type(filename):
    ext = os.path.splitext(filename)[1].lower()
    return {'png':'image/png','jpg':'image/jpeg','jpeg':'image/jpeg','webp':'image/webp'}.get(ext,'image/png')

# ── Ana işlem ──
print("\n🔧 MakiNakarat Studio — Logo Ekleme Aracı")
print("=" * 45)

if not os.path.exists(HTML_FILE):
    print(f"❌ HATA: '{HTML_FILE}' bulunamadı!")
    print("   Bu script'i index.html ile aynı klasöre koy.")
    sys.exit(1)

with open(HTML_FILE, 'r', encoding='utf-8') as f:
    html = f.read()

# Mevcut logo ID'lerini bul
mevcut_ids = set(re.findall(r"id:'([^']+)'", html))
print(f"📦 Mevcut logo sayısı: {len(mevcut_ids)}")

# Klasördeki PNG dosyalarını bul
klasordeki_dosyalar = [
    f for f in os.listdir(SCRIPT_DIR)
    if os.path.splitext(f)[1].lower().lstrip('.') in ('png','jpg','jpeg','webp')
    and f != 'index.html'
]

# index.html'e eklenmeyen yenileri filtrele
yeni_dosyalar = []
for dosya in sorted(klasordeki_dosyalar):
    id_ = dosya_adi_to_id(dosya)
    if id_ not in mevcut_ids:
        yeni_dosyalar.append(dosya)

if not yeni_dosyalar:
    print("\n✅ Eklenecek yeni dosya yok.")
    print("   Tüm PNG'ler zaten HTML'de mevcut.")
    sys.exit(0)

print(f"\n🆕 Eklenecek {len(yeni_dosyalar)} yeni dosya bulundu:")
for d in yeni_dosyalar:
    print(f"   + {d}")

# Yedek al
import shutil
shutil.copy(HTML_FILE, BACKUP_FILE)
print(f"\n💾 Yedek alındı: index_yedek.html")

# Her dosya için JS kodu oluştur
yeni_satirlar = []
for dosya in yeni_dosyalar:
    dosya_yolu = os.path.join(SCRIPT_DIR, dosya)
    with open(dosya_yolu, 'rb') as f:
        b64 = base64.b64encode(f.read()).decode()
    mime = mime_type(dosya)
    id_  = dosya_adi_to_id(dosya)
    label = guzellestir_label(dosya)
    src   = f"data:{mime};base64,{b64}"
    satir = f"  {{id:'{id_}',label:'{label}',file:'{dosya}',src:'{src}'}},"
    yeni_satirlar.append(satir)

# builtinLogos dizisinin sonuna ekle (son ]'den önce)
# Dizi şöyle: builtinLogos=[...son_eleman...]; 
# Son elemanın sonundaki virgülden sonra yeni satırları ekle
pattern = r'(const builtinLogos=\[)(.*?)(\];)'
def replace_logos(m):
    existing = m.group(2).rstrip()
    # Son virgül yoksa ekle
    if existing.rstrip()[-1] != ',':
        existing = existing.rstrip() + ','
    yeni_blok = '\n' + '\n'.join(yeni_satirlar)
    return m.group(1) + existing + yeni_blok + '\n' + m.group(3)

yeni_html = re.sub(pattern, replace_logos, html, flags=re.DOTALL)

if yeni_html == html:
    print("\n❌ HATA: builtinLogos dizisi bulunamadı!")
    print("   HTML dosyası beklenen formatta değil.")
    sys.exit(1)

with open(HTML_FILE, 'w', encoding='utf-8') as f:
    f.write(yeni_html)

boyut_mb = os.path.getsize(HTML_FILE) / 1024 / 1024
print(f"\n✅ Başarılı! {len(yeni_dosyalar)} logo eklendi.")
print(f"📁 Yeni dosya boyutu: {boyut_mb:.1f} MB")
print(f"\n🌐 index.html'i Cloudflare'e yükleyebilirsin!")
