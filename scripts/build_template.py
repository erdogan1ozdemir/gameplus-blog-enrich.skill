"""
Build template — KOPYALA ve içeriğe göre uyarla.
=================================================
Bu, bir blog yazısını zenginleştirmek için minimal iskelet. Component library'yi
import eder, bileşenleri üretir, orijinal gövdeye enjekte eder, çıktı alır.

Gerçek kullanımda:
  1. Bu dosyayı /tmp/build_<slug>.py olarak kopyala
  2. SKILL_DIR yolunu doğrula
  3. `original_body`'yi .docx'ten çıkardığın gerçek HTML ile doldur
  4. TLDR maddeleri / card-table oyunları / CTA metinleri vb. içeriğe göre değiştir
  5. placement-rules.md'ye göre enjeksiyon hedeflerini yazının cümlelerine göre ayarla
  6. python3 ile çalıştır
"""
import sys, os

SKILL_DIR = os.path.expanduser("~/.claude/skills/gameplus-blog-enrich/scripts")
sys.path.insert(0, SKILL_DIR)
from gameplus_blog_components import *      # render_* + ANIMATED_BORDER_STYLE + PAGE_HEAD/FOOT
from export_output import export

OUT_DIR = "/Users/Erdo/Desktop/Claude Projects/Dispatch"

# ─── 1. Orijinal gövde (yazarın metni, HTML'e çevrilmiş — CÜMLELER DEĞİŞMEZ) ───
original_body = """<h1>BLOG BAŞLIĞI</h1>
<p>Giriş paragrafı...</p>
<h2>İlk Bölüm</h2>
<p>...</p>
"""  # ← .docx'ten çıkarılan gerçek içerikle değiştir

# ─── 2. Heading id + ToC + embed shrink ───
body, toc_items = inject_heading_ids(original_body)
body = shrink_youtube_embeds(body)

# ─── 3. Bileşenler (içeriğe göre doldur) ───
meta = render_meta("Güncellenme: 2026")                 # GFN için: render_meta("21 Mayıs 2026", "GAME+ Blog · GFN Thursday")
toc  = render_floating_toc(toc_items)
tldr = render_tldr([
    "<strong>Madde 1:</strong> ...",
    "<strong>Madde 2:</strong> ...",
])
info = render_info_card([                                 # SADECE genel blog
    ("İncelenen", "12 Yapım"), ("Öne Çıkan", "..."),
])

card_table = render_card_table("En İyi N ... Oyunu", [
    {'name': 'Oyun A', 'badge': 'KORKU', 'badge_color': '#dc2626',
     'meta': 'Stüdyo · 2024', 'anchor': 'oyun-a'},
    # ...
])

end_cta = render_end_cta(
    "Efsane oyunları bulutta yeniden yaşa!",
    "Performance veya Ultimate paketle kütüphanendeki GeForce NOW destekli yapımları başlat.",
)  # GFN: btn2_label="GeForce NOW Oyunları", btn2_url=".../gfn/oyunlar", chip2="Oyunlar"

faq = render_faq_accordion([
    ("Soru 1?", "Cevap 1."),
    ("Soru 2?", "Cevap 2."),
])

# ─── 4. Enjeksiyon (placement-rules.md — hedef cümleleri yazıdan seç) ───
body = re.sub(r'(</h1>)', r'\1\n' + meta + toc + tldr + info, body, count=1)
# body = body.replace('<h2 id="ikinci-h2">', cta_paketler + '<h2 id="ikinci-h2">', 1)
# body = body.replace('<h3 id="ilk-oyun">', card_table + '<h3 id="ilk-oyun">', 1)
# ... (placement-rules.md'deki tüm adımlar)
# body = body.replace('<h2 id="sss">', end_cta + '<h2 id="sss">', 1)

# ─── 5. Birleştir + çıktı ───
final_body = ANIMATED_BORDER_STYLE + body

items = [{
    "title": "BLOG BAŞLIĞI",
    "slug": slugify("BLOG BAŞLIĞI"),
    "html": final_body,
}]

# Varsayılan Excel. Kullanıcı isterse: fmt="files" | "files-preview" | "combined"
out = export(items, fmt="excel", out_path=os.path.join(OUT_DIR, "gameplus-blog-icerikler.xlsx"))
print("✓ Çıktı:", out)

# Tarayıcı önizlemesi istenirse her blog için tam HTML de yaz:
# preview = PAGE_HEAD.replace("__TITLE__", items[0]["title"]) + final_body + PAGE_FOOT
# open(os.path.join(OUT_DIR, f"ornek-blog-{items[0]['slug']}.html"), "w").write(preview)
