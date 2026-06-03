"""
Gameplus Blog Enrichment — Component Library
=============================================
Pure, reusable HTML component renderers for enriching gameplus.com.tr blog posts.
Final design (v9): dark theme (#000 bg), Turkish genre tags, trophy icon,
V8 rotating-conic-glow (TLDR/CTA outer), V9 layered frame (Hatırlatma/Editör/tables/card-table/compact CTA),
Controller-Tag compact CTA, Hover-Slide card-table rows, pulsing FAQ "+".

Import this module from a per-blog build script:
    from gameplus_blog_components import *
Then call render_*() to get HTML strings, assemble, and write out.

All components use inline CSS so they survive CMS paste. The one <style> block
(ANIMATED_BORDER_STYLE) must be prepended ONCE to the final body.
"""
import re
import json

# === HTML Wrapper ===
PAGE_HEAD = '''<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>__TITLE__</title>
<style>
  /* Önizleme tipografisi gameplus.com.tr blog ile bire bir (GreycliffCF, 20px gövde, 1200px kolon). Yalnızca önizleme; CMS gövdesi etkilenmez. */
  @font-face { font-family:'GreycliffCF'; font-style:normal; font-weight:400; font-display:swap; src:url('https://gameplus.com.tr/_next/static/media/GreycliffCF-Regular.55993c60.otf') format('opentype'); }
  @font-face { font-family:'GreycliffCF'; font-style:normal; font-weight:500; font-display:swap; src:url('https://gameplus.com.tr/_next/static/media/GreycliffCF-Medium.b24079d5.woff2') format('woff2'); }
  @font-face { font-family:'GreycliffCF'; font-style:normal; font-weight:700; font-display:swap; src:url('https://gameplus.com.tr/_next/static/media/GreycliffCF-Bold.d881132f.woff2') format('woff2'); }
  * { box-sizing: border-box; }
  body { font-family: GreycliffCF, -apple-system, "system-ui", "Segoe UI", Roboto, Oxygen, Ubuntu, Cantarell, "Fira Sans", "Droid Sans", "Helvetica Neue", sans-serif; max-width: 1200px; margin: 0 auto; padding: 28px 20px 80px; color: #b2b2b2; font-size: 20px; line-height: 1.5; background: #000; }
  h1 { font-size: 40px; font-weight: 500; line-height: 1.15; margin: 0 0 6.5px; color: #fff; }
  h2 { font-size: 32px; font-weight: 500; line-height: 1.2; margin: 24px 0 6.5px; color: #fff; }
  h3 { font-size: 22.75px; font-weight: 500; line-height: 1.25; margin: 18px 0 6.5px; color: #fff; }
  h4 { font-size: 20px; font-weight: 500; line-height: 1.3; margin: 14px 0 6.5px; color: #fff; }
  p { margin: 0 0 13px; color: #b2b2b2; }
  ul, ol { margin: 0 0 13px; padding-left: 24px; color: #b2b2b2; }
  li { margin: 4px 0; }
  ul li p, ol li p { margin: 0; }
  a { color: #a3e635; text-decoration: underline; }
  a:hover { color: #76b900; }
  em { font-style: italic; }
  strong { font-weight: 700; }
  @media (max-width: 700px) {
    body { font-size: 16px; line-height: 1.6; padding: 18px 16px 60px; }
    h1 { font-size: 30px; } h2 { font-size: 24px; } h3 { font-size: 19px; } h4 { font-size: 17px; }
  }
</style>
</head>
<body>
'''
PAGE_FOOT = '\n</body>\n</html>'


def embed_fonts(html):
    """Make a preview self-contained: replace the GreycliffCF gameplus URLs with
    base64 data URIs (gameplus serves fonts WITHOUT CORS, so cross-origin @font-face
    fails on localhost/Vercel). Reads the bundled fonts in scripts/_fonts/."""
    import base64, os
    base = os.path.join(os.path.dirname(__file__), "_fonts")
    mapping = {
        "https://gameplus.com.tr/_next/static/media/GreycliffCF-Regular.55993c60.otf": ("reg.otf", "font/otf"),
        "https://gameplus.com.tr/_next/static/media/GreycliffCF-Medium.b24079d5.woff2": ("med.woff2", "font/woff2"),
        "https://gameplus.com.tr/_next/static/media/GreycliffCF-Bold.d881132f.woff2": ("bold.woff2", "font/woff2"),
    }
    for url, (fn, mime) in mapping.items():
        fp = os.path.join(base, fn)
        if os.path.exists(fp):
            with open(fp, "rb") as f:
                html = html.replace(url, "data:%s;base64,%s" % (mime, base64.b64encode(f.read()).decode()))
    return html

