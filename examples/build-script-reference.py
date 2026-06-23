# ============================================================================
# REFERANS BUILD SCRIPT (v9 — tam çalışan örnek)
# ============================================================================
# Bu, remake + GFN Thursday yazilarinin TAM assembly/placement ornegidir.
# Bilesen fonksiyonlari burada inline (kanonik hali scripts/gameplus_blog_components.py).
# Yeni blog icin: scripts/build_template.py'yi kopyala (o, kutuphaneyi import eder).
# Bu dosyayi placement/enjeksiyon mantigini gormek icin oku.
# Girdi: /tmp/remake-original.html + /tmp/gfn-thursday-original.html (orijinal taslaklar).
# ============================================================================

"""Enrich blog posts v3 — dark theme compatible blocks, table-style cards, inline cards, animated borders."""
import re
import json
from pathlib import Path

OUT_DIR = Path("/Users/Erdo/Desktop/Claude Projects/Dispatch")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# === HTML Wrapper ===
PAGE_HEAD = '''<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>__TITLE__</title>
<style>
  * { box-sizing: border-box; }
  body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; max-width: 900px; margin: 0 auto; padding: 24px 20px 60px; color: #e5e7eb; line-height: 1.65; background: #000; }
  h1 { font-size: 2.1em; line-height: 1.25; margin: 16px 0 16px; color: #fff; letter-spacing: -0.01em; }
  h2 { font-size: 1.5em; line-height: 1.3; margin: 40px 0 14px; color: #fff; letter-spacing: -0.01em; }
  h3 { font-size: 1.2em; line-height: 1.35; margin: 30px 0 12px; color: #f3f4f6; }
  h4 { font-size: 1.05em; margin: 22px 0 10px; color: #e5e7eb; }
  p { margin: 12px 0; color: #cbd5e1; }
  ul, ol { margin: 14px 0; padding-left: 24px; color: #cbd5e1; }
  li { margin: 6px 0; }
  ul li p, ol li p { margin: 0; }
  a { color: #a3e635; text-decoration: underline; }
  a:hover { color: #76b900; }
  em { font-style: italic; }
  strong { font-weight: 600; color: #f3f4f6; }
</style>
</head>
<body>
'''
PAGE_FOOT = '\n</body>\n</html>'

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
.gp-animated-border > .gp-inner { background: #000; border-radius: 11px; padding: 22px 24px; }
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
.gp-conic > .gp-conic-inner { background:#000; border-radius:10.5px; position:relative; }
/* V9: Layered Frame */
.gp-layer { position:relative; border-radius:12px; border:1px solid var(--gp-frame,rgba(118,185,0,0.22)); background:#000; }
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
.gp-yt-wrap { max-width: 720px; margin: 1.5em auto !important; box-shadow: 0 4px 14px rgba(0,0,0,0.5); }
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
  .gp-yt-wrap { margin: 1em auto !important; }
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
        return f'''<div class="info-card" style="background:#000;border:1px solid #1f1f1f;border-radius:12px;padding:16px 22px;margin:18px 0 24px;box-shadow:0 2px 12px rgba(0,0,0,0.4);">
{chr(10).join(items)}
</div>
'''
    # Default grid mode (label + value)
    items = []
    for label, value in badges:
        items.append(f'''  <div style="padding:2px 0;">
    <span style="display:block;font-size:0.62em;color:#76b900;text-transform:uppercase;letter-spacing:0.14em;margin-bottom:5px;font-weight:800;">{label}</span>
    <span style="font-size:1.02em;font-weight:700;color:#fff;letter-spacing:-0.005em;">{value}</span>
  </div>''')
    return f'''<div class="info-card" style="background:#000;border:1px solid #1f1f1f;border-radius:12px;padding:18px 22px;margin:18px 0 24px;display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:18px;box-shadow:0 2px 12px rgba(0,0,0,0.4);">
{chr(10).join(items)}
</div>
'''

# --- Article Meta — DEPRECATED: üst meta header artık EKLENMEZ (çağırma) ---
def render_meta(date, category="GAME+ Blog"):
    return f'''<div class="article-meta" style="display:flex;gap:14px;flex-wrap:wrap;align-items:center;font-size:0.85em;color:#8b95a7;margin:0 0 20px;padding:12px 0;border-bottom:1px solid #1f1f1f;">
  <span style="display:inline-flex;align-items:center;background:#000;padding:6px 14px;border-radius:999px;color:#fbbf24;font-weight:700;border:1px solid #1f1f1f;letter-spacing:0.02em;">{SVG_BOLT}{category}</span>
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
    return f'''<div class="cta-ubisoft" style="background:#000;border:1px solid #1f1f1f;border-left:3px solid #0061ff;border-radius:10px;padding:22px 24px;margin:30px 0;box-shadow:0 2px 12px rgba(0,0,0,0.4);">
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
    th = "".join(f'<th style="padding:12px 18px;text-align:left;border-bottom:1px solid rgba(118,185,0,0.18);font-weight:800;background:transparent;color:#76b900;font-size:0.65em;letter-spacing:0.16em;text-transform:uppercase;">{h}</th>' for h in headers)
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
    return f'''<aside class="gp-game-info-card" style="float:right;width:210px;margin:0 0 16px 22px;background:#000;border:1px solid #1f1f1f;border-radius:10px;padding:16px;font-size:0.9em;box-shadow:0 4px 12px rgba(0,0,0,0.5),inset 0 1px 0 rgba(255,255,255,0.04);">
  <span style="display:inline-block;background:{badge_color};color:#fff;padding:4px 11px;border-radius:999px;font-size:0.62em;font-weight:800;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:10px;box-shadow:inset 0 1px 0 rgba(255,255,255,0.18),0 2px 4px rgba(0,0,0,0.4);">{badge}</span>
  <div style="font-weight:700;color:#fff;font-size:1.04em;line-height:1.3;margin-bottom:8px;letter-spacing:-0.01em;">{name}</div>
  <div style="color:#8b95a7;font-size:0.82em;line-height:1.55;font-weight:500;">{meta_html}</div>
</aside>
'''

# --- Previous Weeks Card Grid (thin soft border, no harsh corners) ---
def render_prev_weeks_cards(items):
    cards = []
    for item in items:
        cards.append(f'''  <a href="{item["url"]}" class="gp-prev-week" style="display:block;text-decoration:none;background:#000;border:1px solid rgba(255,255,255,0.05);border-radius:14px;padding:16px 18px;color:inherit;transition:border-color 0.25s,transform 0.25s,box-shadow 0.25s;">
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
        items.append(f'''  <details class="faq-item" style="margin-bottom:10px;border:1px solid #1f1f1f;border-radius:10px;overflow:hidden;background:#000;box-shadow:0 2px 8px rgba(0,0,0,0.4);">
    <summary style="display:flex;align-items:center;gap:14px;padding:16px 20px;cursor:pointer;background:#000;font-weight:700;color:#f3f4f6;letter-spacing:-0.005em;list-style:none;">
      <span class="faq-icon" style="display:inline-flex;align-items:center;justify-content:center;width:22px;height:22px;flex-shrink:0;color:#fbbf24;font-size:1.5em;font-weight:300;line-height:1;">+</span>
      <span style="flex:1;">{q.strip()}</span>
    </summary>
    <div style="padding:14px 20px 18px 56px;border-top:1px solid #1f1f1f;background:#000;"><p style="margin:0;color:#cbd5e1;line-height:1.55;font-size:0.94em;">{a.strip()}</p></div>
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

def ensure_leading_h1(html):
    """Gövde TEK bir H1 ile başlar (ilk başlık = yazı başlığı). Taslakta H1 varsa korur;
    yoksa ilk başlığı (h2-h6) H1'e yükseltir. Build'in EN SON adımı. (demote_h1 DEPRECATED.)"""
    if re.search(r'<h1\b', html, flags=re.IGNORECASE):
        return html
    return re.sub(r'<(h[2-6])(\b[^>]*)>(.*?)</\1>',
                  lambda m: f'<h1{m.group(2)}>{m.group(3)}</h1>',
                  html, count=1, flags=re.DOTALL | re.IGNORECASE)

# === REMAKE GAME DATA ===
remake_games_data = {
    'resident-evil-2-remake': {'badge': 'SURVIVAL HORROR', 'badge_color': '#dc2626', 'meta_lines': ['Capcom · 2019', 'RE Engine']},
    'resident-evil-4-remake': {'badge': 'AKSİYON-KORKU', 'badge_color': '#dc2626', 'meta_lines': ['Capcom · 2023', 'RE Engine']},
    'dead-space-remake': {'badge': 'UZAY KORKU', 'badge_color': '#dc2626', 'meta_lines': ['EA Motive · 2023', 'Frostbite']},
    'silent-hill-2-remake': {'badge': 'PSİKOLOJİK KORKU', 'badge_color': '#dc2626', 'meta_lines': ['Bloober Team · 2024', 'Unreal Engine 5']},
    'final-fantasy-vii-remake': {'badge': 'JRPG', 'badge_color': '#7c3aed', 'meta_lines': ['Square Enix · 2020', 'Unreal Engine 4']},
    'final-fantasy-vii-rebirth': {'badge': 'JRPG', 'badge_color': '#7c3aed', 'meta_lines': ['Square Enix · 2024', 'Unreal Engine 4']},
    'demon-s-souls-remake': {'badge': 'SOULSLIKE', 'badge_color': '#525252', 'meta_lines': ['Bluepoint Games · 2020', 'Proprietary']},
    'shadow-of-the-colossus-remake': {'badge': 'AKSİYON-MACERA', 'badge_color': '#0891b2', 'meta_lines': ['Bluepoint Games · 2018', 'Proprietary']},
    'persona-3-reload': {'badge': 'JRPG', 'badge_color': '#7c3aed', 'meta_lines': ['Atlus · 2024', 'Unreal Engine 4']},
    'metal-gear-solid-delta-snake-eater': {'badge': 'STEALTH', 'badge_color': '#16a34a', 'meta_lines': ['Konami · 2025', 'Unreal Engine 5']},
    'the-last-of-us-part-i': {'badge': 'AKSİYON-MACERA', 'badge_color': '#0891b2', 'meta_lines': ['Naughty Dog · 2022', 'Proprietary']},
    'crash-bandicoot-n-sane-trilogy': {'badge': 'PLATFORM', 'badge_color': '#f59e0b', 'meta_lines': ['Vicarious Visions · 2017', 'Alchemy']},
}

# === Build Remake Enriched ===
remake_clean = Path('/tmp/remake-original.html').read_text(encoding='utf-8')
remake_clean, remake_toc = inject_heading_ids(remake_clean)

# Make YouTube embed wrappers smaller + centered
def shrink_youtube_embeds(html):
    """Add .gp-yt-wrap class to existing embed divs (CSS caps width to 720px and centers)."""
    return re.sub(
        r'(<!--[^>]*Embed Ba[şs]lang[ıi]c[ıi][^>]*-->)\s*<div style="width: 100%;',
        r'\1\n<div class="gp-yt-wrap" style="width: 100%;',
        html
    )

remake_clean = shrink_youtube_embeds(remake_clean)

# NOTE: inline game cards REMOVED in v5 — card-table at top serves as clickable index

# Build components
remake_toc_html = render_floating_toc(remake_toc)
remake_tldr = render_tldr([
    "<strong>Remake nedir:</strong> Eski oyunun güncel teknoloji ve modern mekaniklerle baştan inşa edilmesi.",
    "<strong>Remake, Remaster ve Reboot:</strong> Üçü farklı kapsam, remake en derin yeniden yapım.",
    "<strong>En iyi 12 remake:</strong> Resident Evil 2/4, Dead Space, Silent Hill 2, FF VII Remake/Rebirth, Demon's Souls, Shadow of the Colossus, Persona 3 Reload, MGS Delta, TLOU Part I, Crash N. Sane Trilogy.",
    "<strong>Beklenen 5 remake:</strong> AC Black Flag Resynced, God of War Trilogy, Max Payne 1+2, Splinter Cell, Prince of Persia (durdu).",
])
remake_info = render_info_card([
    ("İncelenen Remake", "12 Yapım"),
    ("Beklenen Remake", "5 Yapım"),
    ("Öne Çıkan Stüdyo", "Capcom"),
    ("Türler", "Korku · RPG · Aksiyon"),
])
remake_cta_paketler = render_cta_paketler(
    "Sahip olduğun remake yapımlarını bulutta oyna!",
    "Resident Evil 4 Remake'ten Final Fantasy VII Rebirth'e, satın almış olduğun ve GeForce NOW destekli remake yapımlarını Performance veya Ultimate paketle saniyeler içinde başlatabilirsin."
)
remake_cta_oyunlar = render_cta_oyunlar(
    "GeForce NOW kütüphanesindeki remake'lere göz at!",
    "Kütüphaneye eklenmiş ve sahip olduğun GeForce NOW destekli remake yapımları bulut üzerinden anında oynanabilir. Hangi yapımların desteklendiğini görmek için kütüphaneye bak."
)
remake_editor_1 = render_editor_note(
    "Capcom, RE Engine ile Resident Evil 2, 3 ve 4 remake'lerini ardı ardına yayımladı. Üçü de eleştirmen skorları ve satış rakamlarıyla remake türünün modern referansı haline geldi."
)
remake_editor_2 = render_editor_note(
    "PlayStation Studios'un God of War Greek Trilogy duyurusu PlayStation Blog'da kısa bir paragraf olarak geçti. Geliştirme PS3 dönemi orijinallerini PS5 standartlarına taşıyor; resmi tarih paylaşılana kadar projeler erken aşama kabul edilmeli."
)
remake_highlight = render_highlight(
    "GeForce NOW üzerinden bir remake oynamak için o yapımın Steam, Epic Games, Xbox veya ilgili platformdaki lisansına sahip olman gerekiyor. Bulut sadece çalıştırır, oyun satmaz.",
    "Hatırlatma"
)
remake_end_cta = render_end_cta(
    "Efsane oyunları bulutta yeniden yaşa!",
    "Performance veya Ultimate paketle kütüphanendeki GeForce NOW destekli remake yapımlarını saniyeler içinde başlatabilirsin. Fırsatlar sayfasından da güncel indirim ve kampanyalardan haberdar olabilirsin."
)
remake_ubisoft = render_ubisoft_cta(
    "Ubisoft yapımlarını tek pakette keşfet.",
    "Assassin's Creed serisinden Splinter Cell ve Prince of Persia franchise'larına kadar Ubisoft kataloğu Ubisoft+ aboneliğinde geniş şekilde yer alıyor. Yeni remake yapımları çıkış sonrası bu kataloğun parçası olabilir."
)

# Comparison tables
remake_compare = render_table(
    ["Tip", "Kapsam", "Ne Değişir?", "Örnek"],
    [
        ['<strong>Remake</strong>', 'En geniş', 'Görsel + oynanış + ses + bazen hikaye', 'Resident Evil 4 Remake, FF VII Remake'],
        ['<strong>Remaster</strong>', 'Teknik iyileştirme', 'Çözünürlük, doku, FPS', 'Skyrim Anniversary, Halo MCC'],
        ['<strong>Reboot</strong>', 'Hikaye sıfırlama', 'Karakter, hikaye, evren tamamen yeni', 'God of War (2018), Tomb Raider (2013)'],
    ]
)

remake_upcoming = render_table(
    ["Oyun", "Stüdyo", "Çıkış Durumu"],
    [
        ['<strong>Assassin\'s Creed Black Flag Resynced</strong>', 'Ubisoft', '9 Temmuz 2026'],
        ['<strong>God of War Greek Trilogy Remake</strong>', 'PlayStation Studios', 'Erken geliştirme'],
        ['<strong>Max Payne 1 &amp; 2 Remake</strong>', 'Remedy + Rockstar', 'Resmi tarih yok'],
        ['<strong>Splinter Cell Remake</strong>', 'Ubisoft Toronto', 'Geliştirme aşaması'],
        ['<strong>Prince of Persia: The Sands of Time Remake</strong>', 'Ubisoft', 'Durduruldu (30 Ocak 2026)'],
    ]
)

# Card-table for best remakes — TURKISH TAGS (v6) + CLICKABLE ANCHORS
# KORKU (red, all horror), JRPG (purple), AKSİYON-MACERA (cyan), SOULSLIKE (gray),
# GİZLİLİK (green, stealth Turkish), PLATFORM (orange)
remake_games_v6 = [
    {'name': 'Resident Evil 2 Remake', 'badge': 'KORKU', 'badge_color': '#dc2626', 'meta_short': 'Capcom · 2019 · RE Engine', 'meta_table': 'Capcom · 2019', 'anchor': 'resident-evil-2-remake'},
    {'name': 'Resident Evil 4 Remake', 'badge': 'KORKU', 'badge_color': '#dc2626', 'meta_short': 'Capcom · 2023 · RE Engine', 'meta_table': 'Capcom · 2023', 'anchor': 'resident-evil-4-remake'},
    {'name': 'Dead Space Remake', 'badge': 'KORKU', 'badge_color': '#dc2626', 'meta_short': 'EA Motive · 2023 · Frostbite', 'meta_table': 'EA Motive · 2023', 'anchor': 'dead-space-remake'},
    {'name': 'Silent Hill 2 Remake', 'badge': 'KORKU', 'badge_color': '#dc2626', 'meta_short': 'Bloober Team · 2024 · Unreal Engine 5', 'meta_table': 'Bloober Team · 2024', 'anchor': 'silent-hill-2-remake'},
    {'name': 'Final Fantasy VII Remake', 'badge': 'JRPG', 'badge_color': '#7c3aed', 'meta_short': 'Square Enix · 2020 · Unreal Engine 4', 'meta_table': 'Square Enix · 2020', 'anchor': 'final-fantasy-vii-remake'},
    {'name': 'Final Fantasy VII Rebirth', 'badge': 'JRPG', 'badge_color': '#7c3aed', 'meta_short': 'Square Enix · 2024 · Unreal Engine 4', 'meta_table': 'Square Enix · 2024', 'anchor': 'final-fantasy-vii-rebirth'},
    {'name': "Demon's Souls Remake", 'badge': 'SOULSLIKE', 'badge_color': '#a3a3a3', 'meta_short': 'Bluepoint Games · 2020 · Proprietary', 'meta_table': 'Bluepoint · 2020', 'anchor': 'demon-s-souls-remake'},
    {'name': 'Shadow of the Colossus Remake', 'badge': 'AKSİYON-MACERA', 'badge_color': '#0891b2', 'meta_short': 'Bluepoint Games · 2018 · Proprietary', 'meta_table': 'Bluepoint · 2018', 'anchor': 'shadow-of-the-colossus-remake'},
    {'name': 'Persona 3 Reload', 'badge': 'JRPG', 'badge_color': '#7c3aed', 'meta_short': 'Atlus · 2024 · Unreal Engine 4', 'meta_table': 'Atlus · 2024', 'anchor': 'persona-3-reload'},
    {'name': 'Metal Gear Solid Delta: Snake Eater', 'badge': 'GİZLİLİK', 'badge_color': '#16a34a', 'meta_short': 'Konami · 2025 · Unreal Engine 5', 'meta_table': 'Konami · 2025', 'anchor': 'metal-gear-solid-delta-snake-eater'},
    {'name': 'The Last of Us Part I', 'badge': 'AKSİYON-MACERA', 'badge_color': '#0891b2', 'meta_short': 'Naughty Dog · 2022 · Proprietary', 'meta_table': 'Naughty Dog · 2022', 'anchor': 'the-last-of-us-part-i'},
    {'name': 'Crash Bandicoot N. Sane Trilogy', 'badge': 'PLATFORM', 'badge_color': '#f59e0b', 'meta_short': 'Vicarious Visions · 2017 · Alchemy', 'meta_table': 'Vicarious Visions · 2017', 'anchor': 'crash-bandicoot-n-sane-trilogy'},
]
# Card-table data uses meta_table (shorter); H3 inline uses meta_short (longer with engine)
remake_card_table = render_card_table(
    "En İyi 12 Remake Oyunu",
    [{'name': g['name'], 'badge': g['badge'], 'badge_color': g['badge_color'], 'meta': g['meta_table'], 'anchor': g['anchor']} for g in remake_games_v6]
)

# === Inject components into remake_clean ===
# 1. ToC + TLDR + Info-Card after H1 (meta header YOK)
remake_clean = re.sub(r'(</h1>)', r'\1\n' + remake_toc_html + remake_tldr + remake_info, remake_clean, count=1)

# 2. Comparison table after 2nd paragraph in "Remake, Remaster ve Reboot Arasındaki Fark" section
remake_clean = re.sub(
    r'(Oyunun adı aynı kalsa bile hikaye, karakterlerin motivasyonları ve içinde bulundukları evren tamamen değişebiliyor\.</p>)',
    r'\1\n' + remake_compare, remake_clean, count=1
)

# 3. CTA Paketler before 2nd H2
remake_clean = remake_clean.replace(
    '<h2 id="remake-oyunlarin-gucu-tanidik-hikayeler-yeni-deneyimler">',
    remake_cta_paketler + '<h2 id="remake-oyunlarin-gucu-tanidik-hikayeler-yeni-deneyimler">', 1
)

# 4. Editor Note 1 after Capcom mention
remake_clean = remake_clean.replace(
    'remake konusunda adeta ders niteliğinde bir başarı öyküsü yazıyor.</p>',
    'remake konusunda adeta ders niteliğinde bir başarı öyküsü yazıyor.</p>\n' + remake_editor_1, 1
)

# 5. Replace existing list of best remakes with NOTHING (card-table moves to TOP)
remake_clean = re.sub(
    r'<ul><li><p>Resident Evil 2 Remake</p></li>.*?</ul>',
    '', remake_clean, count=1, flags=re.DOTALL
)

# 5b. INSERT card-table BEFORE first game H3 (resident-evil-2-remake)
# This makes it the index/preview for all detailed game sections below
remake_clean = remake_clean.replace(
    '<h3 id="resident-evil-2-remake">',
    remake_card_table + '<h3 id="resident-evil-2-remake">', 1
)

# 5c. Replace each plain H3 game title with inline format (tag + name + meta_short)
for g in remake_games_v6:
    old_h3 = f'<h3 id="{g["anchor"]}">{g["name"]}</h3>'
    # Handle smart quotes in Demon's Souls Remake (curly apostrophe)
    if "Demon" in g["name"]:
        old_h3 = f'<h3 id="{g["anchor"]}">Demon’s Souls Remake</h3>'
    new_h3 = render_game_h3_inline(g['anchor'], g['name'], g['badge'], g['badge_color'], g['meta_short'])
    if old_h3 in remake_clean:
        remake_clean = remake_clean.replace(old_h3, new_h3, 1)
    else:
        # Try without enclosing — replace just the inner text H3
        pattern = re.compile(rf'<h3 id="{re.escape(g["anchor"])}">[^<]+</h3>', re.UNICODE)
        remake_clean = pattern.sub(new_h3, remake_clean, count=1)

# 6. CTA Oyunlar before MGS Delta H3
remake_clean = remake_clean.replace(
    '<h3 id="metal-gear-solid-delta-snake-eater">',
    remake_cta_oyunlar + '<h3 id="metal-gear-solid-delta-snake-eater">', 1
)

# 7. Beklenen Remake table after intro paragraph
remake_clean = remake_clean.replace(
    '<p>Eski efsanelerle hasret giderdik ama ufukta bekleyen ve heyecanımızı artıran daha pek çok yapım var:</p>',
    '<p>Eski efsanelerle hasret giderdik ama ufukta bekleyen ve heyecanımızı artıran daha pek çok yapım var:</p>\n' + remake_upcoming, 1
)

# 8. Editor Note 2 after God of War section
remake_clean = remake_clean.replace(
    'belirtiliyor.</p><h3 id="max-payne-1-amp-2-remake">',
    'belirtiliyor.</p>\n' + remake_editor_2 + '<h3 id="max-payne-1-amp-2-remake">', 1
)

# 9. Ubisoft+ CTA after PoP section before Diğer Beklenen H3
remake_clean = remake_clean.replace(
    'aktif olarak en çok beklenenler listesinden şimdilik uzaklaştırdı.</p><h3 id="diger-beklenen-ve-konusulan-remakeler">',
    'aktif olarak en çok beklenenler listesinden şimdilik uzaklaştırdı.</p>\n' + remake_ubisoft + '<h3 id="diger-beklenen-ve-konusulan-remakeler">', 1
)

# 10. Highlight before "Yeni nesil grafikler"
remake_clean = remake_clean.replace(
    '<p>Yeni nesil grafikler her sistemle dost olmayabilir',
    remake_highlight + '<p>Yeni nesil grafikler her sistemle dost olmayabilir', 1
)

# 11. FAQ accordion
faq_h2 = '<h2 id="sikca-sorulan-sorular">Sıkça Sorulan Sorular</h2>'
faq_idx = remake_clean.find(faq_h2)
if faq_idx != -1:
    after = faq_idx + len(faq_h2)
    rest = remake_clean[after:]
    pairs = re.findall(r'<h3 id="[^"]*">(.*?)</h3>\s*<p>(.*?)</p>', rest, re.DOTALL)
    if pairs:
        accordion = render_faq_accordion(pairs)
        first_h3 = rest.find('<h3 id=')
        last_p_end = 0
        for m in re.finditer(r'</p>', rest):
            last_p_end = m.end()
        if first_h3 != -1 and last_p_end > first_h3:
            faq_content = rest[first_h3:last_p_end]
            new_rest = rest.replace(faq_content, accordion, 1)
            remake_clean = remake_clean[:after] + new_rest

# 12. End CTA before SSS H2
remake_clean = remake_clean.replace(faq_h2, remake_end_cta + faq_h2, 1)

# Prepend animated border styles
remake_clean = ensure_leading_h1(remake_clean)  # gövde tek bir H1 ile başlar (ilk başlık)
remake_final_body = ANIMATED_BORDER_STYLE + remake_clean

# Write body-only version
(OUT_DIR / 'ornek-blog-remake-v9-body-only.html').write_text(remake_final_body, encoding='utf-8')

# Write full HTML wrapper for browser preview
remake_full = PAGE_HEAD.replace("__TITLE__", "Remake Nedir? - Game+ Blog - V3") + remake_final_body + PAGE_FOOT
(OUT_DIR / 'ornek-blog-remake-v9.html').write_text(remake_full, encoding='utf-8')
print(f"✓ Remake v3 full: {len(remake_full)} chars")
print(f"✓ Remake v3 body: {len(remake_final_body)} chars")

# === Build GFN Thursday v5 ===
gfn_clean = Path('/tmp/gfn-thursday-original.html').read_text(encoding='utf-8')
gfn_clean, gfn_toc = inject_heading_ids(gfn_clean)
gfn_clean = shrink_youtube_embeds(gfn_clean)
gfn_toc_html = render_floating_toc(gfn_toc)
gfn_tldr = render_tldr([
    "<strong>Bu hafta:</strong> 21 Mayıs 2026 itibarıyla GeForce NOW kütüphanesine <strong>8 yeni oyun</strong> eklendi.",
    "<strong>Yıldız oyun:</strong> <em>Forza Horizon 6</em> Steam ve Xbox üzerinden Game Pass kapsamında yayında.",
    "<strong>Topluluk içeriği:</strong> Cloud Gaming Battle ile NVIDIA'dan Andrew Fear sohbeti GFN Reddit'te ilgi topladı.",
    "<strong>Listede ayrıca:</strong> Deep Rock Galactic: Rogue Core, Luna Abyss, Warhammer 40,000: Mechanicus II ve dahası.",
])
# gfn_info REMOVED in v8 — kullanıcı bu kısmı gereksiz buldu (özellik listesi kaldırıldı)
gfn_editor_1 = render_editor_note(
    "Forza Horizon 6, NVIDIA DLSS ile bulutta 4K akıcı performans sunan yapımlardan biri. Game Pass aboneliğin varsa Xbox hesabını GeForce NOW'a bağladığın an oyun kütüphanende otomatik beliriyor."
)
# Compact featured CTA (single-line) — replaces previous block CTA Paketler in mid-article
gfn_cta_paketler = render_compact_cta(
    "Forza Horizon 6'nın açık dünyasına dal!",
    "Performance veya Ultimate paketle Game Pass üzerinden anında oyna.",
    "GeForce NOW Paketleri",
    "https://gameplus.com.tr/gfn/paketler"
)
gfn_highlight = render_highlight(
    "GeForce NOW desteklenen yapımları oynamak için ilgili platformda (Steam, Xbox, Epic Games) oyun lisansına sahip olman gerekiyor. Bulut sadece çalıştırır, oyun satmaz.",
    "Hatırlatma"
)
gfn_end_cta = render_end_cta(
    "Game+ ile bulutta oyun keyfine hazır mısın?",
    "Performance ve Ultimate paketleri kütüphanendeki GeForce NOW destekli yapımları donanım olmadan oynamanı sağlar. 2.000'den fazla oyunu ve GFN Thursday'e eklenen yeni yapımları görmek için hemen kütüphaneye göz at!",
    btn2_label="GeForce NOW Oyunları",
    btn2_url="https://gameplus.com.tr/gfn/oyunlar",
    chip2="Oyunlar",
)
# Card-table data with platform links applied to meta strings
_gfn_games = [
    {'name': 'Forza Horizon 6', 'badge': 'YARIŞ', 'badge_color': '#dc2626', 'meta': '19 Mayıs · Steam, Xbox · Game Pass'},
    {'name': 'Deep Rock Galactic: Rogue Core', 'badge': 'CO-OP / ROGUELIKE', 'badge_color': '#7c3aed', 'meta': '20 Mayıs · Steam'},
    {'name': 'Luna Abyss', 'badge': 'FPS', 'badge_color': '#0891b2', 'meta': '21 Mayıs · Steam, Xbox · Game Pass'},
    {'name': 'Warhammer 40,000: Mechanicus II', 'badge': 'STRATEJİ', 'badge_color': '#16a34a', 'meta': '21 Mayıs · Steam'},
    {'name': 'ZERO PARADES', 'badge': 'INDIE', 'badge_color': '#f59e0b', 'meta': '21 Mayıs · Steam'},
    {'name': 'Splitgate Arena Reloaded', 'badge': 'FPS', 'badge_color': '#0891b2', 'meta': 'Xbox · Game Pass'},
    {'name': 'Sunderfolk', 'badge': 'CO-OP TAKTİK', 'badge_color': '#7c3aed', 'meta': 'Epic Games Store'},
    {'name': 'TerraTech Legion', 'badge': 'AKSİYON', 'badge_color': '#dc2626', 'meta': 'Steam, Xbox · Game Pass'},
]
for g in _gfn_games:
    g['meta'] = linkify_platforms(g['meta'], g['name'])
gfn_card_table = render_card_table("Bu Hafta Eklenen Oyunlar", _gfn_games)
gfn_prev_weeks = render_prev_weeks_cards([
    {'url': 'https://gameplus.com.tr/blog/gfn-thursday-geforce-now-da-bu-hafta-14-mayis-2026', 'date': '14 Mayıs 2026', 'label': 'Geçen haftanın yeni oyunları ve duyuruları'},
    {'url': 'https://gameplus.com.tr/blog/gfn-thursday--geforce-now%E2%80%99da-bu-hafta-(7-mayis-2026)', 'date': '7 Mayıs 2026', 'label': 'Mayıs ayının ilk haftası eklenenler'},
    {'url': 'https://gameplus.com.tr/blog/gfn-thursday---geforce-now-da-bu-hafta-30-nisan-2026', 'date': '30 Nisan 2026', 'label': 'Nisan kapanışı, ay sonu güncellemeleri'},
])

# Inject
gfn_clean = re.sub(r'(</h1>)', r'\1\n' + gfn_toc_html + gfn_tldr, gfn_clean, count=1)   # meta header YOK
gfn_clean = gfn_clean.replace('<h2 id="topluluktan-one-cikanlar">Topluluktan Öne Çıkanlar</h2>',
    gfn_cta_paketler + '<h2 id="topluluktan-one-cikanlar">Topluluktan Öne Çıkanlar</h2>', 1)
gfn_clean = gfn_clean.replace('<!-- Responsive YouTube Embed Sonu -->',
    '<!-- Responsive YouTube Embed Sonu -->\n' + gfn_editor_1, 1)
# Replace games list with card-table
gfn_clean = re.sub(r'<ul><li><p>Forza Horizon 6.*?</ul>', gfn_card_table.rstrip(), gfn_clean, count=1, flags=re.DOTALL)
# NOTE: gfn_cta_oyunlar REMOVED in v6 — single end CTA covers Paketler + Oyunlar
# Replace previous weeks ul with rich cards
gfn_clean = re.sub(
    r'<ul><li><p><a href="https://gameplus\.com\.tr/blog/gfn-thursday-geforce-now-da-bu-hafta-14-mayis-2026">.*?</ul>',
    gfn_prev_weeks, gfn_clean, count=1, flags=re.DOTALL
)
# End CTA + Highlight before last H2
gfn_clean = gfn_clean.replace('<h2 id="geforce-now-thursday-de-onceki-haftalarda-neler-oldu">',
    gfn_highlight + gfn_end_cta + '<h2 id="geforce-now-thursday-de-onceki-haftalarda-neler-oldu">', 1)

gfn_clean = ensure_leading_h1(gfn_clean)  # gövde tek bir H1 ile başlar (ilk başlık)
# NOT: kanonik kütüphanede her build'in SON adımı: verify_output(final_body, ...) + print_report(...) (content-rules 13).
gfn_final_body = ANIMATED_BORDER_STYLE + gfn_clean
(OUT_DIR / 'ornek-blog-gfn-thursday-v9-body-only.html').write_text(gfn_final_body, encoding='utf-8')
gfn_full = PAGE_HEAD.replace("__TITLE__", "GFN Thursday 21 Mayıs - Game+ Blog - V3") + gfn_final_body + PAGE_FOOT
(OUT_DIR / 'ornek-blog-gfn-thursday-v9.html').write_text(gfn_full, encoding='utf-8')
print(f"✓ GFN v3 full: {len(gfn_full)} chars")
print(f"✓ GFN v3 body: {len(gfn_final_body)} chars")
print(f"\nFiles in {OUT_DIR}:")
for f in sorted(OUT_DIR.glob('ornek-blog-*.html')):
    print(f"  {f.name} ({f.stat().st_size} bytes)")
