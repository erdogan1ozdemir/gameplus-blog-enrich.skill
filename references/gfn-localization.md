# GFN Thursday — Embargo (EN) → TR Yerelleştirme + Enrichment

NVIDIA, GFN Thursday haftalık derlemesini **İngilizce embargo draft'ı** olarak iletir
(`Embargoed_*ThisWeekOnGFN_*.docx`). Bu draft önce **Türkçeye yerelleştirilir**, sonra v9 GFN
enrichment uygulanır; teslim **tek `.docx`**: (1) yerelleştirilmiş metin + (2) `HTML Versiyon`
(enriched HTML). Ayrıca `files-preview` (canlı tipografi) + Excel rollup verilir.

## Tetikleyici
`Embargoed_*ThisWeekOnGFN_*.docx` ya da "GFN embargo metni / İngilizce GFN içeriği / yerelleştir +
enrich" iletildiğinde. (Zaten TR olan bir GFN docx gelirse yerelleştirme adımını atla, doğrudan enrich et.)

## İş akışı
1. **Parse + temizle.** Şunlar ATILIR: embargo notu, `Headline:`/`Sub-headline:`/`Publish Date:`,
   `++++`, `#### END ####`. Çıkar: başlık, alt başlık, giriş, öne çıkan oyun bölümleri
   (kısa başlık + tagline + açıklama), oyun listeleri (bu hafta / ayın geri kalanı / geçen ay).
2. **Yerelleştir** (aşağıdaki kurallar).
3. **YouTube fragmanı bul** (öne çıkan oyunlara). Bulamazsan kullanıcıdan link iste, sonra final.
4. **Un-enriched TR taslağı** yaz (yapı = aşağıdaki akış; başlık metnine `id` gelsin diye düz H1/H2).
5. **v9 GFN enrichment** uygula (bkz. `placement-rules.md` GFN bölümü).
6. **Çıktı:** teslim `.docx` (metin + `HTML Versiyon`) + `files-preview` + Excel.

## Yerelleştirme kuralları

### Dil / voice
- **Canlı, samimi, enerjik.** Model olarak **4 Haziran DIŞINDAKİ** yazıları al (15/29 Mayıs, Bahar
  Coşkusu, 27 Mart) — bunların akıcı, esprili dili. 4 Haziran'ın düz/birebir çeviri dilini KULLANMA.
- "sen" hitabı, retorik kancalar ("Peki, sen hazır mısın?", "Bitti mi? Tabii ki bitmedi!"). Yazı içinde
  siz/sen **tutarlı** olsun (varsayılan: sen).

### Kelime oyunu / deyim — DOĞAL yerelleştir (KRİTİK KURAL)
- İngilizce kelime oyunlarını, deyimleri, kültürel göndermeleri **Türkçede DOĞAL ve ANLAMLI**
  karşılığıyla ver.
- Bir kelime oyunu Türkçeye birebir oturmuyor ve **çiğ / zorlama / anlamsız** kalıyorsa **ZORLAMA** —
  espriyi ve tonu taşıyan temiz bir Türkçe ifadeyle değiştir; gerekirse o spesifik kelime oyununu BIRAK.
- ❌ **Yapma:** "License to stream, shaken and stirred" → "…bir ajan heyecanı: bu haftaki lisansımız
  'akış yapmaya'!" (çiğ, anlamsız, çeviri kokuyor).
- ✅ **Yap:** "Çalkalanmış ama karıştırılmamış, tam kıvamında bir ajan heyecanı seni bekliyor."
  (Bond martini esprisini taşır, doğal biter, "lisans" zorlamasını bırakır.)
- Diğer örnekler: "It's hammer time." → "Demir Tavında Dövülür!"; "He's back." → "O geri döndü!";
  "No joke" (1 Nisan göndermesi) → "Şaka yok!"; "Press Start on April" → "Nisan'a Başla Tuşuna Bas!".
- **Anlam ASLA bozulmaz:** oyun mekanikleri, çıkış tarihleri, donanım/teknik bilgiler, üyelik
  (Ultimate/Performance) detayları **birebir** korunur. Uydurma yok.

### Başlık & bölüm başlıkları & tagline
- **Başlık (H1):** yaratıcı TR; oyun adları korunur; enerjik. Birebir çeviri değil (ör. "Time to Slay:
  'DOOM…'" → "İblis Kasaplığı Vakti Geldi: 'DOOM…' GeForce NOW'da!").
- **Alt başlık:** H1'in altında **italik tek satır** giriş.
- **Bölüm başlıkları (H2):** yaratıcı TR (ör. "Stand and Fight" → "Direniş Başlasın, Düşman Titresin!";
  "Command the Frontier" → "Sınır Boylarını Geri Kazan!").
- **Tagline:** öne çıkan oyunun **video embed'inin hemen altında italik tek satır** (15 Mayıs stili;
  açıklamaya eritme). Ör. "First light, first mission." → *"İlk ışık, ilk görev."*

### Oyun listesi — çıkış tarihi formatı (SABİT)
- "New release on [Platform], [tarih]" → **"[Platform] çıkış tarihi: [TR tarih]"** — varsa **yıl dahil**.
  Steam/Xbox/Epic/Ubisoft fark etmez, **her platform için aynı**. Tarih YOKSA "çıkış tarihi" kullanma
  (yalnız platform/erişim notu).