# === SVG ICONS (premium replacements for emoji) ===
# Trophy icon for "Best Of" lists (replaces star)
SVG_TROPHY = '<svg width="24" height="24" viewBox="0 0 24 24" style="vertical-align:-6px;margin-right:10px;flex-shrink:0;"><defs><linearGradient id="gp-grad" x1="0%" y1="0%" x2="100%" y2="0%"><stop offset="0%" stop-color="#76b900"/><stop offset="100%" stop-color="#f59e0b"/></linearGradient></defs><path fill="url(#gp-grad)" d="M19 5h-2V3H7v2H5c-1.1 0-2 .9-2 2v1c0 2.55 1.92 4.63 4.39 4.94.63 1.5 1.98 2.63 3.61 2.96V19H7v2h10v-2h-4v-3.1c1.63-.33 2.98-1.46 3.61-2.96C19.08 12.63 21 10.55 21 8V7c0-1.1-.9-2-2-2zM5 8V7h2v3.82C5.84 10.4 5 9.3 5 8zm14 0c0 1.3-.84 2.4-2 2.82V7h2v1z"/></svg>'
# Green checkmark for TLDR/info-card items
SVG_CHECK_GREEN = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#76b900" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink:0;"><polyline points="20 6 9 17 4 12"/></svg>'
# External link icon (small arrow up-right)
SVG_EXT_LINK = '<svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:1px;margin-left:3px;opacity:0.65;"><path d="M7 17L17 7"/><polyline points="7 7 17 7 17 17"/></svg>'
# Old gradient star (kept for backward compat)
SVG_STAR_GRADIENT = SVG_TROPHY
SVG_DOC = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:-4px;margin-right:8px;flex-shrink:0;"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="9" y1="13" x2="15" y2="13"/><line x1="9" y1="17" x2="15" y2="17"/></svg>'
SVG_BULB = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:-4px;margin-right:8px;flex-shrink:0;"><path d="M9 18h6"/><path d="M10 22h4"/><path d="M15.09 14a5 5 0 1 0-6.18 0c.66.49 1.09 1.27 1.09 2.1V17h4v-.9c0-.83.43-1.61 1.09-2.1z"/></svg>'
SVG_CAL = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:-2px;margin-right:6px;flex-shrink:0;"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>'
SVG_BOOKMARK = '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:-3px;margin-right:8px;flex-shrink:0;"><line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><line x1="3" y1="6" x2="3.01" y2="6"/><line x1="3" y1="12" x2="3.01" y2="12"/><line x1="3" y1="18" x2="3.01" y2="18"/></svg>'
SVG_BOLT = '<svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor" style="vertical-align:-2px;margin-right:6px;flex-shrink:0;"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>'
SVG_NEWS = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:-2px;margin-right:6px;flex-shrink:0;"><path d="M4 22h16a2 2 0 0 0 2-2V4a2 2 0 0 0-2-2H8a2 2 0 0 0-2 2v16a2 2 0 0 1-2 2zm0 0a2 2 0 0 1-2-2v-9c0-1.1.9-2 2-2h2"/><line x1="18" y1="14" x2="10" y2="14"/><line x1="15" y1="18" x2="10" y2="18"/><rect x="10" y="6" width="8" height="4"/></svg>'
SVG_ARROW = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:-2px;margin-left:6px;flex-shrink:0;"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>'

