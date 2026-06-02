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
GeForce NOW oyun SATMAZ, sadece bulutta ÇALIŞTIRIR. Oynamak için oyunun ilgili platformda (Steam / Epic / Xbox) lisansına sahip olmak gerekir. Hatırlatma (highlight) bloğunda bunu net belirt.

## 4. GFN Thursday CTA sadeliği
- **Tek End CTA yeterli.** İki ayrı CTA bloğu (mid + end) koyma.
- End CTA metni (onaylı):
  > **Başlık:** Game+ ile bulutta oyun keyfine hazır mısın?
  > **Açıklama:** Performance ve Ultimate paketleri kütüphanendeki GeForce NOW destekli yapımları donanım olmadan oynamanı sağlar. 2.000'den fazla oyunu ve GFN Thursday'e eklenen yeni yapımları görmek için hemen kütüphaneye göz at!
  > Butonlar: **Paketler** + **Oyunlar** (Fırsatlar değil).
- Öne çıkan oyun varsa orta kısma **tek satır compact CTA** (Controller-Tag).

## 5. Tür etiketleri (taksonomi)
- Türkçesi yaygın olanı Türkçe yaz: **KORKU** (SURVIVAL/PSİKOLOJİK/UZAY HORROR hepsi tek "KORKU"), **GİZLİLİK** (stealth), **YARIŞ**, **STRATEJİ**, **PLATFORM**, **AKSİYON-MACERA**.
- Terim olarak yerleşmiş İngilizceler kalır: **JRPG, SOULSLIKE, ROGUELIKE, INDIE, FPS, CO-OP**.
- "INDIE" — İ değil I (İngilizce loanword). "CO-OP" (KOOP değil).
- **Aynı yazıda tutarlılık:** Resident Evil 2 ve 4 ikisi de "KORKU" — birine SURVIVAL HORROR, diğerine AKSİYON-KORKU deme. Aynı tür → aynı etiket → aynı renk.

## 6. Yazım / üslup
- **Em dash (—) kullanma.** Nokta veya virgülle böl.
- Dil yazarın diliyle uyumlu olsun (samimi "sen" dili, Gameplus tonu).
- Tarih/breadcrumb gibi alanları yazıya ekleme (CMS otomatik ekliyor). Sadece meta chip'te "Güncellenme: YIL" veya GFN tarihi olur.

## 7. EKLENMEYECEKLER
- Görsel alt text, caption, figure açıklaması **EKLEME**.
- Schema markup / JSON-LD **EKLEME**.
- Bariz/gereksiz info-card alanları koyma (GFN'de "Yayın Tarihi / Kategori" gibi — bunlar zaten belli; GFN'de info-card hiç yok).

## 8. Platform linkleri (GFN card-table)
Eklenen oyunların Steam/Xbox/Epic isimleri `linkify_platforms()` ile arama linkine çevrilir + küçük ↗ ikon. Orijinal yazıda zaten link varsa onu koru.

## 9. Öne çıkarılan oyun (GFN)
Çok öne çıkan bir oyun varsa (haftanın yıldızı) orta kısma compact CTA. Kompakt, tek satır, dar — sayfayı boğmaz.
