---
name: gameplus-blog-enrich
description: Enrich gameplus.com.tr (GeForce NOW Türkiye, powered by GAME+) BLOG POSTS with premium dark-theme HTML components without rewriting the author's sentences. Takes blog drafts delivered as .docx (or html/md/text) and ADDS enrichment (TLDR, info-card, floating ToC, comparison tables, clickable game card-table, inline-tag game headings, CTA blocks, FAQ accordion, editor notes, GFN "previous weeks" grid), then outputs ready-to-paste HTML, by default an Excel rollup (title to html) or separate files / combined preview on request. Use whenever the user gives a Gameplus BLOG post (a guide, listicle, "remake nedir", "en iyi X oyunlar", weekly "GFN Thursday" roundup) and asks to enrich, format, style, add CTA/TLDR/FAQ/tables, or convert blog docs to HTML. Trigger on "blog içeriğini zenginleştir", "gfn thursday html", "bu blog yazısını formatla", "blog docx'lerini html yap", or when blog .docx files are handed over. Do NOT use for /gfn/oyunlar/* CATEGORY pages (that is gameplus-category-content).
---

# Gameplus Blog Enrichment

Bu skill, **gameplus.com.tr blog yazılarını** (NVIDIA GeForce NOW powered by GAME+ Türkiye) zengin, koyu temalı, premium HTML bileşenleriyle süsler. Kritik kural: **yazarın cümlelerini değiştirmez** — sadece enrichment öğeleri EKLER (TLDR, info-card, ToC, tablolar, oyun kartları, CTA'lar, FAQ, editör notları). Çıktı CMS'e yapıştırılmaya hazır HTML'dir; varsayılan olarak Excel'de toplanır (başlık → html).

Bu tasarım, Gameplus ekibiyle çok turlu revizyonla oturmuş son haldir (v9). Tüm görsel ve içerik kuralları bu skill'de hazır gelir — sıfırdan tasarlamaya gerek yok.

## Ne zaman tetiklenir

- Kullanıcı bir veya birden fazla **blog yazısını** (.docx / .html / .md / yapıştırılmış metin) iletip "zenginleştir / formatla / HTML yap / CTA-TLDR-FAQ ekle" derse
- "GFN Thursday" haftalık oyun derlemesi iletildiğinde
- "En iyi X oyunlar", "X nedir", rehber/listicle tarzı blog taslağı iletildiğinde
- Blog docx'leri CMS'e hazırlanmak istendiğinde

**TetiklenME:** `/gfn/oyunlar/*` kategori sayfaları için DEĞİL — o ayrı `gameplus-category-content` skill'idir. Bu skill blog (`/blog/*`) içindir.

## İki blog tipi

Skill iki blog tipini ayırt eder; bileşen seti farklıdır:

| Öğe | Genel Blog (rehber/listicle) | GFN Thursday (haftalık) |
|---|---|---|
| Meta header | `⚡ GAME+ Blog · 📅 Güncellenme: YIL` | `⚡ GAME+ Blog · GFN Thursday · 📅 tarih` |
| Info-card | ✅ (4 metrik: incelenen sayı, öne çıkan, türler…) | ❌ (kaldırıldı — bariz bilgi koymuyoruz) |
| Card-table | "En İyi N …" tıklanabilir liste (oyun bölümlerine kayar) | "Bu Hafta Eklenen Oyunlar" (platform linkli) |
| CTA sayısı | 3 (Paketler ortada, Oyunlar orta-son, dual End CTA) | **Tek** End CTA + 1 compact featured CTA |
| Compact CTA | yok | ✅ öne çıkan oyun için (Controller-Tag) |
| Önceki haftalar | yok | ✅ soft-border kart grid |
| Editör notu / Hatırlatma | ihtiyaç oldukça | ihtiyaç oldukça |

Detaylı yerleşim kuralları: **`references/placement-rules.md`**.

## Workflow

### 1. Taslağı oku ve yapıyı çıkar
- `.docx` ise: `python3 -c "from docx import Document; ..."` veya `references/docx-extract.md`'deki yöntemle paragraf/başlık/liste/link yapısını çıkar. YouTube embed'leri ve `<iframe>`'leri **olduğu gibi koru**.
- Başlıkları (H2/H3), paragrafları, listeleri, linkleri, görsel/video embed'lerini belirle.
- Blog tipini tespit et (GFN Thursday mı, genel blog mu).

### 2. Orijinal HTML gövdesini hazırla
- Yazarın metnini HTML'e çevir (H1/H2/H3, `<p>`, `<ul>`, `<a>`, embed'ler). **Cümleleri değiştirme.**
- `inject_heading_ids(html)` ile her H2/H3'e `id` ekle ve ToC öğelerini topla.
- `shrink_youtube_embeds(html)` ile embed'leri `.gp-yt-wrap` (max 720px, ortalı) yap.