# === DARK THEME BLOCK STYLES (CMS-portable inline) ===
# Common animated border style + mobile responsiveness + FAQ + table fixes
ANIMATED_BORDER_STYLE = '''<style>
@property --gp-conic-angle {
  syntax: '<angle>';
  initial-value: 0deg;
  inherits: false;
}
@keyframes gameplus-border-shimmer {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}
@keyframes gp-rotate-conic {
  to { --gp-conic-angle: 360deg; }
}
@keyframes gp-pulse-plus {
  0%, 100% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.18); opacity: 0.85; }
}
.gp-animated-border { position: relative; border-radius: 12px; padding: 1px; background: linear-gradient(110deg, #76b900 0%, #f59e0b 30%, #76b900 60%, #f59e0b 100%); background-size: 300% 100%; animation: gameplus-border-shimmer 6s ease-in-out infinite; }
.gp-animated-border > .gp-inner { background: transparent; border-radius: 11px; padding: 22px 24px; }
/* V8: Rotating Conic Glow border */
.gp-conic { position: relative; border-radius: 12px; padding: 1.5px; }
.gp-conic::before {
  content:''; position:absolute; inset:0; border-radius:12px; padding:1.5px;
  background: conic-gradient(from var(--gp-conic-angle,0deg), transparent 0deg, var(--gp-glow,#76b900) 60deg, transparent 120deg, transparent 360deg);
  -webkit-mask: linear-gradient(#000 0 0) content-box, linear-gradient(#000 0 0);
  -webkit-mask-composite: xor;
          mask-composite: exclude;
  animation: gp-rotate-conic 6s linear infinite;
  pointer-events: none;
}
.gp-conic > .gp-conic-inner { background:transparent; border-radius:10.5px; position:relative; }
/* V9: Layered Frame */
.gp-layer { position:relative; border-radius:12px; border:1px solid var(--gp-frame,rgba(118,185,0,0.22)); background:transparent; }
.gp-cell { position:relative; border:1px solid rgba(255,255,255,0.08); border-radius:10px; padding:14px 16px; }
.gp-layer::before { content:''; position:absolute; inset:5px; border:1px solid rgba(255,255,255,0.04); border-radius:8px; pointer-events:none; }
/* FAQ + sign pulsing animation */
.faq-item .faq-icon { animation: gp-pulse-plus 2.2s ease-in-out infinite; }
.gp-card-table-inner .card-row:last-child { border-bottom: none !important; }
.gp-card-table-inner .card-row { position: relative; }
.gp-card-table-inner a.card-row { text-decoration: none !important; color: inherit !important; }
/* Hover Slide Accent: colored bar slides in from left on hover (Steam list vibe) */
.gp-card-table-inner .card-row::before { content:''; position:absolute; left:0; top:0; bottom:0; width:0; background:var(--row-c,#76b900); transition:width 0.2s ease; }
.gp-card-table-inner .card-row:hover::before { width:4px; }
.gp-card-table-inner .card-row:hover { background: rgba(255,255,255,0.025) !important; }
.gp-card-table-inner a.card-row:hover .gp-name { color: #fff !important; }
/* Comparison table fixes */
.table-wrap tbody tr:last-child td { border-bottom: none !important; }
.table-wrap table { border-radius: 12px; }
/* FAQ + indicator */
.faq-item .faq-icon { transition: transform 0.25s ease, color 0.2s; }
.faq-item[open] .faq-icon { transform: rotate(45deg); color: #76b900 !important; }
.faq-item summary:hover .faq-icon { color: #f59e0b; }
/* YouTube embed wrapper smaller + centered */
.gp-yt-wrap { max-width: 560px; margin: 1.5em 0 !important; }
/* Mobile: card-table responsive */
@media (max-width: 700px) {
  .gp-card-table-inner .card-row {
    grid-template-columns: auto 1fr !important;
    grid-template-rows: auto auto;
    gap: 6px 12px !important;
    padding: 14px 16px !important;
  }
  .gp-card-table-inner .card-row > .gp-badge {
    grid-row: 1; grid-column: 1;
    font-size: 0.54em !important;
    min-width: auto !important;
    padding: 4px 9px !important;
    letter-spacing: 0.08em !important;
  }
  .gp-card-table-inner .card-row > .gp-name {
    grid-row: 1; grid-column: 2;
    font-size: 0.95em !important;
    align-self: center;
  }
  .gp-card-table-inner .card-row > .gp-meta {
    grid-row: 2; grid-column: 1 / -1;
    text-align: left !important;
    font-size: 0.78em !important;
    padding-left: 0 !important;
  }
  .gp-game-inline > aside { float: none !important; width: 100% !important; margin: 0 0 16px 0 !important; }
  .gp-yt-wrap { margin: 1em 0 !important; }
}

/* ===== v10 genel revizeler: embed 16:9, tablo alt kapatma, kupa ortala, FAQ sol, mobil responsive ===== */
/* ===== YouTube embed: 16:9 (kare değil), sola dayalı, küçük ===== */
.gp-yt-wrap { max-width: 560px; margin: 1.5em 0 !important; }
.gp-yt-wrap iframe { display: block; width: 100% !important; aspect-ratio: 16 / 9 !important; height: auto !important; border: 0; border-radius: 12px; box-shadow: 0 4px 14px rgba(0,0,0,0.5); }

/* ===== Tabloların altını kapat: tek temiz çerçeve, son satır ayracı ===== */
.table-wrap.gp-layer::before,
.card-table.gp-layer::before { display: none !important; }
.table-wrap { border: 1px solid rgba(118,185,0,0.38) !important; }
.gp-card-table-inner { border: 1px solid rgba(118,185,0,0.38) !important; }
.table-wrap tbody tr:last-child td { border-bottom: 1px solid rgba(255,255,255,0.06) !important; }

/* ===== Card-table başlığı (kupa + başlık) tam ortalı ===== */
.card-table-wrap > div:first-child { text-align: center; }
.card-table-wrap h3 { display: flex !important; align-items: center !important; justify-content: center !important; gap: 9px !important; }
.card-table-wrap h3 > svg { margin-right: 0 !important; vertical-align: middle !important; }
.card-table-wrap h3 > span { min-width: 0; }

/* ===== FAQ soruları biraz daha sola dayalı ===== */
.faq-item summary { padding: 14px 16px !important; gap: 10px !important; }

/* ===== MOBİL (<=700px) ===== */
@media (max-width: 700px) {
  /* --- Karşılaştırma tablosu: yatay kaydırma yok, tüm sütunlar görünür, okunur punto --- */
  .table-wrap > div { overflow-x: visible !important; }
  .table-wrap table { font-size: 0.62em !important; table-layout: fixed; width: 100% !important; }
  .table-wrap th, .table-wrap td {
    padding: 8px 7px !important; white-space: normal !important;
    word-break: break-word; overflow-wrap: anywhere; vertical-align: top; line-height: 1.4 !important;
  }
  .table-wrap th { letter-spacing: 0.04em !important; }
  .table-wrap th:nth-child(1), .table-wrap td:nth-child(1) { width: 34%; }
  .table-wrap th:nth-child(2), .table-wrap td:nth-child(2) { width: 26%; }
  .table-wrap th:nth-child(3), .table-wrap td:nth-child(3) { width: 20%; }
  .table-wrap th:nth-child(4), .table-wrap td:nth-child(4) { width: 20%; }

  /* --- Card-table: TEK SATIR + rozet sütunu SABİT (oyun isimleri hizalı) --- */
  .gp-card-table-inner .card-row {
    grid-template-columns: 94px 1fr auto !important;
    grid-template-rows: auto !important;
    gap: 4px 9px !important; padding: 11px 12px !important; align-items: center !important;
  }
  .gp-card-table-inner .card-row > .gp-badge {
    grid-row: 1 !important; grid-column: 1 !important;
    width: 100% !important; min-width: 0 !important; box-sizing: border-box;
    font-size: 0.44em !important; padding: 3px 4px !important; letter-spacing: 0.03em !important; text-align: center;
  }
  .gp-card-table-inner .card-row > .gp-name {
    grid-row: 1 !important; grid-column: 2 !important; font-size: 0.8em !important; line-height: 1.28 !important;
  }
  .gp-card-table-inner .card-row > .gp-meta {
    grid-row: 1 !important; grid-column: 3 !important; text-align: right !important;
    font-size: 0.58em !important; padding-left: 0 !important; white-space: normal !important;
    max-width: 104px; line-height: 1.35 !important;
  }

  /* --- FAQ: soru ve cevap sola dayalı, okunur --- */
  .faq-item summary { padding: 13px 13px !important; gap: 9px !important; font-size: 0.95em !important; }
  .faq-item > div { padding: 12px 14px 15px 14px !important; }

  /* --- Hızlı Özet (TLDR): kompakt ve okunur --- */
  .tldr-block .gp-conic-inner { padding: 15px 15px !important; font-size: 0.85em !important; }
  .tldr-block li { gap: 9px !important; }

  /* --- CTA blokları: kompakt, butonlar tam genişlik --- */
  .cta-end .gp-conic-inner, .cta-paketler .gp-conic-inner, .cta-oyunlar .gp-conic-inner { padding: 18px 16px !important; }
  .cta-end a, .cta-paketler a, .cta-oyunlar a { flex: 1 1 100% !important; justify-content: center !important; box-sizing: border-box; }
  .cta-end .gp-conic-inner > div:last-child { gap: 9px !important; }

  /* --- info-card: 2 sütun --- */
  .info-card { grid-template-columns: repeat(2, 1fr) !important; gap: 10px !important; }
}
</style>
'''

