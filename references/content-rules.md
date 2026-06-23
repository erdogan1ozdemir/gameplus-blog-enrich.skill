# İçerik Kuralları (Gameplus ekibiyle oturmuş, zorunlu)

Bu kurallar çok turlu revizyonla netleşti. İhlal etme.

## 1. Yazarın metni dokunulmaz
- **Yazarın cümlelerini DEĞİŞTİRME, yeniden yazma, kısaltma.** Skill sadece enrichment EKLER.
- Mevcut linkleri, YouTube embed'lerini, `<iframe>`'leri olduğu gibi koru.
- Yeni cümle eklemek gerekiyorsa (TLDR, CTA, editör notu, FAQ) — bunlar enrichment'tır, yazının gövdesine karışmaz.

## 2. CTA dürüstlüğü (en kritik)
- **"Tüm yapımlara/oyunlara erişebilirsin" DEME.** Her oyun GeForce NOW'da olmayabilir.
- Şu ifadeleri kullan: **"satın aldığın oyunlar", "sahip olduğun oyunlar", "kütüphanendeki oyunlar", "GeForce NOW destekli yapımlar"**.
- Örnek doğru cümle: *"Resident Evil 4 Remake'ten Final Fantasy VII Rebirth'e, satın almış olduğun ve GeForce NOW destekli remake yapımlarını Performance veya Ultimate paketle saniyeler içinde başlatabilirsin."*

## 3. Lisans hatırlatması
GeForce NOW oyun SATMAZ, sadece bulutta ÇALIŞTIRIR. Oynamak için oyunun **GFN'in desteklediği bir platformda** (Steam, Epic Games Store, Xbox / Xbox Game Pass, Ubisoft Connect, GOG, EA App, Battle.net vb.) lisansına sahip olmak gerekir. Hatırlatma (highlight) bloğunda bunu net belirt.

**PlayStation Store'u ASLA YAZMA.** GFN PlayStation'ı desteklemez. "Steam, PlayStation Store veya Xbox'ta" gibi bir platform listesi verme; sadece GFN'in gerçekten desteklediği platformları say. Eğer desteklenen platformlar bilinmiyorsa genel olarak "ilgili platformda" de, PlayStation'a atıfta bulunma.

## 4. GFN Thursday CTA sadeliği
- **Tek End CTA yeterli.** İki ayrı CTA bloğu (mid + end) koyma.
- End CTA metni (onaylı):
  > **Başlık:** Game+ ile bulutta oyun keyfine hazır mısın?
  > **Açıklama:** Performance ve Ultimate paketleri kütüphanendeki GeForce NOW destekli yapımları donanım olmadan oynamanı sağlar. 2.000'den fazla oyunu ve GFN Thursday'e eklenen yeni yapımları görmek için hemen kütüphaneye göz at!
  > Butonlar: **Paketler** + **Oyunlar** (Fırsatlar değil).
- Öne çıkan oyun varsa orta kısma **tek satır compact CTA** (Controller-Tag).

## 5. Tür etiketleri (taksonomi) — mümkünse GFN kategorilerini kullan
- **Oyun GFN kütüphanesindeyse**, hangi GFN kategorisine giriyorsa o türü yaz. Mevcut kategoriler (rozet adı olarak bunları tercih et): **Basit Eğlence, Bulmaca, Strateji, Macera, Canlandırma (RPG), Simülasyon, Dövüş, Yarış, Aile Dostu, Platform, Spor, Bağımsız (Indie), Aksiyon, Oynaması Ücretsiz, MMO, Demo, FPS, Arcade, MOBA.**
- **Oyun GFN'de var ve birden fazla türe uyuyorsa** birleşik rozet yazabilirsin: **Aksiyon-Macera, Aksiyon-RPG, Indie-RPG** gibi. (Not: birleşik rozette **her parça kendi kategorisine** linklenir — Aksiyon-Macera → Aksiyon /aksiyon + Macera /macera; bkz. kural 12.)
- **Oyun GFN'de yoksa** uygun türü sen seç (yukarıdakilerden veya dışından: KORKU, SOULSLIKE, ROGUELIKE, METROIDVANIA, HAYATTA KALMA, DÖVÜŞ vb.).
- Türkçesi yaygınsa Türkçe yaz (KORKU = SURVIVAL/PSİKOLOJİK/UZAY HORROR hepsi tek "KORKU", GİZLİLİK = stealth, YARIŞ, STRATEJİ, PLATFORM). Terim kalanlar İngilizce: **JRPG, SOULSLIKE, ROGUELIKE, INDIE, FPS, MOBA, CO-OP**. "INDIE" (İNDİ değil), "CO-OP" (KOOP değil).
- **Aynı yazıda tutarlılık:** RE2 ve RE4 ikisi de "KORKU"; aynı tür → aynı etiket → aynı renk.

