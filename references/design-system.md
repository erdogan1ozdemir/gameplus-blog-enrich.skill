# Tasarım Sistemi (v9 — son hal)

Tüm görsel kurallar `scripts/gameplus_blog_components.py` içindeki `ANIMATED_BORDER_STYLE` ve render fonksiyonlarında hazır. Bu dosya neyin neden öyle olduğunu açıklar; değer değiştirmek istersen referans.

## Renk paleti
> **Arka plan:** Site zaten siyah; **bloklara ekstra siyah arka plan BASMA** (bloklar `transparent`, siteyle kaynaşır). Sadece floating ToC gibi overlay'ler kendi zeminini taşır.
> **Başlık rengi:** Doküman başlıklarına (H1/H2/H3/H4 ve oyun başlıkları) **renk ATAMA** — CMS başlık rengini zaten veriyor (yük azalır). Aşağıdaki #fff yalnızca önizleme (PAGE_HEAD) içindir.

| Token | Hex | Kullanım |
|---|---|---|
| Arka plan | `transparent` | Bloklar (site zaten `#000`; ekstra siyah basma) |
| Gövde metni | `#cbd5e1` | Paragraf (önizlemede #b2b2b2) |
| Başlık | `#fff` *(yalnız önizleme)* | H1/H2/H3 — CMS verir, biz body'de atamayız |
| Soluk metin | `#a8b2c0` | meta, açıklama (eski #8b95a7'ten bir tık beyaza yakın) |
| GFN yeşili | `#76b900` | birincil aksan, butonlar |
| Açık yeşil | `#a3e635` | link, hover |
| Amber | `#f59e0b` | hatırlatma, fırsat |
| Game+ sarı | `#fbbf24` | meta chip, uyarı başlığı |
| Ubisoft mavi | `#0061ff` | Ubisoft CTA |
| Editör mavi | `#3b82f6` / `#93c5fd` | editör notu |

### Tür (badge) renkleri — tutarlı taksonomi
> **Tür adı:** Oyun GFN'deyse hangi GFN kategorisine giriyorsa onu yaz (Aksiyon, Macera, Canlandırma/RPG, Strateji, FPS, Platform, MMO, Yarış, Dövüş, Spor, Bağımsız/Indie, Bulmaca, Arcade, MOBA, Aile Dostu, Basit Eğlence, Simülasyon…). Birden fazla türe uyuyorsa birleşik (Aksiyon-Macera, Aksiyon-RPG, Indie-RPG). GFN'de yoksa uygun türü seç. Tür GFN kategorisine fit ediyorsa rozet o kategoriye iç link olur (content-rules 12).
> **Rozet kontrastı (WCAG):** Aşağıdaki hex'ler rozetin **kenar + zemini** (tür rengi) içindir. Rozet **METNİ** bu rengin açık tonudur (`lighten(renk, 0.45)`) — koyu zeminde doygun renk metin kontrastı düşürüp Lighthouse/PageSpeed uyarısı verir; açık ton 7:1+ kontrast sağlar. Zemin tür rengi %16, kenar %45.

Renk eşlemesi (kenar/zemin):

| Tür | Hex |
|---|---|
| KORKU (tüm survival/psikolojik/uzay korku) | `#dc2626` |
| JRPG | `#7c3aed` |
| AKSİYON-MACERA | `#0891b2` |
| GİZLİLİK (stealth) | `#16a34a` |
| PLATFORM | `#f59e0b` |
| SOULSLIKE | `#a3a3a3` |
| YARIŞ | `#dc2626` |
| FPS | `#0891b2` |
| STRATEJİ | `#16a34a` |
| CO-OP / ROGUELIKE / CO-OP TAKTİK | `#7c3aed` |
| INDIE | `#f59e0b` |

## Çerçeve / efekt sistemi

### V8 — Rotating Conic Glow (`.gp-conic`)
Çerçeve etrafında 6 sn'de bir tur atan ışık parçası. `@property --gp-conic-angle` + `conic-gradient` mask tekniği. `--gp-glow` ile renk verilir.
**Kullanım:** Hızlı Özet (TLDR) + büyük CTA'ların DIŞ çerçevesi. Dikkat çeken "hero" bloklar için.
```html
<div class="gp-conic" style="--gp-glow:#76b900;"><div class="gp-conic-inner">…</div></div>
```

### V9 — Layered Frame (`.gp-layer`)
Soluk renkli dış çerçeve + `::before` ile 5px içeride çok soluk ikinci çizgi. Sakin, premium, derinlik hissi. `--gp-frame` ile dış renk.
**Kullanım:** Hatırlatma, Editör notu, karşılaştırma tabloları, card-table, compact CTA. Sık tekrar eden, dikkat dağıtmaması gereken bloklar.
```html
<div class="gp-layer" style="--gp-frame:rgba(245,158,11,0.22);padding:14px 18px;">
  <div style="position:relative;z-index:1;">…</div>
</div>
```
> İçerik `position:relative;z-index:1` olmalı (yoksa `::before` üstünü kapatır).

### Büyük CTA = V8 + V9 kombo
Dış `.gp-conic` (dönen ışık) + iç `.gp-conic-inner.gp-layer` (soluk çerçeve). En zengin blok.

## Bileşene özel detaylar
- **Trophy ikon:** `SVG_TROPHY` — "En İyi N…" başlığında yıldız yerine kupa, GFN yeşil→amber gradient.
- **Yeşil tik:** `SVG_CHECK_GREEN` — TLDR ve checkmark info-card maddelerinde nokta yerine.
- **Controller-Tag compact CTA:** oyun kolu SVG + "★ ÖNE ÇIKAN" üst etiket + isim + tagline + buton. Sol tarafta yeşil gradient yıkama (`linear-gradient(90deg, rgba(118,185,0,0.06), transparent 40%)`).
- **Hover-Slide card-table:** her satırın `--row-c` değişkeni türün rengi. `:hover` → sol kenarda 4px renkli çubuk kayar + satır arka planı hafif aydınlanır. Steam liste hissi.
- **Pulsing FAQ +:** `.faq-icon` 2.2 sn nabız animasyonu; `[open]` durumunda 45° dönerek `×` olur.
- **YouTube embed:** `.gp-yt-wrap` max 720px, ortalı, gölgeli.
- **Tablolar:** zebra striping (`rgba(255,255,255,0.015)` çift satırlar), başlık satırı yeşil uppercase, alt border `tr:last-child` için kapatılmış (köşeler `overflow:hidden`).

## Mobil responsive
`ANIMATED_BORDER_STYLE` içinde `@media (max-width:700px)`:
- Card-table satırı 2 satıra döner: badge + isim üstte, meta altta full-width.
- Inline game card aside float kalkar, full-width olur.
- YouTube wrap margin küçülür.

Her zaman mobilde kontrol et (badge'lerin taşmadığından, card-row'ların stack olduğundan emin ol).