# --- TLDR (V8 conic glow + checkmark items) ---
def render_tldr(items):
    items_html = "\n".join(
        f'    <li style="display:flex;gap:11px;margin:8px 0;list-style:none;align-items:flex-start;line-height:1.5;"><span style="flex-shrink:0;margin-top:3px;">{SVG_CHECK_GREEN}</span><span>{x}</span></li>'
        for x in items
    )
    return f'''<div class="tldr-block gp-conic" style="--gp-glow:#76b900;margin:22px 0;box-shadow:0 4px 20px rgba(0,0,0,0.5);">
  <div class="gp-conic-inner" style="padding:18px 22px;font-size:0.92em;">
    <h3 style="margin:0 0 12px 0;font-size:1em;font-weight:800;letter-spacing:-0.005em;display:flex;align-items:center;color:#76b900;">{SVG_DOC}<span style="color:#fff;">Hızlı Özet</span></h3>
    <ul style="margin:0;padding:0;color:#cbd5e1;list-style:none;">
{items_html}
    </ul>
  </div>
</div>
'''

# --- Info-card (premium compact dark grid OR checkmark feature list) ---
def render_info_card(badges, style="grid"):
    """badges: [(label, value), ...] for grid; or [value, ...] for checkmark mode"""
    if style == "checkmark":
        items = []
        for value in badges:
            items.append(f'<div style="display:flex;align-items:center;gap:11px;margin:8px 0;">{SVG_CHECK_GREEN}<span style="color:#e5e7eb;font-size:0.95em;font-weight:500;">{value}</span></div>')
        return f'''<div class="info-card" style="background:transparent;border:1px solid #1f1f1f;border-radius:12px;padding:16px 22px;margin:18px 0 24px;">
{chr(10).join(items)}
</div>
'''
    # Default grid mode (label + value)
    items = []
    for label, value in badges:
        items.append(f'''  <div class="gp-cell">
    <span style="display:block;font-size:0.62em;color:#76b900;text-transform:uppercase;letter-spacing:0.14em;margin-bottom:5px;font-weight:800;">{label}</span>
    <span style="font-size:1.02em;font-weight:700;color:#fff;letter-spacing:-0.005em;">{value}</span>
  </div>''')
    return f'''<div class="info-card" style="margin:18px 0 24px;display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;">
{chr(10).join(items)}
</div>
'''

# --- Article Meta (date + platform, premium SVG) ---
def render_meta(date, category="GAME+ Blog"):
    return f'''<div class="article-meta" style="display:flex;gap:14px;flex-wrap:wrap;align-items:center;font-size:0.85em;color:#8b95a7;margin:0 0 20px;padding:12px 0;border-bottom:1px solid #1f1f1f;">
  <span style="display:inline-flex;align-items:center;background:transparent;padding:6px 14px;border-radius:999px;color:#fbbf24;font-weight:700;border:1px solid #1f1f1f;letter-spacing:0.02em;">{SVG_BOLT}{category}</span>
  <span style="display:inline-flex;align-items:center;font-weight:500;color:#8b95a7;">{SVG_CAL}{date}</span>
</div>
'''

# --- Editor Note (V9 layered frame, blue) ---
def render_editor_note(text):
    return f'''<div class="editor-note gp-layer" style="--gp-frame:rgba(59,130,246,0.22);margin:22px 0;padding:14px 18px;box-shadow:0 2px 12px rgba(0,0,0,0.4);">
  <div style="position:relative;z-index:1;">
    <div style="display:flex;align-items:center;font-weight:800;margin-bottom:6px;color:#93c5fd;font-size:0.72em;letter-spacing:0.12em;text-transform:uppercase;">{SVG_DOC}Game+ Editör Notu</div>
    <p style="margin:0;color:#cbd5e1;line-height:1.55;font-size:0.94em;">{text}</p>
  </div>
</div>
'''

# --- Highlight (V9 layered frame, amber) ---
def render_highlight(text, title="Hatırlatma"):
    return f'''<div class="highlight-box gp-layer" style="--gp-frame:rgba(245,158,11,0.22);margin:22px 0;padding:14px 18px;box-shadow:0 2px 12px rgba(0,0,0,0.4);">
  <div style="position:relative;z-index:1;">
    <div style="display:flex;align-items:center;font-weight:800;margin-bottom:6px;color:#fbbf24;font-size:0.72em;letter-spacing:0.12em;text-transform:uppercase;">{SVG_BULB}{title}</div>
    <p style="margin:0;color:#fde68a;line-height:1.55;font-size:0.94em;">{text}</p>
  </div>
</div>
'''