### 3. Bileşenleri üret (component library)
`scripts/gameplus_blog_components.py`'i import et. Her bileşen inline-CSS'li HTML string döndürür. İçeriğe göre (yazıyı OKUYARAK) doğru verileri sen kararlaştırırsın — TLDR maddeleri, hangi oyunların card-table'a gireceği, türleri, CTA metinleri.

```python
import sys; sys.path.insert(0, "<skill>/scripts")
from gameplus_blog_components import *

toc_items = []  # inject_heading_ids doldurur
body, toc_items = inject_heading_ids(body)
body = shrink_youtube_embeds(body)

meta   = render_meta("Güncellenme: 2026")                      # genel blog
tldr   = render_tldr(["<strong>…:</strong> …", ...])           # ✓ tikli maddeler
info   = render_info_card([("İncelenen", "12 Yapım"), ...])    # sadece genel blog
toc    = render_floating_toc(toc_items)
cta_p  = render_cta_paketler(headline, desc)
table  = render_table(["Tip","Kapsam",...], [[...],[...]])
cards  = render_card_table("En İyi 12 Remake Oyunu", games)    # games: aşağıda
faq    = render_faq_accordion([(soru, cevap), ...])
```

### 4. Yerleştir (placement)
`references/placement-rules.md`'deki kurallara göre bileşenleri orijinal gövdeye `str.replace` / `re.sub` ile enjekte et. Özet:
- Meta + ToC + TLDR + (info-card) → H1'den hemen sonra
- Karşılaştırma tablosu → ilgili kavram paragrafından sonra
- **CTA Paketler** → 2. H2'den önce
- **Card-table** → listicle'ın yerine, ilk oyun H3'ünden ÖNCE (genel blog); GFN'de oyun listesi yerine
- Genel blogda her oyun H3'ü → `render_game_h3_inline()` ile tag+isim+meta formatına çevir
- **End CTA** → SSS H2'sinden önce
- **FAQ accordion** → SSS bölümündeki H3+P çiftlerinin yerine

### 5. Birleştir ve çıktı al
- `body = ANIMATED_BORDER_STYLE + enriched_body` (style bloğu bir kez, en başta)
- Önizleme için: `PAGE_HEAD.replace("__TITLE__", baslik) + body + PAGE_FOOT`
- **Çıktı:** `scripts/export_output.py` → `export(items, fmt="excel")`. Varsayılan Excel rollup (Başlık | HTML Part1 | HTML Part2 | Slug | Karakter). Kullanıcı farklı isterse: `fmt="files"` (ayrı body-only), `fmt="files-preview"` (tarayıcıda açılır tam HTML), `fmt="combined"` (tek dosyada toplu önizleme).

`items` formatı:
```python
items = [{"title": "Remake Nedir? …", "slug": "remake-nedir-…", "html": final_body}]
```

## Tasarım sistemi (v9 — son hal)

