# Yerleşim Kuralları — bileşenler yazıya nereye girer

Orijinal gövde HTML'ine bileşenleri `str.replace` / `re.sub` ile enjekte et. Hedef metinleri yazının gerçek cümlelerinden seç (aşağıdaki örnekler remake/GFN yazılarından; yeni yazıda muadil cümleyi bul).

## Genel Blog (rehber / listicle / "X nedir")

Sıra:
1. **H1'den hemen sonra:** `floating_toc + tldr + info_card` (**meta header YOK** — render_meta DEPRECATED; bkz. content-rules 6/7). Gövde **tek bir H1 ile başlar** (ilk başlık = yazı başlığı).
   ```python
   body = re.sub(r'(</h1>)', r'\1\n' + toc + tldr + info, body, count=1)
   ```
2. **Karşılaştırma tablosu:** ilgili kavramın açıklandığı paragraftan sonra (örn. "Remake/Remaster/Reboot" farkını anlatan son cümleden sonra).
3. **CTA Paketler:** 2. H2'den HEMEN ÖNCE.
   ```python
   body = body.replace('<h2 id="ikinci-h2-slug">', cta_paketler + '<h2 id="ikinci-h2-slug">', 1)
   ```
4. **Editör notu 1:** ilgili paragraftan sonra (örn. stüdyo/başarı anlatımı).
5. **Listicle → Card-table:** orijinal "en iyi N oyun" madde listesini (`<ul>…</ul>`) SİL, yerine card-table'ı **ilk oyun H3'ünden ÖNCE** koy. Böylece tablo tüm oyun bölümlerinin tıklanabilir indeksi olur.
   ```python
   body = re.sub(r'<ul><li><p>İlk Oyun Adı</p></li>.*?</ul>', '', body, count=1, flags=re.DOTALL)
   body = body.replace('<h3 id="ilk-oyun-slug">', card_table + '<h3 id="ilk-oyun-slug">', 1)
   ```
6. **Her oyun başlığı → inline format (ZORUNLU; yazıda BİRDEN FAZLA oyun varsa):** düz `<h2/h3/h4 id="x">Oyun Adı</…>`'ü `render_game_h3_inline(anchor, isim, "TÜR", renk, "Stüdyo · Yıl", level="h2|h3|h4", badge_href=…)` ile değiştir. **Başlık H2/H3/H4 olabilir** (çevredeki seviyeye uy). **Başlık metnine RENK atanmaz** (CMS verir). Tür + stüdyo + yıl her oyunda; card-table satırındaki veriyle birebir aynı. Yıl yoksa dönem ("2027 (beklenen)", "Belirsiz", "Yayında"). Tür GFN kategorisine fit ediyorsa rozet o kategoriye iç link (`badge_href=None` otomatik: tek/saf rozet tüm rozeti, birleşik rozet HER PARÇAYI ayrı linkler; `False` = link yok), dedup yok (eşleşen her rozet linklenir) — content-rules 12. Tek oyun anlatılıyorsa başlık şart değil. Etkinlik özetleri (State of Play) dahil.
7. **Oyun fragmanı (YouTube embed) yeri:** Bir oyunun fragmanı varsa, embed **oyun başlığının HEMEN ALTINA, açıklama metninden ÖNCE** gelir (sıra: **başlık → embed → açıklama**). Embed'i başlığın ÜSTÜNE koyma. Taslakta her oyun başlığının altına `<!-- EMBED: <ad> <11-haneli-video-id> -->` koy; build EN SON karakter grubunu (video id) 16:9 iframe'e çevirir. (GFN'de öne çıkan oyun bölümünde sıra: başlık → embed → italik tagline → açıklama.)
7. **CTA Oyunlar (OPSİYONEL):** listenin ~2/3'ünde bir oyun başlığından önce. **CTA sayısı 2-3'tür; her zaman 3 şart değil** — kısa/odaklı yazıda CTA Oyunlar atlanabilir (Paketler + dual End kalır).
8. **İkinci tablo** (varsa, örn. "beklenen oyunlar"): ilgili giriş paragrafından sonra.
9. **Editör notu 2 / Ubisoft CTA:** ilgili bölümden sonra (Ubisoft oyunu geçiyorsa Ubisoft CTA).
10. **Hatırlatma (highlight):** lisans/GFN uyarısının olduğu paragraftan önce.
11. **FAQ accordion:** "Sıkça Sorulan Sorular" H2'sinden sonraki H3+P çiftlerini bul, hepsini tek accordion ile değiştir.
12. **End CTA:** SSS H2'sinden HEMEN ÖNCE (dual buton: Paketler + Fırsatlar).

## GFN Thursday (haftalık derleme)

> **0. Embargo (EN) draft'ı geldiyse ÖNCE YERELLEŞTİR** (`references/gfn-localization.md`): canlı dil (4 Haziran dışı yazıların tonu), kelime oyunlarını doğal/anlamlı Türkçeyle (çiğ kalıyorsa zorlama), çıkış tarihi formatı **"[Platform] çıkış tarihi: [TR tarih]"**, iç linkler (/gfn, /gfn/paketler, /gfn/oyunlar, /ubisoft, tür kategori, ilgili /blog), öne çıkan oyunlara **YouTube fragmanı** (bulunmazsa kullanıcıdan iste), öne çıkan oyun bölümünde **italik tagline** (embed'in hemen altında). SONRA aşağıdaki enrichment'ı uygula. **Teslim:** tek `.docx` = yerelleştirilmiş metin + `HTML Versiyon` (enriched HTML) + `files-preview` + Excel.

