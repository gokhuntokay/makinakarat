import re, shutil, os

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

shutil.copy("index.html", "index_yedek.html")

# ── DÜZELTME 1: cosplay-1.png → assets/cosplay-1.png (doğru isim) ──
# asset_001.png'yi cosplay-1.png olarak yeniden adlandır
if os.path.exists("assets/asset_001.png"):
    os.rename("assets/asset_001.png", "assets/cosplay-1.png")
    print("✓ assets/asset_001.png → assets/cosplay-1.png")

if os.path.exists("assets/asset_002.png"):
    os.rename("assets/asset_002.png", "assets/garaj-1.png")
    print("✓ assets/asset_002.png → assets/garaj-1.png")

html = html.replace('url("assets/asset_001.png")', 'url("assets/cosplay-1.png")')
html = html.replace('url("assets/asset_002.png")', 'url("assets/garaj-1.png")')

# ── DÜZELTME 2: Overlay kararmasını azalt 0.45 → 0.20 ──
html = html.replace(
    'background:rgba(0,0,0,0.45)',
    'background:rgba(0,0,0,0.20)'
)
print("✓ Overlay kararması azaltıldı (0.45 → 0.20)")

# ── DÜZELTME 3: Greenbox görselleri .jpeg → .jpg uzantısını dene her ikisini de ──
# Şu an "greenbox-1.jpeg" yazıyor, dosyalar "greenbox-1.jpg" ise değiştir
# Önce kontrol et: klasörde .jpg mi .jpeg mi var?
has_jpg   = os.path.exists("greenbox-1.jpg")
has_jpeg  = os.path.exists("greenbox-1.jpeg")

if has_jpg and not has_jpeg:
    # Dosyalar .jpg, HTML'de .jpeg yazıyor → düzelt
    html = re.sub(r'"greenbox-(\d+)\.jpeg"', r'"greenbox-\1.jpg"', html)
    print("✓ Greenbox uzantıları .jpeg → .jpg düzeltildi")
elif has_jpeg:
    print("✓ Greenbox dosyaları .jpeg uzantılı, HTML ile uyumlu — değişiklik yok")
else:
    print("⚠ greenbox-1.jpg veya greenbox-1.jpeg bulunamadı!")
    print("  Greenbox görsellerini ana klasöre (index.html ile aynı yere) kopyala.")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print(f"\n✅ Tamamlandı! Yeni boyut: {len(html)//1024} KB")
print("\nGitHub'a push etmeyi unutma:")
print("  git add .")
print('  git commit -m "gorsel duzeltmeleri"')
print("  git push origin main")
