# Component API — `gameplus_blog_components.py`

Her fonksiyon inline-CSS'li bir HTML string döndürür. Import:

```python
import sys; sys.path.insert(0, "<skill>/scripts")
from gameplus_blog_components import *
```

## Sabitler
- `ANIMATED_BORDER_STYLE` — TEK `<style>` bloğu (conic/layer/pulse keyframe + hover-slide + mobil responsive + FAQ + yt-wrap). Final gövdenin **en başına bir kez** eklenir.
- `PAGE_HEAD` / `PAGE_FOOT` — tarayıcı önizlemesi için `<html><body>` sarmalayıcı. `PAGE_HEAD.replace("__TITLE__", baslik)`.
- SVG'ler: `SVG_TROPHY`, `SVG_CHECK_GREEN`, `SVG_EXT_LINK`, `SVG_DOC`, `SVG_BULB`, `SVG_CAL`, `SVG_BOOKMARK`, `SVG_BOLT`, `SVG_NEWS`, `SVG_ARROW`.

## Yardımcılar
- `slugify(text)` → URL-safe slug (Türkçe karakterleri çevirir).
- `hex_to_rgba(hex, alpha)` → tint/border renkleri için.
- `inject_heading_ids(html)` → `(yeni_html, toc_items)`. Her `<h2>/<h3>`'e `id` ekler; `toc_items` = `[(level, text, anchor), ...]`.
- `shrink_youtube_embeds(html)` → embed div'lerine `.gp-yt-wrap` ekler (max 720px, ortalı).
- `linkify_platforms(meta_text, game_name)` → meta string'indeki Steam/Xbox/Epic/Game Pass kelimelerini arama linkine çevirir + ↗ ikon. (GFN card-table meta'sı için.)

## Bileşenler

### `render_meta(date, category="GAME+ Blog")`
Üst meta chip'i. Genel blog: `render_meta("Güncellenme: 2026")`. GFN: `render_meta("21 Mayıs 2026", "GAME+ Blog · GFN Thursday")`.

### `render_tldr(items)`
`items` = HTML string listesi (**3-6 madde, duruma göre** — her zaman 4 şart değil). Her madde yeşil ✓ ile. V8 conic glow çerçeveli. Maddeleri `<strong>Etiket:</strong> açıklama` formatında ver. **Başlık ("Hızlı Özet") `<h2>`'dir.**

### `render_info_card(badges, style="grid")`
- `style="grid"` (genel blog): `badges` = `[(etiket, değer), ...]`. 4 metrik önerilir (İncelenen Remake / Beklenen / Öne Çıkan Stüdyo / Türler).
- `style="checkmark"`: `badges` = `[değer, ...]`. **GFN'de KULLANMA** (kaldırıldı).

### `render_floating_toc(items)`
`items` = `inject_heading_ids`'in döndürdüğü liste. Sağda sabit, tıklayınca kapanıp ilgili başlığa kayar.

### `render_editor_note(text)`
V9 layered (mavi). Game+ Editör Notu. `text` düz cümle.

### `render_highlight(text, title="Hatırlatma")`
V9 layered (amber). Lisans/uyarı kutusu.

### `render_cta_paketler(headline, desc)`
V8+V9. Paketler'e yönlendirir. **CTA dürüstlük kuralına uy** (bkz content-rules).

### `render_cta_oyunlar(headline, desc)`
V8+V9 (beyaz aksan). Oyun kütüphanesine yönlendirir. Sadece genel blogda.

### `render_end_cta(headline, desc, btn2_label, btn2_url, chip2)`
V8+V9 dual buton. Varsayılan 2. buton "Güncel Fırsatlar". **GFN'de:** `btn2_label="GeForce NOW Oyunları", btn2_url=".../gfn/oyunlar", chip2="Oyunlar"`.

### `render_ubisoft_cta(headline, desc)`
Ubisoft mavi. Yazıda Ubisoft oyunu (AC, Splinter Cell, PoP…) varsa.

### `render_compact_cta(game_name, tagline, button_label, button_url)`
**Sadece GFN.** Controller-Tag: oyun kolu ikonu + "★ ÖNE ÇIKAN" + isim + tagline + buton. Tek satır, dar. Haftanın öne çıkan oyunu için.

