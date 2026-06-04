# Yerleşim Kuralları — bileşenler yazıya nereye girer

Orijinal gövde HTML'ine bileşenleri `str.replace` / `re.sub` ile enjekte et. Hedef metinleri yazının gerçek cümlelerinden seç (aşağıdaki örnekler remake/GFN yazılarından; yeni yazıda muadil cümleyi bul).

## Genel Blog (rehber / listicle / "X nedir")

Sıra:
1. **H1'den hemen sonra:** `meta + floating_toc + tldr + info_card`
   ```python
   body = re.sub(r'(</h1>)', r'\1\n' + meta + toc + tldr + info, body, count=1)
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
6. **Her oyun H3'ü → inline format (ZORUNLU, her yazıda aynı):** düz `<h3 id="x">Oyun Adı</h3>`'ü `render_game_h3_inline(anchor, isim, "TÜR", renk, "Stüdyo · Yıl")` ile değiştir. **Tür etiketi + yapımcı stüdyo + çıkış yılı her oyunda bulunur** ve card-table satırındaki veriyle birebir aynıdır (badge=tür, meta="Stüdyo · Yıl"). Engine opsiyonel; asıl üçlü tür + stüdyo + yıl. Yeni duyurulan oyunda kesin yıl yoksa dönem yaz ("2027 (beklenen)", "Belirsiz", "Yayında"). Bkz. content-rules kural 11. **Aynı kural etkinlik özetleri (State of Play vb.) için de geçerli:** oradaki her oyun bölümünün başlığını da bu inline formata çevir.
7. **CTA Oyunlar:** listenin ortasına/sonuna doğru bir oyun H3'ünden önce (örn. listenin ~2/3'ü).
8. **İkinci tablo** (varsa, örn. "beklenen oyunlar"): ilgili giriş paragrafından sonra.
9. **Editör notu 2 / Ubisoft CTA:** ilgili bölümden sonra (Ubisoft oyunu geçiyorsa Ubisoft CTA).
10. **Hatırlatma (highlight):** lisans/GFN uyarısının olduğu paragraftan önce.
11. **FAQ accordion:** "Sıkça Sorulan Sorular" H2'sinden sonraki H3+P çiftlerini bul, hepsini tek accordion ile değiştir.
12. **End CTA:** SSS H2'sinden HEMEN ÖNCE (dual buton: Paketler + Fırsatlar).

## GFN Thursday (haftalık derleme)

Farklar:
1. **H1'den sonra:** `toc + tldr + info-card` — **meta header YOK** (render_meta ekleme; CMS kategori + tarihi zaten gösterir). **TLDR ve info-card GFN'de de ZORUNLU.** GFN info-card 4 metrik; metrikler yazının ritmine göre değişir:
   - **Aylık / ay başı yazısı:** "Bu Ay Eklenen: N Oyun" (ayın toplamı), "Ayın/Haftanın Öne Çıkanı", "Öne Çıkan Dönüş", "Platformlar" (Steam · Epic · Xbox).
   - **Haftalık yazı:** "Bu Ay Eklenen oyun sayısı" metriğini ZORLAMA — her hafta yeni oyun eklenmeyebilir (bazı haftalar yeni oyun yerine DLC / yeni sezon / güncelleme gelir ya da katalogdan kalkan bir oyun geri döner). **"Bu Hafta Eklenen: 0" gibi olumsuz/boş değer gösterme;** metrikleri o haftanın gerçek içeriğine göre seç (örn. "Bu Hafta Eklenen" yalnızca gerçekten yeni oyun varsa, "Haftanın Öne Çıkanı", "Öne Çıkan Güncelleme/DLC/Sezon", "Geri Dönen Oyun", "Platformlar"). Ayrıntı: `content-rules.md` kural 10.
2. **Compact CTA (Controller-Tag):** haftanın öne çıkan oyununun bölümünden hemen sonra / 2. H2'den önce. Tek öne çıkan oyun için.
3. **Editör notu:** öne çıkan oyunun video embed'inden sonra (opsiyonel).
4. **Oyun listeleri → GERÇEK TABLO**, card-table DEĞİL. `render_table(["Oyun","Platform ve Çıkış"], rows)` kullan; rozetsiz card-table sol sütunu boş bırakıp "tablo gibi" durmuyor. Her satır: `["<strong>Oyun Adı</strong>", platform/çıkış bilgisi]`; ikinci sütundaki platform adlarını **docx'teki gerçek mağaza linkleriyle** bağla (linkify_platforms arama linki üretir; varsa docx'in tam ürün URL'lerini tercih et). Birden fazla liste varsa (bu hafta eklenenler / ayın geri kalanı / önceki ay öne çıkanlar) her biri için **ayrı H3 + tablo**. **(content-rules kural 11)** Tutarlılık için GFN tablosu da oyunun **türü + stüdyosu + çıkış yılını** taşımalı: tabloya bir **"Tür"** sütunu ekle ve mümkünse stüdyo + çıkış yılını ver (platform/eklenme bilgisini koruyarak, örn. `["<strong>Oyun</strong>", "Tür", "Stüdyo", "Platform · Çıkış"]`). Haftanın öne çıkan oyununun kendi bölümü varsa başlığını inline formatla (`render_game_h3_inline`) ver.
5. **Hatırlatma:** lisans uyarısı (`render_highlight`).
6. **End CTA (TEK):** `btn2_label="GeForce NOW Oyunları", btn2_url=".../gfn/oyunlar", chip2="Oyunlar"`. İkinci ayrı CTA bloğu koyma — tek blok Paketler + Oyunlar'ı kapsar.
7. **"Önceki Haftalarda Neler Oldu?" bölümü EN ALTTA** (End CTA'dan SONRA, yazının son bloğu olarak): H2 + giriş paragrafı + `render_prev_weeks_cards()` grid. Kart alt etiketi **"Haftanın haberlerini oku →"** tarzında olsun; oyun-spesifik ("o haftanın yeni oyunları") yazma.

## Genel kurallar
- **Oyun giriş formatı HER YAZIDA AYNI:** Bir liste/bölümdeki her oyun **tür etiketi + Stüdyo · Yıl** taşır — başlıklarda `render_game_h3_inline`, card-table satırlarında badge=tür + meta="Stüdyo · Yıl", GFN tablolarında Tür/Stüdyo/Çıkış sütunları. Düz `<h3>Oyun Adı</h3>` bırakma. Detay: content-rules kural 11.
- Style bloğu (`ANIMATED_BORDER_STYLE`) final gövdenin **en başına bir kez**.
- Her `replace`/`sub` için `count=1` — yanlışlıkla çoklu enjeksiyon olmasın.
- Enjeksiyondan sonra doğrula: `grep -c "card-row"`, badge sayısı, FAQ sayısı beklenenle uyuşmalı.
- Çoklu blog: her biri için aynı pipeline; sonda `export(items, fmt=...)`.