Farklar:
1. **H1'den sonra (enjeksiyon çapası):** `toc + tldr + info-card` `</h1>`'den hemen sonra enjekte edilir; **meta header YOK** (render_meta DEPRECATED, ekleme; site/CMS marka adı + tarihi zaten gösterir). **Gövde TEK bir H1 ile BAŞLAR** (ilk başlık = yazı başlığı, H1) — build en SON adımda `ensure_leading_h1(body)` çağırır (taslakta H1 varsa korur, yoksa ilk başlığı H1 yapar; `demote_h1` DEPRECATED — content-rules 7). **TLDR ve info-card GFN'de de ZORUNLU.** GFN info-card 4 metrik; metrikler yazının ritmine göre değişir:
   - **Aylık / ay başı yazısı:** "Bu Ay Eklenen: N Oyun" (ayın toplamı), "Ayın/Haftanın Öne Çıkanı", "Öne Çıkan Dönüş", "Platformlar" (Steam · Epic · Xbox).
   - **Haftalık yazı:** "Bu Ay Eklenen oyun sayısı" metriğini ZORLAMA — her hafta yeni oyun eklenmeyebilir (bazı haftalar yeni oyun yerine DLC / yeni sezon / güncelleme gelir ya da katalogdan kalkan bir oyun geri döner). **"Bu Hafta Eklenen: 0" gibi olumsuz/boş değer gösterme;** metrikleri o haftanın gerçek içeriğine göre seç (örn. "Bu Hafta Eklenen" yalnızca gerçekten yeni oyun varsa, "Haftanın Öne Çıkanı", "Öne Çıkan Güncelleme/DLC/Sezon", "Geri Dönen Oyun", "Platformlar"). Ayrıntı: `content-rules.md` kural 10.
2. **Compact CTA (Controller-Tag):** haftanın öne çıkan oyununun bölümünden hemen sonra / 2. H2'den önce. Tek öne çıkan oyun için.
3. **Editör notu:** öne çıkan oyunun video embed'inden sonra (opsiyonel).
4. **Oyun listeleri → GERÇEK TABLO**, card-table DEĞİL. `render_table(["Oyun","Platform ve Çıkış"], rows)` kullan; rozetsiz card-table sol sütunu boş bırakıp "tablo gibi" durmuyor. Her satır: `["<strong>Oyun Adı</strong>", platform/çıkış bilgisi]`; ikinci sütundaki platform adlarını **docx'teki gerçek mağaza linkleriyle** bağla (linkify_platforms arama linki üretir; varsa docx'in tam ürün URL'lerini tercih et). Birden fazla liste varsa (bu hafta eklenenler / ayın geri kalanı / önceki ay öne çıkanlar) her biri için **ayrı H3 + tablo**. **(content-rules kural 11)** Tutarlılık için GFN tablosu da oyunun **türü + stüdyosu + çıkış yılını** taşımalı: tabloya bir **"Tür"** sütunu ekle ve mümkünse stüdyo + çıkış yılını ver (platform/eklenme bilgisini koruyarak, örn. `["<strong>Oyun</strong>", "Tür", "Stüdyo", "Platform · Çıkış"]`). Haftanın öne çıkan oyununun kendi bölümü varsa başlığını inline formatla (`render_game_h3_inline`) ver.
5. **Hatırlatma:** lisans uyarısı (`render_highlight`).
6. **End CTA (TEK):** `btn2_label="GeForce NOW Oyunları", btn2_url=".../gfn/oyunlar", chip2="Oyunlar"`. İkinci ayrı CTA bloğu koyma — tek blok Paketler + Oyunlar'ı kapsar.
7. **"Önceki Haftalarda Neler Oldu?" bölümü EN ALTTA** (End CTA'dan SONRA, yazının son bloğu olarak): H2 + giriş paragrafı + `render_prev_weeks_cards()` grid. Kart alt etiketi **"Haftanın haberlerini oku →"** tarzında olsun; oyun-spesifik ("o haftanın yeni oyunları") yazma.

## Genel kurallar
- **Oyun giriş formatı HER YAZIDA AYNI (yazıda >1 oyun varsa):** her oyun **tür + Stüdyo · Yıl** taşır — başlıklarda `render_game_h3_inline` (H2/H3/H4, başlığa renk atama), card-table'da badge=tür + meta="Stüdyo · Yıl", GFN tablolarında Tür/Stüdyo/Çıkış. Tür GFN kategorisine fit ediyorsa rozet o kategoriye iç link — tek/saf rozet tüm rozeti, birleşik rozet her parçayı ayrı linkler (badge_href=None otomatik), dedup yok, sadece oyun başlığında (liste/tabloda değil). Detay: content-rules 12.
- **Özet (TLDR) madde sayısı:** 3-6 (duruma göre). **CTA sayısı:** 2-3 (Oyunlar opsiyonel). **Ekstra siyah arka plan basma** (site zaten siyah; bloklar transparent). **Başlık rengini CMS'e bırak.**
- Style bloğu (`ANIMATED_BORDER_STYLE`) final gövdenin **en başına bir kez**.
- Her `replace`/`sub` için `count=1` — yanlışlıkla çoklu enjeksiyon olmasın.
- **Enjeksiyondan sonra `verify_output(final_body, blog_type=..., n_games=..., expect_faq=...)` + `print_report(...)` çalıştır** (content-rules 13 + `references/qa-checklist.md`): tek H1 + ilk başlık H1, meta header yok, ANIMATED_BORDER_STYLE 1x, ToC/TLDR(3-6)/info-card, oyun sayısı (inline başlık = card-row), embed aspect-ratio, em dash yok. **FAIL varsa teslim etme, düzelt.**
- Çoklu blog: her biri için aynı pipeline; sonda `export(items, fmt=...)`.
