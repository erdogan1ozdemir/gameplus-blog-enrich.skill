# Çıktı Kontrol Listesi (teslim öncesi — her yazıda)

Amaç: **her blog yazısının aynı iskelet ve aynı kurallarla** çıkması. Bir kısmı otomatik
(`verify_output`), bir kısmı yargı gerektirir (aşağıdaki manuel maddeler). Build'in son adımında
otomatik kontrolü çalıştır, sonra manuel maddeleri gözden geçir. **FAIL varsa teslim etme.**

## 1. Otomatik kontrol (zorunlu — build'in SON adımı)

```python
from gameplus_blog_components import verify_output, print_report
res = verify_output(final_body, blog_type="general", n_games=12, expect_faq=True)  # GFN: blog_type="gfn"
ok  = print_report(res)   # FAIL yoksa True
```

`verify_output` şunları doğrular (FAIL = ihlal, WARN = bağlama göre bak):

| Kontrol | Beklenen |
|---|---|
| Tek H1 + ilk başlık H1 | Gövde tek bir H1 ile başlar (ilk başlık = yazı başlığı) |
| Meta header yok | `render_meta` çıktısı (article-meta) gövdede YOK |
| ANIMATED_BORDER_STYLE | tam 1 kez, en başta |
| Em dash yok | `—` hiç geçmez |
| Floating ToC | var |
| TLDR | var, **3-6 madde** |
| Info-card | var (genel blog + GFN) |
| FAQ accordion | `expect_faq=True` ise var |
| Oyun sayısı | `n_games` verildiyse: inline başlık = card-row = n_games |
| Embed | `youtube.com/embed` varsa `aspect-ratio` var, padding-% hack yok (WARN) |
| PlayStation | geçiyorsa WARN (GFN platform/lisans/CTA bağlamında olmamalı) |

## 2. Manuel kontrol (yargı gerektirir — otomatik değil)

### İçerik bütünlüğü
- [ ] **Yazarın cümleleri DEĞİŞMEDİ** — sadece enrichment eklendi (TLDR/CTA/FAQ/editör notu yeni cümle; gövde metni aynen).
- [ ] Mevcut linkler ve YouTube embed'leri korundu (silinmedi, değişmedi).
- [ ] Em dash yok; yerine nokta/virgül (otomatik yakalar ama prozada kontrol et).

### Başlık / yapı
- [ ] Gövde **H1 ile başlıyor** (yazı başlığı). Bölüm başlıkları H2/H3. Tek H1.
- [ ] **Üst meta header / tarih-marka chip'i YOK** (site zaten gösteriyor).

### Oyun giriş formatı (yazıda >1 oyun varsa — content-rules 11)
- [ ] Her oyunun başlığı `render_game_h3_inline` ile: **tür rozeti + isim + "Stüdyo · Yıl"**. Düz `<hN>Oyun</hN>` kalmadı.
- [ ] Başlık metnine renk atanmadı (CMS verir).
- [ ] Card-table satırı ile başlık verisi **birebir aynı** (tür + Stüdyo · Yıl).
- [ ] Yıl yoksa dönem ("2027 (beklenen)", "Belirsiz", "Yayında").

### Tür taksonomisi (content-rules 5/12)
- [ ] Tür adları **GFN kategorileriyle** uyumlu (oyun GFN'deyse). Aynı yazıda **tutarlı** (RE2 ve RE4 ikisi de "KORKU").
- [ ] Tek/saf rozet kendi kategorisine link; **birleşik rozet (AKSİYON-MACERA) her parça ayrı** linklenir; GFN'de olmayan tür (KORKU, SOULSLIKE…) düz kalır.
- [ ] Tek-tür seride (hepsi FPS) link stuffing önlemek için `badge_href=False`.

### CTA & lisans (content-rules 2/3/4)
- [ ] **CTA dürüstlüğü:** "tüm oyunlara erişebilirsin" YOK; "satın aldığın / kütüphanendeki / GFN destekli yapımlar" var.
- [ ] **Lisans hatırlatması** var: GFN oyun satmaz, ilgili platformda lisans gerekir.
- [ ] **PlayStation Store / PSN geçmiyor** (GFN desteklemez). Desteklenen platformlar: Steam · Epic · Xbox/Game Pass · Ubisoft Connect · GOG · EA App · Battle.net · Wargaming.
- [ ] Genel blog: CTA Paketler + dual End (CTA Oyunlar opsiyonel). GFN: tek End + 1 compact featured CTA.

### GFN Thursday'e özel
- [ ] Oyun listeleri **gerçek tablo** (`render_table`), card-table değil.
- [ ] **Tarih sütunu:** kaynakta tarih yoksa **"-"** ("Bu hafta eklendi" gibi belirsiz ifade yazma).
- [ ] Info-card metrikleri haftaya göre (yeni oyun yoksa "0" gösterme; DLC/sezon/güncelleme/geri dönen).
- [ ] "Önceki Haftalarda" bölümü en altta (End CTA'dan sonra).

### Görsel / teknik
- [ ] Görsel alt text / caption / JSON-LD **eklenmedi** (kullanıcı istemiyor).
- [ ] YouTube embed'ler 16:9 (`aspect-ratio`), kare görünmüyor.
- [ ] Önizleme (`files-preview`) tarayıcıda kontrol edildi (card-table hizası, uzun rozet kırpılmıyor, mobil).

## 3. Çıktı
- [ ] **İki çıktı** üretildi: `files-preview` (GreycliffCF gömülü) + `excel` rollup. (Kullanıcı tersini demedikçe ikisi de.)
