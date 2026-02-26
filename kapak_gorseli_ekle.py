import base64, shutil

# Gorselleri base64'e cevir
with open("cosplay-1.png","rb") as f:
    cosplay = "data:image/png;base64," + base64.b64encode(f.read()).decode()
with open("garaj-1.png","rb") as f:
    garaj = "data:image/png;base64," + base64.b64encode(f.read()).decode()

with open("index.html","r",encoding="utf-8") as f:
    html = f.read()

# Yedek al
shutil.copy("index.html","index_yedek.html")

# Degistirilecek satırlar
old_a = '.home-btn-a{background:linear-gradient(135deg,#0f2a4a,#1a3a6b);border-color:#60A5FA;color:#fff}'
new_a = '.home-btn-a{background:url("' + cosplay + '") center/cover no-repeat;border-color:#60A5FA;color:#fff;position:relative;overflow:hidden}'

old_b = '.home-btn-b{background:linear-gradient(135deg,#1a2e0a,#2d5016);border-color:#86efac;color:#fff}'
new_b = '.home-btn-b{background:url("' + garaj + '") center/cover no-repeat;border-color:#86efac;color:#fff;position:relative;overflow:hidden}'

old_hover = '.home-btn:hover{transform:translateY(-6px);box-shadow:0 20px 50px rgba(0,0,0,.4)}'
new_hover = '.home-btn:hover{transform:translateY(-6px);box-shadow:0 20px 50px rgba(0,0,0,.4)}.home-btn::before{content:"";position:absolute;inset:0;background:rgba(0,0,0,0.45);border-radius:14px;z-index:0}'

old_icon = '.home-btn-icon{font-size:3rem}'
new_icon = '.home-btn-icon{font-size:3rem;position:relative;z-index:1}'

old_title = ".home-btn-title{font-family:'Bebas Neue',sans-serif;font-size:1.3rem;letter-spacing:1.5px;text-align:center;line-height:1.2}"
new_title = ".home-btn-title{font-family:'Bebas Neue',sans-serif;font-size:1.3rem;letter-spacing:1.5px;text-align:center;line-height:1.2;position:relative;z-index:1}"

old_sub = '.home-btn-sub{font-size:.78rem;color:rgba(255,255,255,.6);text-align:center;line-height:1.5}'
new_sub = '.home-btn-sub{font-size:.78rem;color:rgba(255,255,255,.9);text-align:center;line-height:1.5;position:relative;z-index:1}'

html = html.replace(old_a, new_a)
html = html.replace(old_b, new_b)
html = html.replace(old_hover, new_hover)
html = html.replace(old_icon, new_icon)
html = html.replace(old_title, new_title)
html = html.replace(old_sub, new_sub)

with open("index.html","w",encoding="utf-8") as f:
    f.write(html)

print("Tamamlandi! index_yedek.html yedegi alindi.")
print("Yeni boyut: " + str(len(html)//1024) + " KB")