## 6. Yazım / üslup
- **Em dash (—) kullanma.** Nokta veya virgülle böl.
- Dil yazarın diliyle uyumlu olsun (samimi "sen" dili, Gameplus tonu).
- Tarih/breadcrumb/marka adı gibi alanları yazıya EKLEME — site/CMS bunları (eklenme tarihi + GAME+ marka adı) zaten gösteriyor. **Üst meta header / tarih-marka chip'i KOYMA** (`render_meta` DEPRECATED; çağırma). Bkz. kural 7.

## 7. EKLENMEYECEKLER
- **Gövde TEK bir H1 ile BAŞLAR (ilk başlık = yazı başlığı, H1).** Bu kural eskiden tersineydi (gövdeye H1 ekleme, H2'ye çevir); **ARTIK her blog yazısı gövdede bir H1 ile başlar.** `ensure_leading_h1(body)` build akışının EN SON adımıdır: taslakta H1 varsa KORUR, yoksa gövdedeki ilk başlığı (h2-h6) H1'e yükseltir. Gövdede yalnız **1 adet H1** olsun; bölüm başlıkları H2/H3 kalır. ToC yalnız h2/h3'ten beslendiği için H1 ToC'ye girmez. (`demote_h1` DEPRECATED — artık H1'i korur, çağırma.)
- **Üst meta header / tarih-marka chip'i EKLEME.** Site/CMS yazının eklenme tarihini ve GAME+ marka adını zaten gösteriyor; gövdeye `render_meta` ile ikinci bir tarih/marka şeridi koymak tekrar olur (`render_meta` DEPRECATED; çağırma).
- Görsel alt text, caption, figure açıklaması **EKLEME**.
- Schema markup / JSON-LD **EKLEME**.
- Bariz/gereksiz info-card alanları koyma (örn. "Yayın Tarihi / Kategori"; bunlar CMS'te zaten belli). GFN'de info-card VAR (4 metrik), ama metrikleri yazının türüne göre seç (bkz. kural 10).

## 8. Platform linkleri (GFN tablosu)
GFN'in desteklediği ve **herkese açık (public) olarak paylaşılan** platformları linkle + küçük ↗ ikon. Orijinal yazıda zaten link varsa onu koru.

**Desteklenen GFN platformları (bunları linkleyebilirsin):**
Steam · Epic Games Store · Xbox / Xbox Game Pass · Ubisoft Connect · GOG · EA App · Battle.net · Wargaming

**KESİNLİKLE LINKLEME:** PlayStation Store, PlayStation Network. GeForce NOW, PlayStation platformlarını DESTEKLEMEZ; oyuna PlayStation'da sahip olsan bile GFN'de oynayamazsın. Bu platformlardan hiç bahsetme.

**Çıkış / Eklenme tarihi sütunu:** Kaynakta (docx) tarih belirtilmemişse o hücreye **"-" yaz**. "Bu hafta eklendi", "Mevcut" gibi belirsiz/uydurma ifade yazma. Tarih varsa "Steam çıkış tarihi: GG Ay YYYY" formatında ver (GFN localization kuralı); yoksa "-".

## 9. Öne çıkarılan oyun (GFN)
Çok öne çıkan bir oyun varsa (haftanın yıldızı) orta kısma compact CTA. Kompakt, tek satır, dar — sayfayı boğmaz.

## 10. GFN info-card metrikleri: aylık vs haftalık (dürüstlük)
GFN yazılarının iki ritmi var; info-card ve TLDR metrikleri buna göre değişir:
- **Ay başı / aylık yazı:** "Bu Ay Eklenen: N Oyun" metriği uygundur (ayın toplam yeni oyun sayısı).
- **Haftalık yazı:** "Bu Ay Eklenen oyun sayısı" metriğini ZORLAMA. Her hafta yeni oyun eklenmeyebilir; bazı haftalar yeni oyun yerine **DLC, yeni sezon veya güncelleme (update)** gelir, ya da **katalogdan kalkmış bir oyun geri döner**. **"Bu Hafta Eklenen: 0" gibi boş/olumsuz bir metrik KOYMA.**
- Haftalık metrikleri o haftanın GERÇEK içeriğine göre seç. Örnekler: "Bu Hafta Eklenen" (yalnızca gerçekten yeni oyun varsa sayı ver), "Haftanın Öne Çıkanı" (oyun), "Öne Çıkan Güncelleme / DLC / Yeni Sezon", "Geri Dönen Oyun", "Platformlar" (Steam · Epic · Xbox).
- TLDR ilk maddesi de aynı mantıkla: yeni oyun yoksa "Bu hafta: N yeni oyun" deme; "Bu hafta öne çıkan: X'in yeni sezonu / Y güncellemesi / geri dönen Z" gibi o haftaya özgü bir özet ver.

## 11. Oyun giriş formatı: tür + stüdyo + yıl (HER YAZIDA AYNI — zorunlu)
**Yazıda birden fazla oyundan bahsediliyorsa**, her oyunun başına bir oyun başlığı ekle ve 3 veri taşı: **(1) tür etiketi, (2) yapımcı stüdyo, (3) çıkış yılı/dönemi.** (Tek bir oyun anlatılıyorsa oyun başlığı şart değil.) Format bütün yazılarda (genel blog, listicle, etkinlik özeti, GFN) aynıdır.
- **Oyun başlığı H2, H3 veya H4 olabilir** — çevredeki başlık seviyesine uy. `render_game_h3_inline(anchor, "Oyun Adı", "TÜR", renk, "Stüdyo · Yıl", level="h2|h3|h4")` ile ver. **Düz `<h2/h3/h4 id="x">Oyun Adı</…>` BIRAKMA.** Yazarın başlık metnini koru, sadece tür rozeti + stüdyo·yıl ekle.
- **Başlık metnine RENK atama.** CMS başlık rengini zaten verir (render_game_h3_inline başlığa renk basmaz; bu yük azaltır). Rozetin kendi rengi (tür rengi) ve meta'nın soluk rengi kalır.
- **Card-table satırı:** `badge` = tür, `meta` = "Stüdyo · Yıl". Başlık ile card-table verisi **birebir aynı** olmalı.
- **GFN tabloları:** oyunun türü + stüdyosu + çıkış yılı tabloda da bulunsun ("Tür" sütunu + stüdyo/yıl), platform/eklenme bilgisini koruyarak.
- **Çıkış yılı yoksa** (yeni duyurulan oyun) dönem/ifade yaz: "2027 (beklenen)", "Sonbahar 2026", "Belirsiz", "Yayında". Stüdyo bilinmiyorsa yayıncıyı yaz.
- **Ayraç:** orta nokta " · " (ör. "Vicarious Visions · 2017", "Santa Monica · 2027 (beklenen)").
- **Tür taksonomisi kural 5 ile tutarlı.** (Tematik istisna: tekno-tanıtımda rozet türün yerine temayı gösterebilir, ör. DLSS açıklayıcısında "DLSS"/"RAY TRACING"; stüdyo · yıl yine bulunur.)

## 12. Tür rozeti → GFN kategorisine iç link
Tür rozeti markanın **linklenebilir GFN kategorilerinden** birine fit ediyorsa, rozet o kategori sayfasına iç link olur (`category_url_for(badge)` URL'i döndürür). Linklenebilir kategoriler: `strateji, aksiyon, simulasyon, dovus-oyunu, yaris, fps, mmo, macera, steam, canlandirma, moba, bagimsiz, arcade, bulmaca, basit-eglence, aile-dostu, platform, spor, ubisoft-connect, populer-oyunlar`.
- **Tek/saf rozet → tüm rozet kendi kategorisine** linklenir (ör. saf "Aksiyon" → /aksiyon, "RPG" → /canlandirma). **Birleşik/çift rozette (Aksiyon-Macera, Aksiyon-RPG, Indie-RPG) HER PARÇA AYRI AYRI kendi kategorisine** linklenir: "Aksiyon-Macera" → **Aksiyon** = /gfn/oyunlar/aksiyon + **Macera** = /gfn/oyunlar/macera; eşleşmeyen parça (GFN kategorisi değilse) düz kalır. `render_game_h3_inline(badge_href=None)` (varsayılan) bunu **otomatik** yapar (parça-bazlı `<a color:inherit>`, tek rozette tüm rozet `<a display:contents>`). **`badge_href=False` verirsen rozet hiç linklenmez** — tek-tür seride (ör. hepsi FPS olan Call of Duty) 20+ özdeş /fps linki = stuffing olmaması için bunu kullan. Çok kelimeli tekil kategoriler boşlukla yazıldığından ("Dövüş Oyunu", "Aile Dostu") tek rozet gibi linklenir.
- **DEDUP YOK — aynı yazıda eşleşen HER rozet linklenir.** İki oyunun da rozeti "RPG" ise ikisi de /canlandirma'ya, iki oyun "Aksiyon" ise ikisi de /aksiyon'a linklenir. (Bunlar farklı oyunların rozetleri; bağlamsal gezinme linkidir, link stuffing değil.)
- Rozet linki **yalnızca oyun başlığında** verilir (`render_game_h3_inline(..., badge_href=url)`). **Card-table indeksi ve master tabloda kategori linki VERİLMEZ** — card-table satırı zaten bölüme jump-link (iç içe `<a>` geçersiz), liste/tabloda kategori linki istenmiyor.
- GFN'de karşılığı olmayan türler (KORKU, SOULSLIKE, METROIDVANIA, HAYATTA KALMA vb.) **düz rozet** kalır.
- İç link; `nofollow`/`target=_blank` YOK. Görünüm değişmez (rozet aynı, sadece `<a>` ile sarılı; `display:contents` sayesinde linksiz rozetle birebir aynı yükseklik/yerleşim).

### Build script deseni (dedup yok)
```python
# Saf rozet -> kategori URL'i; birleşik/eşleşmeyen -> None (category_url_for birleşiği zaten eler).
for (name, badge, color, meta, vid) in games:
    inline = render_game_h3_inline(anchor, name, badge, color, meta, level=lvl)  # badge_href=None (otomatik)
```

## 13. Çıktı kontrolü (tutarlılık — her build'in SON adımı, zorunlu)
Her yazının **aynı iskeletle** çıkması kritik. Build'in en sonunda final body üzerinde otomatik kontrol çalıştır:
```python
from gameplus_blog_components import verify_output, print_report
res = verify_output(final_body, blog_type="general", n_games=12, expect_faq=True)  # GFN: blog_type="gfn"
print_report(res)        # FAIL varsa TESLİM ETME, düzelt
```
`verify_output` programatik olarak şunları doğrular: **tek H1 + ilk başlık H1**, **meta header yok**, ANIMATED_BORDER_STYLE 1x, **em dash yok**, floating ToC + TLDR (3-6 madde) + info-card var, (`expect_faq`) FAQ accordion, (`n_games` verildiyse) **inline oyun başlığı = card-row = oyun sayısı** (düz `<hN>Oyun</hN>` kalmamış), YouTube embed `aspect-ratio` (kare-bug yok), PlayStation uyarısı. **FAIL = çıktı kuralı ihlali.** WARN = bağlama göre değerlendir.

Yargı gerektiren (otomatik kontrol edilemeyen) maddeler için **`references/qa-checklist.md`**'yi gözden geçir: yazarın cümleleri korunmuş mu, her oyun inline başlık + doğru tür/stüdyo/yıl taşıyor mu, tür taksonomisi tutarlı mı, CTA dürüstlüğü, lisans hatırlatması, GFN tarih sütununda "-" kuralı, PlayStation bağlamı.