- "available on Game Pass" → "Game Pass'te mevcut"; "available on the Microsoft store" → "Microsoft
  Store'da mevcut"; çoklu platformda "and" → "ve".
- Enrichment'ta liste **gerçek tabloya** döner (placement GFN kural 4); "Platform ve Çıkış" hücresi bu
  formatı taşır: `[Steam] çıkış tarihi: 26 Mayıs 2026`.

### İç linkler (kategori skili mantığı)
- EN linklerini (geforcenow.com, play.geforcenow.com, nvidia.com/geforce-now) **Gameplus muadiliyle**
  değiştir: "GeForce NOW" → `https://gameplus.com.tr/gfn`.
- Uygun yerlere ekle: `/gfn`, `/gfn/paketler` (Ultimate/Performance), `/gfn/oyunlar` (kütüphane),
  `/ubisoft` (Ubisoft+/Warcraft/King's Quest gibi Ubisoft başlıkları).
- **Tür kategori linkleri** (prose içinde, doğal): tek/saf tür GFN kategorisine fit ediyorsa
  `/gfn/oyunlar/<kategori>` (ör. "yarış oyunu" → /yaris, "aksiyon" → /aksiyon). **Birleşik tür
  linklenmez** (content-rules 12).
- **İlgili /blog yazıları:** varsa ekle (cloud-gaming-nedir, oyun izlenim yazıları). URL'leri kullanıcı
  verir veya mevcut olduğu doğrulanır — **uydurma URL YOK**.
- **Dış linkler (Reddit vb.):** kaldır; içeriği dış link olmadan yerelleştir.

### Şablon placeholder'ları & marka
- Kaynaktaki "[XX]" / "GeForce NOW powered by [XX]" → **"GeForce NOW powered by GAME+"** /
  "GAME+ kütüphanesi".
- Embargo metni "premium / Ultimate and Performance members" → "Ultimate ve Performance üyeleri".

### Dürüstlük
- "tüm oyunlara erişebilirsin" DEME → "sahip olduğun / kütüphanendeki oyunlar".

## YouTube fragmanları
- **Yalnız öne çıkan oyunlara** (kendi H2 bölümü olanlara) 16:9 embed. DataForSEO YouTube kapalı →
  **WebSearch** ile resmi fragman (yayıncı/resmi kanal; lansman/announce trailer tercih). Reaction/breakdown
  kanalı kullanma; timestamp tahmin etme.
- Bulamazsan **kullanıcıdan link iste**, sonra final sürümü ilet.

## Önceki Haftalar
- En altta, **End CTA'dan SONRA**: "GeForce NOW Thursday'de Önceki Haftalarda Neler Oldu?" H2 + giriş +
  `render_prev_weeks_cards()` grid; son 2-3 GFN Thursday blog URL'si; kart etiketi
  "Haftanın haberlerini oku →".
- URL'leri **kullanıcı verir VEYA sen öner** (doğrula, uydurma yok). ToC'ye bu H2 girmez.

## Yapı / akış (= 4 Haziran)
H1 → italik alt başlık → giriş → [öne çıkan oyun H2 (yaratıcı başlık) + 16:9 embed + italik tagline +
açıklama] × N → "Bu Hafta Eklenenler" tablosu → ["Ayın Geri Kalanı" tablosu, varsa] → ["Geçen Aydan
Öne Çıkanlar" tablosu, varsa] → **End CTA** → **"Önceki Haftalar" grid**.

## Teslim (.docx + HTML Versiyon)
- Teslim docx İKİ parçalıdır: **(1)** yerelleştirilmiş metin (Word başlık/paragraf/liste; öne çıkan
  oyunlarda YouTube linki metin olarak) + **(2)** `HTML Versiyon` (Heading 1) başlığı altında
  **v9-enriched body HTML** (markanın CMS'e yapıştırması için). Ayrıca `files-preview` + Excel.

## Build deseni (referans: `Dispatch/build_gfn28.py`, `examples/build-script-reference.py`)
```python
body, toc_items = inject_heading_ids(body)
toc = render_floating_toc([(l,t,a) for (l,t,a) in toc_items if l==2 and not t.startswith("GeForce NOW Thursday")])  # önceki-haftalar hariç
body = re.sub(r'<!--\s*EMBED:\s*(.*?)\s*([A-Za-z0-9_-]{11})\s*-->', lambda m: embed(m.group(2), m.group(1)), body)  # öne çıkan oyun videoları
# tldr (haftalık metrik), info-card (haftalık), oyun listesi <ul> -> render_table(["Oyun","Platform ve Çıkış"], rows)
# compact featured CTA (haftanın yıldızı), TEK End CTA, prev-weeks grid
body = body.replace("</h1>", "</h1>\n"+toc+tldr+info, 1)
# enjeksiyon çapaları için başlık METNİNE göre eşleştir (slug tahmini KIRILGAN: İ->i-niyor, thursday-de)
body = re.sub(r'(<h2 id="[^"]*">GeForce NOW Thursday)', endcta + r'\1', body, count=1)
body = demote_h1(body)  # gövde H1 içermez
```