# --- CTA Paketler (V8 conic glow + V9 inner faded frame) ---
def render_cta_paketler(headline, desc):
    return f'''<div class="cta-paketler gp-conic" style="--gp-glow:#76b900;margin:30px 0;box-shadow:0 6px 24px rgba(0,0,0,0.55);">
<div class="gp-conic-inner gp-layer" style="--gp-frame:rgba(118,185,0,0.22);padding:22px 24px;">
  <div style="display:flex;align-items:center;gap:10px;margin-bottom:10px;position:relative;z-index:1;">
    <span style="display:inline-block;background:#76b900;color:#fff;padding:4px 11px;border-radius:999px;font-size:0.6em;font-weight:800;letter-spacing:0.12em;text-transform:uppercase;box-shadow:inset 0 1px 0 rgba(255,255,255,0.18);">GeForce NOW</span>
  </div>
  <div style="font-weight:800;font-size:1.2em;margin-bottom:8px;line-height:1.3;color:#fff;letter-spacing:-0.01em;position:relative;z-index:1;">{headline}</div>
  <p style="color:#cbd5e1;margin:0 0 16px 0;line-height:1.55;font-size:0.93em;position:relative;z-index:1;">{desc}</p>
  <a href="https://gameplus.com.tr/gfn/paketler" style="display:inline-flex;align-items:center;background:#76b900;color:#fff;padding:11px 22px;border-radius:6px;font-weight:700;text-decoration:none;letter-spacing:-0.005em;box-shadow:0 2px 8px rgba(118,185,0,0.35);font-size:0.94em;position:relative;z-index:1;">GeForce NOW Paketlerini İncele{SVG_ARROW}</a>
</div>
</div>
'''

# --- CTA Oyunlar (V8 conic + V9 inner faded frame, white tag) ---
def render_cta_oyunlar(headline, desc):
    return f'''<div class="cta-oyunlar gp-conic" style="--gp-glow:#ffffff;margin:30px 0;box-shadow:0 6px 24px rgba(0,0,0,0.55);">
<div class="gp-conic-inner gp-layer" style="--gp-frame:rgba(255,255,255,0.16);padding:22px 24px;">
  <div style="display:flex;align-items:center;gap:10px;margin-bottom:10px;position:relative;z-index:1;">
    <span style="display:inline-block;background:#fff;color:#000;padding:4px 11px;border-radius:999px;font-size:0.6em;font-weight:800;letter-spacing:0.12em;text-transform:uppercase;">Oyun Kütüphanesi</span>
  </div>
  <div style="font-weight:800;font-size:1.2em;margin-bottom:8px;line-height:1.3;color:#fff;letter-spacing:-0.01em;position:relative;z-index:1;">{headline}</div>
  <p style="color:#cbd5e1;margin:0 0 16px 0;line-height:1.55;font-size:0.93em;position:relative;z-index:1;">{desc}</p>
  <a href="https://gameplus.com.tr/gfn/oyunlar" style="display:inline-flex;align-items:center;background:#fff;color:#000;padding:11px 22px;border-radius:6px;font-weight:700;text-decoration:none;letter-spacing:-0.005em;font-size:0.94em;position:relative;z-index:1;">GeForce NOW Oyunlarını Keşfet{SVG_ARROW}</a>
</div>
</div>
'''

# --- End CTA Dual (V8 conic + V9 inner faded frame) ---
def render_end_cta(headline, desc, btn2_label="Güncel Fırsatlar", btn2_url="https://gameplus.com.tr/firsatlar", chip2="Fırsatlar"):
    return f'''<div class="cta-end gp-conic" style="--gp-glow:#76b900;margin:40px 0 24px;box-shadow:0 6px 28px rgba(0,0,0,0.6);">
<div class="gp-conic-inner gp-layer" style="--gp-frame:rgba(118,185,0,0.22);padding:28px 30px;">
  <div style="display:flex;align-items:center;gap:14px;margin-bottom:14px;flex-wrap:wrap;position:relative;z-index:1;">
    <div style="font-size:1.15em;font-weight:800;color:#fff;letter-spacing:-0.015em;">
      GeForce <span style="color:#76b900;">NOW</span>
    </div>
    <div style="height:18px;width:1px;background:#2a2a2a;"></div>
    <div style="display:flex;gap:8px;flex-wrap:wrap;">
      <span style="color:#76b900;font-weight:700;font-size:0.66em;padding:4px 10px;border:1px solid #76b900;border-radius:4px;letter-spacing:0.12em;text-transform:uppercase;">Paketler</span>
      <span style="color:#f59e0b;font-weight:700;font-size:0.66em;padding:4px 10px;border:1px solid #f59e0b;border-radius:4px;letter-spacing:0.12em;text-transform:uppercase;">{chip2}</span>
    </div>
  </div>
  <div style="font-size:1.32em;font-weight:800;margin-bottom:8px;line-height:1.3;color:#fff;letter-spacing:-0.015em;position:relative;z-index:1;">{headline}</div>
  <p style="color:#cbd5e1;margin:0 0 18px 0;line-height:1.55;font-size:0.93em;position:relative;z-index:1;">{desc}</p>
  <div style="display:flex;flex-wrap:wrap;gap:10px;position:relative;z-index:1;">
    <a href="https://gameplus.com.tr/gfn/paketler" style="display:inline-flex;align-items:center;background:#76b900;color:#fff;padding:11px 22px;border-radius:6px;font-weight:700;text-decoration:none;font-size:0.93em;box-shadow:0 2px 8px rgba(118,185,0,0.35);letter-spacing:-0.005em;">GeForce NOW Paketleri{SVG_ARROW}</a>
    <a href="{btn2_url}" style="display:inline-flex;align-items:center;background:transparent;color:#fff;padding:10px 21px;border-radius:6px;font-weight:700;text-decoration:none;font-size:0.93em;border:1px solid #f59e0b;letter-spacing:-0.005em;">{btn2_label}{SVG_ARROW}</a>
  </div>
</div>
</div>
'''

