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
6. **Her oyun H3'ü → inline format:** düz `<h3 id="x">Oyun Adı</h3>`'ü `render_game_h3_inline()` çıktısıyla değiştir (tag + isim + `Stüdyo · Yıl · Engine`).
7. **CTA Oyunlar:** listenin ortasına/sonuna doğru bir oyun H3'ünden önce (örn. listenin ~2/3'ü).
8. **İkinci tablo** (varsa, örn. "beklenen oyunlar"): ilgili giriş paragrafından sonra.
9. **Editör notu 2 / Ubisoft CTA:** ilgili bölümden sonra (Ubisoft oyunu geçiyorsa Ubisoft CTA).
10. **Hatırlatma (highlight):** lisans/GFN uyarısının olduğu paragraftan önce.
11. **FAQ accordion:** "Sıkça Sorulan Sorular" H2'sinden sonraki H3+P çiftlerini bul, hepsini tek accordion ile değiştir.
12. **End CTA:** SSS H2'sinden HEMEN ÖNCE (dual buton: Paketler + Fırsatlar).

## GFN Thursday (haftalık derleme)

Farklar:
1. **H1'den sonra:** `meta(GFN) + toc + tldr` — **info-card YOK.**
2. **Compact CTA (Controller-Tag):** haftanın öne çıkan oyununun bölümünden hemen sonra / 2. H2'den önce. Tek öne çıkan oyun için.
3. **Editör notu:** öne çıkan oyunun video embed'inden sonra (opsiyonel).
4. **Oyun listesi → Card-table:** "Bu Hafta Eklenen Oyunlar". `meta`'ları `linkify_platforms()` ile platform-linkli ver, `anchor` koyma (oyunların ayrı bölümü yok).
5. **Önceki haftalar:** orijinal link listesini `render_prev_weeks_cards()` grid'i ile değiştir.
6. **Hatırlatma:** lisans uyarısı.
7. **End CTA (TEK):** son H2'den önce. `btn2_label="GeForce NOW Oyunları", btn2_url=".../gfn/oyunlar", chip2="Oyunlar"`. **İkinci ayrı CTA bloğu koyma** — tek blok Paketler + Oyunlar'ı kapsar.

## Genel kurallar
- Style bloğu (`ANIMATED_BORDER_STYLE`) final gövdenin **en başına bir kez**.
- Her `replace`/`sub` için `count=1` — yanlışlıkla çoklu enjeksiyon olmasın.
- Enjeksiyondan sonra doğrula: `grep -c "card-row"`, badge sayısı, FAQ sayısı beklenenle uyuşmalı.
- Çoklu blog: her biri için aynı pipeline; sonda `export(items, fmt=...)`.
