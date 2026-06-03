# GreycliffCF fontları (repoya dahil DEĞİL — lisanslı)

`embed_fonts()` önizlemeyi self-contained yapmak için bu klasörde 3 dosya bekler:
`reg.otf` (Regular/400), `med.woff2` (Medium/500), `bold.woff2` (Bold/700).

Bunlar ticari GreycliffCF fontlarıdır; herkese açık repoda yeniden dağıtılmasın diye
commit'lenmez (bkz. .gitignore). Önizleme üretmeden önce 3 dosyayı gameplus font
kaynağından indirip buraya koy. Dosya yoksa embed_fonts() çalışır, önizleme sistem
fontuna düşer.