# --- Ubisoft+ CTA (premium Ubisoft blue, SVG arrow) ---
def render_ubisoft_cta(headline, desc):
    return f'''<div class="cta-ubisoft" style="background:transparent;border:1px solid #1f1f1f;border-left:3px solid #0061ff;border-radius:10px;padding:22px 24px;margin:30px 0;box-shadow:0 2px 12px rgba(0,0,0,0.4);">
  <div style="display:flex;align-items:center;gap:10px;margin-bottom:10px;">
    <span style="display:inline-block;background:#0061ff;color:#fff;padding:4px 11px;border-radius:999px;font-size:0.6em;font-weight:800;letter-spacing:0.12em;text-transform:uppercase;box-shadow:inset 0 1px 0 rgba(255,255,255,0.18);">Ubisoft+</span>
  </div>
  <div style="font-weight:800;font-size:1.2em;margin-bottom:8px;line-height:1.3;color:#fff;letter-spacing:-0.01em;">{headline}</div>
  <p style="color:#cbd5e1;margin:0 0 16px 0;line-height:1.55;font-size:0.93em;">{desc}</p>
  <a href="https://gameplus.com.tr/ubisoft/paketler" style="display:inline-flex;align-items:center;background:#0061ff;color:#fff;padding:11px 22px;border-radius:6px;font-weight:700;text-decoration:none;letter-spacing:-0.005em;font-size:0.94em;box-shadow:0 2px 8px rgba(0,97,255,0.4);">Ubisoft+ Paketlerini İncele{SVG_ARROW}</a>
</div>
'''

# --- Comparison Table (premium dark, refined borders) ---
def render_table(headers, rows):
    """V9 layered frame — soft outer color border + faint inner stroke, zebra striping."""
    th = "".join(f'<th style="padding:14px 18px;text-align:left;border-bottom:1px solid rgba(118,185,0,0.18);font-weight:800;background:transparent;color:#76b900;font-size:0.98em;letter-spacing:0.06em;text-transform:uppercase;">{h}</th>' for h in headers)
    body_rows = []
    for i, row in enumerate(rows):
        is_last = (i == len(rows) - 1)
        row_bg = 'background:rgba(255,255,255,0.015);' if i % 2 == 0 else ''
        bottom = '' if is_last else 'border-bottom:1px solid rgba(255,255,255,0.04);'
        tds = "".join(f'<td style="padding:11px 18px;vertical-align:top;{bottom}{row_bg}color:#cbd5e1;line-height:1.5;font-size:0.92em;">{c}</td>' for c in row)
        body_rows.append(f'<tr>{tds}</tr>')
    return f'''<div class="table-wrap gp-layer" style="--gp-frame:rgba(118,185,0,0.22);margin:22px 0;box-shadow:0 4px 18px rgba(0,0,0,0.5);overflow:hidden;">
  <div style="overflow-x:auto;position:relative;z-index:1;">
    <table style="width:100%;border-collapse:collapse;background:transparent;">
      <thead><tr>{th}</tr></thead>
      <tbody>
{chr(10).join(body_rows)}
      </tbody>
    </table>
  </div>
</div>
'''

# --- Compact featured-game CTA (Controller Tag — gamepad icon + "ÖNE ÇIKAN" label) ---
def render_compact_cta(game_name, tagline, button_label, button_url):
    gamepad = '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#76b900" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink:0;"><line x1="6" y1="11" x2="10" y2="11"/><line x1="8" y1="9" x2="8" y2="13"/><line x1="15" y1="12" x2="15.01" y2="12"/><line x1="18" y1="10" x2="18.01" y2="10"/><rect x="2" y="6" width="20" height="12" rx="6"/></svg>'
    return f'''<div class="cta-compact" style="border-radius:12px;border:1px solid rgba(118,185,0,0.22);background:linear-gradient(90deg, rgba(118,185,0,0.06), transparent 40%), #000;padding:14px 18px;margin:24px auto;max-width:760px;box-shadow:0 2px 12px rgba(0,0,0,0.4);">
<div style="display:flex;align-items:center;justify-content:space-between;gap:16px;flex-wrap:wrap;">
  <div style="display:flex;align-items:center;gap:14px;flex:1;min-width:240px;">
    {gamepad}
    <div>
      <div style="font-size:0.6em;color:#76b900;font-weight:800;letter-spacing:0.16em;text-transform:uppercase;margin-bottom:3px;">★ Öne Çıkan</div>
      <div style="font-weight:800;color:#fff;font-size:0.98em;letter-spacing:-0.01em;line-height:1.3;">{game_name}</div>
      <div style="font-size:0.8em;color:#9ca3af;line-height:1.4;margin-top:2px;">{tagline}</div>
    </div>
  </div>
  <a href="{button_url}" style="display:inline-flex;align-items:center;background:#76b900;color:#fff;padding:9px 18px;border-radius:6px;font-weight:700;text-decoration:none;font-size:0.85em;letter-spacing:-0.005em;white-space:nowrap;box-shadow:0 2px 8px rgba(118,185,0,0.35);">{button_label}{SVG_ARROW}</a>
</div>
</div>
'''

# --- Steam/Xbox/Epic link helper (adds external icon and clickable wrapping) ---
def linkify_platforms(meta_text, game_name):
    """Wrap Steam/Xbox/Epic/Game Pass mentions with search links + ext icon."""
    import urllib.parse
    q = urllib.parse.quote(game_name)
    platforms = {
        'Steam': f'https://store.steampowered.com/search/?term={q}',
        'Xbox': f'https://www.xbox.com/en-US/games/search?q={q}',
        'Epic Games Store': f'https://store.epicgames.com/en-US/browse?q={q}&sortBy=relevancy',
        'Epic Games': f'https://store.epicgames.com/en-US/browse?q={q}&sortBy=relevancy',
        'Game Pass': f'https://www.xbox.com/en-US/xbox-game-pass/games?q={q}',
    }
    out = meta_text
    for label, url in platforms.items():
        link = f'<a href="{url}" target="_blank" rel="nofollow noopener" style="color:inherit;text-decoration:none;border-bottom:1px dotted rgba(255,255,255,0.3);">{label}{SVG_EXT_LINK}</a>'
        # Replace only whole-word matches (so "Steam, Xbox" doesn't break)
        import re as _re
        out = _re.sub(r'\b' + _re.escape(label) + r'\b(?![^<]*</a>)', link, out, count=1)
    return out