Detaylar **`references/design-system.md`**'de. Özet:
- **Arka plan:** her yerde saf siyah `#000` (site koyu temalı)
- **Renkler:** `#76b900` GFN yeşili · `#f59e0b` amber · `#fbbf24` Game+ sarı · `#0061ff` Ubisoft mavi · tür renkleri (korku `#dc2626`, JRPG `#7c3aed`, aksiyon-macera `#0891b2`, gizlilik `#16a34a`, platform `#f59e0b`, soulslike `#a3a3a3`)
- **TLDR + büyük CTA dış çerçeve:** V8 "Rotating Conic Glow" (`.gp-conic`, dönen ışık)
- **Hatırlatma + Editör notu + tablolar + card-table + compact CTA:** V9 "Layered Frame" (`.gp-layer`, soluk renkli dış + çok soluk iç çerçeve)
- **Büyük CTA:** V8 dış + V9 iç kombinasyonu
- **Compact CTA (öne çıkan oyun):** Controller-Tag (oyun kolu ikonu + "★ ÖNE ÇIKAN")
- **Card-table satırları:** Hover-Slide Accent (üstüne gelince sol kenarda türün renginde çubuk kayar)
- **Başlık ikonu:** trophy SVG (yıldız değil), gradient
- **TLDR/info-card maddeleri:** yeşil ✓ SVG (nokta değil)
- **FAQ:** nabız atan `+` işareti (açılınca 45° döner)
- **Türkçe tür etiketleri:** "KORKU" (SURVIVAL HORROR değil), "GİZLİLİK" (STEALTH değil); ROGUELIKE/SOULSLIKE/INDIE/JRPG İngilizce terim olarak kalır. **Aynı yazıda tutarlı taksonomi** — RE2 ve RE4 ikisi de "KORKU", farklı isim verme.

## İçerik kuralları (zorunlu)

Tam liste **`references/content-rules.md`**'de. En kritikleri:
- **Yazarın cümlelerini ASLA değiştirme.** Sadece enrichment ekle.
- **CTA dürüstlüğü:** "tüm yapımlara erişebilirsin" DEME (her oyun GFN'de olmayabilir). "satın aldığın / sahip olduğun / kütüphanendeki oyunlar" de.
- **Lisans hatırlatması:** GFN oyun satmaz, sadece çalıştırır; oyunun ilgili platformda (Steam/Xbox/Epic) lisansına sahip olmak gerekir.
- **GFN Thursday'de tek CTA** yeterli (Paketler + Oyunlar yönlendirmesi). İki ayrı blok koyma.
- Em dash (—) kullanma; nokta veya virgülle böl.
- Görsel alt text / caption / şema markup EKLEME (kullanıcı istemiyor).
- YouTube embed'leri ve mevcut linkleri koru.

## Çıktı formatları

| `fmt` | Sonuç |
|---|---|
| `excel` (varsayılan) | `gameplus-blog-icerikler.xlsx` — satır başına blog: Başlık \| HTML(1) \| HTML(2) \| Slug \| Karakter. 32.767 char limiti için HTML iki hücreye bölünür. |
| `files` | Her blog için ayrı `ornek-blog-<slug>-body-only.html` |
| `files-preview` | Her blog için tarayıcıda açılır tam HTML |
| `combined` | Tek dosyada tüm bloglar (hızlı önizleme) |

Çıkışı CWD'ye yaz (genelde `/Users/Erdo/Desktop/Claude Projects/Dispatch/`). Kullanıcı formatı belirtmezse Excel yap ve "ayrı dosya / önizleme de isteyebilirsin" diye belirt.

## Referans dosyaları

- `references/design-system.md` — tüm renkler, V8/V9 efektleri, bileşen görünümleri
- `references/placement-rules.md` — bileşenlerin yazıya nereye/nasıl enjekte edileceği, GFN vs genel blog
- `references/content-rules.md` — dürüstlük, kopya, taksonomi, yasak öğeler
- `references/component-api.md` — her `render_*` fonksiyonunun imzası, parametreleri, örnek çağrı
- `references/docx-extract.md` — .docx'ten yapı çıkarma yöntemi
- `examples/` — v9 referans çıktıları (remake + gfn-thursday) ve `build-script-reference.py` (tam assembly örneği)

Yeni bir blog geldiğinde **`examples/build-script-reference.py`**'i şablon al, içeriğe göre verileri değiştir.
