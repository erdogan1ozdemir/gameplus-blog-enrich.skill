# .docx'ten Yapı Çıkarma

Blog taslakları genelde `.docx` gelir. Amaç: başlık (H1), bölüm başlıkları (H2/H3), paragraflar, listeler, linkler ve video embed'lerini çıkarıp temiz bir HTML gövdesine çevirmek — **yazarın metnini birebir koruyarak**.

## Yöntem 1 — python-docx (önerilen)
```python
from docx import Document
doc = Document("blog.docx")
for p in doc.paragraphs:
    style = p.style.name          # 'Title','Heading 1','Heading 2','Heading 3','Normal','List Paragraph'
    text  = p.text
    # run-level: p.runs[i].bold / .italic / .hyperlink
```
- `Title` veya ilk `Heading 1` → `<h1>`
- `Heading 2/3` → `<h2>/<h3>`
- `Normal` → `<p>`
- `List Paragraph` (ardışık) → `<ul><li>` grupla
- Bold run → `<strong>`, italic → `<em>`
- Hyperlink → `<a href="…">`

Linkleri çıkarmak için ilişki tablosu gerekebilir:
```python
rels = doc.part.rels
# w:hyperlink r:id → rels[rId].target_ref
```

## Yöntem 2 — Word XML'i doğrudan
`.docx` bir zip. `word/document.xml`'i açıp `<w:hyperlink>` ve `<w:p>` öğelerini parse et. python-docx hyperlink'i atlıyorsa bu daha güvenilir:
```bash
unzip -p blog.docx word/document.xml > /tmp/doc.xml
```

## YouTube / video embed'leri
Yazar genelde embed'i ayrı verir (link veya not olarak: "buraya X videosu"). Orijinal HTML'de zaten responsive embed bloğu varsa onu koru. Yoksa standart blok:
```html
<!-- Responsive YouTube Embed Başlangıcı -->
<div style="width: 100%; aspect-ratio: 16/9; background: #000; overflow: hidden; border-radius: 12px; margin: 1em 0;"><iframe style="width: 100%; height: 100%; object-fit: contain; display: block; background: #000;" title="YouTube video player" src="https://www.youtube.com/embed/VIDEO_ID" width="560" height="315" frameborder="0" allowfullscreen="allowfullscreen"></iframe></div>
<!-- Responsive YouTube Embed Sonu -->
```
`shrink_youtube_embeds()` bunları otomatik `.gp-yt-wrap`'e alır (max 720px, ortalı). Embed yorum işaretleri (`Embed Başlangıcı/Sonu`) regex'in çalışması için önemli — koru.

## anthropic-skills:docx
Karmaşık tablolar, gömülü görseller veya tracked-changes varsa `anthropic-skills:docx` skill'i daha güçlü çıkarım yapar. Basit blog taslakları için python-docx yeterli.

## Sonraki adım
Temiz gövdeyi çıkardıktan sonra `inject_heading_ids()` → ToC, sonra placement-rules.md'ye göre bileşenleri enjekte et.