# --- Helper: rgba from hex (for tag tints) ---
def hex_to_rgba(hex_color, alpha):
    h = hex_color.lstrip('#')
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f'rgba({r},{g},{b},{alpha})'

# --- Card-Table: compact rows with text-like tags ---
def render_card_table(title, games):
    """games: list of {name, badge, badge_color, meta, anchor (optional)}"""
    rows = []
    for g in games:
        color = g.get("badge_color", "#76b900")
        tint = hex_to_rgba(color, 0.10)
        border = hex_to_rgba(color, 0.30)
        badge_html = ''
        if g.get('badge'):
            badge_html = f'<span class="gp-badge" style="display:inline-block;color:{color};background:{tint};border:1px solid {border};padding:3px 10px;border-radius:4px;font-size:0.62em;font-weight:800;letter-spacing:0.14em;white-space:nowrap;min-width:120px;text-align:center;text-transform:uppercase;">{g["badge"]}</span>'
        meta_html = ''
        if g.get('meta'):
            meta_html = f'<div class="gp-meta" style="color:#8b95a7;font-size:0.78em;text-align:right;white-space:nowrap;font-weight:500;letter-spacing:0.01em;">{g["meta"]}</div>'
        name_html = f'<div class="gp-name" style="font-weight:600;color:#f3f4f6;font-size:0.98em;letter-spacing:-0.005em;transition:color 0.2s;">{g["name"]}</div>'
        # If anchor provided, make row a clickable anchor link
        if g.get('anchor'):
            row_tag = 'a'
            attrs = f' href="#{g["anchor"]}"'
        else:
            row_tag = 'div'
            attrs = ''
        rows.append(f'''  <{row_tag} class="card-row"{attrs} style="--row-c:{color};display:grid;grid-template-columns:140px 1fr auto;gap:14px;padding:8px 18px;border-bottom:1px solid rgba(255,255,255,0.04);align-items:center;transition:background 0.2s ease;text-decoration:none;color:inherit;">
    {badge_html}
    {name_html}
    {meta_html}
  </{row_tag}>''')
    return f'''<div class="card-table-wrap" style="margin:28px 0;">
  <div style="text-align:center;margin-bottom:14px;">
    <h3 style="display:inline-flex;align-items:center;justify-content:center;font-size:1.3em;font-weight:800;letter-spacing:-0.01em;margin:0;">
      {SVG_TROPHY}<span style="background:linear-gradient(110deg,#76b900,#f59e0b);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">{title}</span>
    </h3>
  </div>
  <div class="card-table gp-layer gp-card-table-inner" style="--gp-frame:rgba(118,185,0,0.22);overflow:hidden;box-shadow:0 4px 18px rgba(0,0,0,0.5);">
    <div style="position:relative;z-index:1;">
{chr(10).join(rows)}
    </div>
  </div>
</div>
'''

# --- Game H3 with inline tag + studio metadata (matches card-table style) ---
def render_game_h3_inline(anchor, name, badge, badge_color, meta_text):
    tint = hex_to_rgba(badge_color, 0.10)
    border = hex_to_rgba(badge_color, 0.30)
    return f'''<h3 id="{anchor}" style="display:flex;flex-wrap:wrap;align-items:center;gap:12px;margin:32px 0 14px;font-size:1.18em;line-height:1.4;">
  <span style="display:inline-block;color:{badge_color};background:{tint};border:1px solid {border};padding:3px 10px;border-radius:4px;font-size:0.5em;font-weight:800;letter-spacing:0.14em;text-transform:uppercase;white-space:nowrap;">{badge}</span>
  <span style="color:#fff;font-weight:700;letter-spacing:-0.01em;">{name}</span>
  <span style="font-size:0.52em;color:#8b95a7;font-weight:500;letter-spacing:0.02em;flex-basis:100%;margin-top:-4px;">{meta_text}</span>
</h3>'''

# --- Inline Game Card (small, premium, in game description section) ---
def render_inline_game_card(name, badge, badge_color, meta_lines):
    """Small card to be floated alongside game description text."""
    meta_html = '<br>'.join(meta_lines)
    return f'''<aside class="gp-game-info-card" style="float:right;width:210px;margin:0 0 16px 22px;background:transparent;border:1px solid #1f1f1f;border-radius:10px;padding:16px;font-size:0.9em;box-shadow:0 4px 12px rgba(0,0,0,0.5),inset 0 1px 0 rgba(255,255,255,0.04);">
  <span style="display:inline-block;background:{badge_color};color:#fff;padding:4px 11px;border-radius:999px;font-size:0.62em;font-weight:800;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:10px;box-shadow:inset 0 1px 0 rgba(255,255,255,0.18),0 2px 4px rgba(0,0,0,0.4);">{badge}</span>
  <div style="font-weight:700;color:#fff;font-size:1.04em;line-height:1.3;margin-bottom:8px;letter-spacing:-0.01em;">{name}</div>
  <div style="color:#8b95a7;font-size:0.82em;line-height:1.55;font-weight:500;">{meta_html}</div>
</aside>
'''