### `render_table(headers, rows)`
V9 layered, zebra striped, yumuşak çerçeve. `headers`=liste, `rows`=liste listesi. Hücrelerde `<strong>` kullanılabilir.

### `render_card_table(title, games)`
V9 layered + kompakt + Hover-Slide. `title` (trophy + gradient ile gösterilir). `games` listesi:
```python
{'name': 'Resident Evil 2 Remake', 'badge': 'KORKU', 'badge_color': '#dc2626',
 'meta': 'Capcom · 2019', 'anchor': 'resident-evil-2-remake',  # anchor varsa satır tıklanabilir
 'badge_href': None}  # opsiyonel: rozet kategori linki — YALNIZCA anchor yoksa uygulanır (iç içe <a> olmaz)
```
GFN'de `meta`'yı `linkify_platforms` ile platform-linkli ver, `anchor` koyma. Tür kategori linkini genelde **oyun başlığında** ver (card-row zaten jump-link).
**Rozet kontrastı:** rozet METNİ `lighten(badge_color, 0.45)` ile açık tondur (doygun renk değil), koyu zeminde kontrast 7:1+ olur (Lighthouse/PageSpeed kontrast uyarısını giderir). Zemin (tür rengi %16) ve kenar (%45) hâlâ tür rengindedir; kimlik korunur. Aynı kural `render_game_h3_inline` rozetinde de uygulanır.

### `render_game_h3_inline(anchor, name, badge, badge_color, meta_text, level="h3", badge_href=None)`
**ZORUNLU standart — yazıda >1 oyun varsa her oyun başlığı bu formatta** (genel blog listicle + State of Play gibi etkinlik özetleri). Düz `<h2/h3/h4>Oyun Adı</…>` bırakma.
- **`level`** = `"h2" | "h3" | "h4"` — çevredeki başlık seviyesine uy.
- Çıktı: `[TÜR] Oyun Adı` + altında `meta_text`. **`meta_text` = "Stüdyo · Yıl"** (ör. `Capcom · 2019`; engine opsiyonel: `Capcom · 2019 · RE Engine`).
- **Başlık metnine RENK atanmaz** (CMS başlık rengini verir; yük azalır). Rozet kendi tür rengini, meta soluk rengi taşır.
- **`badge_href`** verilirse tür rozeti o GFN kategori sayfasına iç link olur (`<a display:contents>` ile sarılır; linksiz rozetle birebir aynı yükseklik). URL'i `category_url_for(badge)` bulur — yalnızca tek/saf rozet eşleşir, birleşik rozet `None` döner. **Dedup YOK:** aynı yazıda eşleşen her rozet linklenir; build script artık `seen` kümesi tutmaz, doğrudan `category_url_for(badge)` sonucunu geçer (content-rules kural 12).
- Card-table satırıyla (badge=tür, meta="Stüdyo · Yıl") birebir aynı veri.

### `category_url_for(badge)` + `GFN_CATEGORY_URLS`
`badge` (ör. "Aksiyon") markanın linklenebilir GFN kategorilerinden birine **tam/saf** fit ediyorsa kategori URL'ini döndürür, yoksa `None`. **Birleşik/çift rozet (ayraçlı: "Aksiyon-RPG", "Aksiyon-Macera", "Indie-RPG") → `None`** (linklenmez); ayraç içeren rozet otomatik elenir. Çok kelimeli tekil kategoriler boşlukla yazıldığından ("Dövüş Oyunu", "Aile Dostu") eşleşir. Türkçe/case duyarsız. Linklenebilir set: strateji, aksiyon, simulasyon, dovus-oyunu, yaris, fps, mmo, macera, steam, canlandirma, moba, bagimsiz, arcade, bulmaca, basit-eglence, aile-dostu, platform, spor, ubisoft-connect, populer-oyunlar.

### `render_prev_weeks_cards(items)`
**Sadece GFN.** Soft-border kart grid. `items` = `[{'url':..., 'date':'14 Mayıs 2026', 'label':'...'}, ...]`.

### `render_faq_accordion(pairs)`
`pairs` = `[(soru, cevap), ...]`. Nabız atan `+` işaretli `<details>`.

### `render_inline_game_card(...)`
v5'te kaldırıldı (legacy). Kullanma — card-table + inline H3 onun yerine geçti.
