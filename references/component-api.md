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
`items` = HTML string listesi. Her madde yeşil ✓ ile. V8 conic glow çerçeveli. Maddeleri `<strong>Etiket:</strong> açıklama` formatında ver.

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
 'meta': 'Capcom · 2019', 'anchor': 'resident-evil-2-remake'}  # anchor varsa satır tıklanabilir
```
GFN'de `meta`'yı `linkify_platforms` ile platform-linkli ver, `anchor` koyma.

### `render_game_h3_inline(anchor, name, badge, badge_color, meta_text)`
**ZORUNLU standart — her oyun başlığı bu formatta** (genel blog listicle + State of Play gibi etkinlik özetleri). Düz `<h3>Oyun Adı</h3>` bırakma. Çıktı: `[TÜR] Oyun Adı` + altında `meta_text`. **`meta_text` = "Stüdyo · Yıl"** (ör. `Capcom · 2019`; engine opsiyonel olarak eklenebilir: `Capcom · 2019 · RE Engine`). Card-table satırıyla (badge=tür, meta="Stüdyo · Yıl") birebir aynı veri. Bkz. content-rules kural 11.

### `render_prev_weeks_cards(items)`
**Sadece GFN.** Soft-border kart grid. `items` = `[{'url':..., 'date':'14 Mayıs 2026', 'label':'...'}, ...]`.

### `render_faq_accordion(pairs)`
`pairs` = `[(soru, cevap), ...]`. Nabız atan `+` işaretli `<details>`.

### `render_inline_game_card(...)`
v5'te kaldırıldı (legacy). Kullanma — card-table + inline H3 onun yerine geçti.