# --- Previous Weeks Card Grid (thin soft border, no harsh corners) ---
def render_prev_weeks_cards(items):
    cards = []
    for item in items:
        cards.append(f'''  <a href="{item["url"]}" class="gp-prev-week" style="display:block;text-decoration:none;background:transparent;border:1px solid rgba(255,255,255,0.05);border-radius:14px;padding:16px 18px;color:inherit;transition:border-color 0.25s,transform 0.25s,box-shadow 0.25s;">
    <div style="display:flex;align-items:center;font-size:0.58em;color:#76b900;font-weight:800;letter-spacing:0.16em;text-transform:uppercase;margin-bottom:10px;">{SVG_NEWS}GFN Thursday</div>
    <div style="font-weight:700;color:#fff;font-size:1.02em;margin-bottom:6px;letter-spacing:-0.01em;">{item["date"]}</div>
    <div style="font-size:0.82em;color:#8b95a7;font-weight:500;line-height:1.5;">{item["label"]}</div>
  </a>''')
    return f'''<div class="prev-weeks-grid" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px;margin:20px 0 28px;">
{chr(10).join(cards)}
</div>
<style>
  .gp-prev-week:hover {{ border-color: rgba(118,185,0,0.35) !important; transform: translateY(-2px); box-shadow: 0 6px 20px rgba(0,0,0,0.5); }}
</style>
'''

# --- Floating ToC (premium dark, SVG bookmark icon, soft frame) ---
def render_floating_toc(items):
    li_items = []
    for level, text, anchor in items:
        indent = '18px' if level == 3 else '4px'
        font_size = '0.86em' if level == 3 else '0.95em'
        weight = '500' if level == 3 else '600'
        li_items.append(f'    <li style="margin:8px 0;padding-left:{indent};font-size:{font_size};list-style:none;"><a href="#{anchor}" onclick="this.closest(\'details\').removeAttribute(\'open\')" style="color:#cbd5e1;text-decoration:none;font-weight:{weight};letter-spacing:-0.005em;">{text}</a></li>')
    return f'''<details class="floating-toc" style="position:fixed;top:120px;right:0;z-index:100;max-width:300px;border:1px solid #2a2a2a;border-right:none;border-radius:12px 0 0 12px;background:#000;box-shadow:-6px 6px 24px rgba(0,0,0,0.7);">
  <summary style="display:flex;align-items:center;padding:13px 18px;background:#000;color:#fff;cursor:pointer;font-weight:800;list-style:none;border-radius:12px 0 0 0;user-select:none;letter-spacing:-0.005em;">{SVG_BOOKMARK}<span>İçindekiler</span></summary>
  <ul style="margin:0;padding:14px 18px 14px 12px;font-size:0.88em;max-height:60vh;overflow-y:auto;list-style:none;">
{chr(10).join(li_items)}
  </ul>
</details>
<style>
  .floating-toc:not([open]) {{ border: none !important; background: transparent !important; box-shadow: none !important; }}
  .floating-toc:not([open]) > summary {{ border-radius: 12px 0 0 12px !important; box-shadow: -4px 4px 14px rgba(0,0,0,0.6); border: 1px solid #2a2a2a; border-right: none; background: #000 !important; }}
  .floating-toc summary::-webkit-details-marker {{ display: none; }}
  .floating-toc summary::marker {{ display: none; }}
  .floating-toc ul li a:hover {{ color: #76b900 !important; }}
  @media (max-width: 900px) {{
    .floating-toc {{ top: auto !important; bottom: 16px !important; max-width: 240px !important; }}
  }}
</style>
'''

# --- FAQ Accordion (premium dark, Game+ '+' indicator that rotates) ---
def render_faq_accordion(pairs):
    items = []
    for q, a in pairs:
        items.append(f'''  <details class="faq-item" style="margin-bottom:10px;border:1px solid #1f1f1f;border-radius:10px;overflow:hidden;background:transparent;box-shadow:0 2px 8px rgba(0,0,0,0.4);">
    <summary style="display:flex;align-items:center;gap:14px;padding:16px 20px;cursor:pointer;background:transparent;font-weight:700;color:#f3f4f6;letter-spacing:-0.005em;list-style:none;">
      <span class="faq-icon" style="display:inline-flex;align-items:center;justify-content:center;width:22px;height:22px;flex-shrink:0;color:#fbbf24;font-size:1.5em;font-weight:300;line-height:1;">+</span>
      <span style="flex:1;">{q.strip()}</span>
    </summary>
    <div style="padding:14px 20px 18px 56px;border-top:1px solid #1f1f1f;background:transparent;"><p style="margin:0;color:#cbd5e1;line-height:1.55;font-size:0.94em;">{a.strip()}</p></div>
  </details>''')
    return f'<div class="faq-block" style="margin:24px 0;">\n{chr(10).join(items)}\n</div>'

# --- Slug helper ---
def slugify(text):
    text = text.lower()
    text = re.sub(r'[ığüşöç]', lambda m: {'ı':'i','ğ':'g','ü':'u','ş':'s','ö':'o','ç':'c'}[m.group()], text)
    text = re.sub(r'[^a-z0-9]+', '-', text).strip('-')
    return text[:60]

def inject_heading_ids(html):
    toc_items = []
    def replace_h(match):
        tag = match.group(1)
        text = match.group(2)
        clean = re.sub(r'<[^>]+>', '', text)
        anchor = slugify(clean)
        toc_items.append((int(tag[1]), clean, anchor))
        return f'<{tag} id="{anchor}">{text}</{tag}>'
    new_html = re.sub(r'<(h[23])>(.*?)</\1>', replace_h, html, flags=re.DOTALL)
    return new_html, toc_items


# --- YouTube embed shrink (720px max, centered) ---
def shrink_youtube_embeds(html):
    """Add .gp-yt-wrap class to existing embed divs (CSS caps width to 720px and centers)."""
    return re.sub(
        r'(<!--[^>]*Embed Ba[şs]lang[ıi]c[ıi][^>]*-->)\s*<div style="width: 100%;',
        r'\1\n<div class="gp-yt-wrap" style="width: 100%;',
        html
    )
