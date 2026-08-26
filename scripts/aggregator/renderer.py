"""
HTML Dashboard renderer built on Warm Editorial Parchment & Espresso Design System:
- High-detail gradient SVG Sun and Moon icons with realistic celestial lighting
- Realistic celestial Sun setting / Moon rising animation with spring physics
- Warm parchment paper light mode & warm espresso dark mode
"""

def render_item_html(item):
    """Render a single item li HTML snippet with compact, readable micro-card layout."""
    item_type = item.get("type")
    url = item.get("url", "#")
    title = item.get("title", "")
    
    if item_type == "hn":
        cmts = item.get("comments", 0)
        dom = item.get("domain", "")
        
        cmts_badge = f'<span class="badge comments">{cmts} comments</span>'
        dom_badge = f'<span class="badge domain">{dom}</span>' if dom else ''
        
        meta_html = f'<div class="meta">{cmts_badge}{dom_badge}</div>'
        
        return f"""      <li class="item">
        <a href="{url}" target="_blank" rel="noopener" class="item-title">{title}</a>
        {meta_html}
      </li>"""
      
    elif item_type == "github":
        title = item.get("title") or item.get("full_name") or ""
        stars = item.get("stars", 0)
        formatted_stars = f"{stars:,}"
        lang = item.get("language") or ""
        desc = item.get("description", "")
        
        star_svg = '<svg width="11" height="11" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true" style="display:inline-block;vertical-align:-1px;"><path d="M8 .25a.75.75 0 0 1 .673.418l1.882 3.815 4.21.612a.75.75 0 0 1 .416 1.279l-3.046 2.97.719 4.192a.75.75 0 0 1-1.088.791L8 12.347l-3.766 1.98a.75.75 0 0 1-1.088-.79l.72-4.194L.818 6.374a.75.75 0 0 1 .416-1.28l4.21-.611L7.327.668A.75.75 0 0 1 8 .25Z"></path></svg>'
        stars_badge = f'<span class="badge stars">{star_svg} {formatted_stars}</span>'
        lang_badge = f'<span class="badge lang">{lang}</span>' if lang else ''
        
        meta_html = f'<div class="meta">{stars_badge}{lang_badge}</div>'
        desc_html = f'\n        <div class="desc">{desc}</div>' if desc else ""
        
        return f"""      <li class="item">
        <a href="{url}" target="_blank" rel="noopener" class="item-title">{title}</a>
        {meta_html}{desc_html}
      </li>"""

    elif item_type == "arxiv":
        date_str = item.get("date", "")
        meta_html = f'<div class="meta"><span class="badge arxiv">arXiv</span><span class="badge date">{date_str}</span></div>'
        
        return f"""      <li class="item">
        <a href="{url}" target="_blank" rel="noopener" class="item-title">{title}</a>
        {meta_html}
      </li>"""

    return ""

def render_column_content(items, defaultquiet_msg):
    """Render ul content or quiet column fallback."""
    if not items:
        return f"""    <ul class="item-list">
      <li class="quiet">{defaultquiet_msg}</li>
    </ul>"""
    
    rendered_lis = [render_item_html(item) for item in items if item]
    lis_str = "\n".join(rendered_lis)
    return f"""    <ul class="item-list">
{lis_str}
    </ul>"""

def generate_dashboard_html(data):
    """Generate complete dashboard HTML with detailed gradient Sun and Moon artwork."""
    snapshot = data["snapshot"]
    
    agents_items = data.get("agents", [])
    infra_items = data.get("infra", [])
    applied_items = data.get("applied", [])
    opensource_items = data.get("opensource", [])

    agents_html = render_column_content(
        agents_items, 
        "No qualifying agent stories broke through in the last 48h."
    )
    infra_html = render_column_content(
        infra_items, 
        "No qualifying GPU/inference infra stories broke through in the last 48h."
    )
    applied_html = render_column_content(
        applied_items, 
        "No qualifying applied AI stories broke through in the last 48h."
    )
    opensource_html = render_column_content(
        opensource_items, 
        "No qualifying open-source repositories broke through in the last 30d."
    )

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AI News Dashboard</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<script>
  (function() {{
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark' || savedTheme === 'dusk' || savedTheme === 'light') {{
      document.documentElement.setAttribute('data-theme', savedTheme);
    }} else if (window.matchMedia('(prefers-color-scheme: dark)').matches) {{
      document.documentElement.setAttribute('data-theme', 'dark');
    }} else {{
      document.documentElement.setAttribute('data-theme', 'light');
    }}
  }})();
</script>
<style>
  :root {{
    /* Warm Parchment & Reader-Friendly Light Palette */
    --bg-color: #fcfaf6;
    --text-color: #1c1917;
    --text-muted: #78716c;
    --card-bg: #ffffff;
    --card-border: #e7e5e4;
    --card-shadow: 0 1px 3px rgba(28, 25, 23, 0.04), 0 4px 12px rgba(28, 25, 23, 0.02);
    --card-blur: none;

    --item-bg: #f5f2eb;
    --item-border: #e6e1d9;
    --item-hover: #ece6dc;
    
    --link-color: #1c1917;
    --link-hover: #c2410c;
    --badge-bg: #ffffff;
    --badge-text: #57534e;
    --badge-border: #d6d3d1;
    --focus-ring: #c2410c;
    
    /* Warm Domain Accent Indicators */
    --accent-agents: #4f46e5;
    --accent-infra: #c2410c;
    --accent-applied: #047857;
    --accent-opensource: #b45309;
    
    /* Morning Sky Palette for Sun Toggle */
    --toggle-bg: #fffbeb;
    --toggle-border: #fde68a;
  }}

  [data-theme="dark"] {{
    /* Warm Espresso & Dark Charcoal Palette */
    --bg-color: #12100e;
    --text-color: #f5f3ef;
    --text-muted: #a8a29e;
    --card-bg: #1a1715;
    --card-border: #292524;
    --card-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
    --card-blur: none;

    --item-bg: #231f1c;
    --item-border: #332d29;
    --item-hover: #2d2724;
    
    --link-color: #f5f3ef;
    --link-hover: #fb923c;
    --badge-bg: #1a1715;
    --badge-text: #a8a29e;
    --badge-border: #44403c;
    --focus-ring: #fb923c;
    
    --accent-agents: #818cf8;
    --accent-infra: #fb923c;
    --accent-applied: #34d399;
    --accent-opensource: #fbbf24;
    
    /* Midnight Cosmos Sky Palette for Moon Toggle */
    --toggle-bg: #1e1b4b;
    --toggle-border: #3730a3;
  }}

  [data-theme="dusk"] {{
    /* Serene Photorealistic Dusk Glassmorphism Palette */
    --bg-color: #120e29;
    --text-color: #fcf9f5;
    --text-muted: #d8ceec;
    --card-bg: linear-gradient(135deg, rgba(30, 20, 52, 0.62), rgba(16, 10, 32, 0.48));
    --card-border: rgba(255, 255, 255, 0.28);
    --card-shadow: 0 16px 48px rgba(8, 4, 20, 0.55), inset 0 1px 0 rgba(255, 255, 255, 0.35), inset 0 -1px 0 rgba(0, 0, 0, 0.25);
    --card-blur: blur(14px) saturate(160%) contrast(102%);

    --item-bg: rgba(14, 9, 28, 0.52);
    --item-border: rgba(255, 255, 255, 0.16);
    --item-hover: rgba(26, 16, 48, 0.72);

    --link-color: #fff9f0;
    --link-hover: #ffb86c;
    --badge-bg: rgba(0, 0, 0, 0.35);
    --badge-text: #f0e6ff;
    --badge-border: rgba(255, 255, 255, 0.25);
    --focus-ring: #ffb86c;

    --accent-agents: #c2caff;
    --accent-infra: #ffbd8a;
    --accent-applied: #8ff0cf;
    --accent-opensource: #ffe697;

    /* Twilight Sky Palette for Dusk Toggle */
    --toggle-bg: rgba(255, 255, 255, 0.16);
    --toggle-border: rgba(255, 255, 255, 0.38);
  }}

  * {{ box-sizing: border-box; }}
  
  html, body {{
    min-height: 100vh;
    margin: 0;
    padding: 0;
    background: var(--bg-color);
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    font-size: 13.5px;
    color: var(--text-color);
    transition: background 0.3s ease, color 0.3s ease;
    line-height: 1.45;
    -webkit-font-smoothing: antialiased;
  }}

  .container {{
    width: 100%;
    max-width: 100%;
    min-height: 100vh;
    padding: 20px 24px 24px;
    display: flex;
    flex-direction: column;
    box-sizing: border-box;
    position: relative;
    z-index: 1;
  }}

  /* ================================================================
     Dusk Valley Scene — Serene Realistic Photorealistic Backdrop
     ================================================================ */
  .dusk-backdrop-container {{
    position: fixed;
    inset: 0;
    width: 100%;
    height: 100%;
    z-index: 0;
    pointer-events: none;
    opacity: 0;
    visibility: hidden;
    transition: opacity 1.4s ease, visibility 1.4s ease;
  }}

  [data-theme="dusk"] .dusk-backdrop-container {{
    opacity: 1;
    visibility: visible;
  }}

  .dusk-bg-img {{
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: center bottom;
    filter: brightness(0.92) contrast(1.05) saturate(1.1);
  }}

  .dusk-scene {{
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    z-index: 1;
    pointer-events: none;
  }}

  .dusk-scene svg {{
    width: 100%;
    height: 100%;
    display: block;
  }}

  [data-theme="dusk"] h1,
  [data-theme="dusk"] .subtitle,
  [data-theme="dusk"] footer,
  [data-theme="dusk"] .footer-links a,
  [data-theme="dusk"] .col h2,
  [data-theme="dusk"] .item-title,
  [data-theme="dusk"] .desc {{
    text-shadow: 0 1px 10px rgba(15, 6, 30, 0.7);
  }}

  /* Frosted Glassmorphism Columns in Dusk Mode */
  [data-theme="dusk"] .col {{
    background: var(--card-bg);
    backdrop-filter: var(--card-blur);
    -webkit-backdrop-filter: var(--card-blur);
    border: 1px solid var(--card-border);
    box-shadow: var(--card-shadow);
    border-radius: 12px;
  }}

  [data-theme="dusk"] .item {{
    background: var(--item-bg);
    border: 1px solid var(--item-border);
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    box-shadow: 0 4px 14px rgba(5, 2, 14, 0.35);
    transition: background 0.25s ease, border-color 0.25s ease, transform 0.25s ease, box-shadow 0.25s ease;
  }}

  [data-theme="dusk"] .item:hover {{
    background: var(--item-hover);
    border-color: rgba(255, 184, 108, 0.45);
    box-shadow: 0 6px 20px rgba(5, 2, 14, 0.5), 0 0 14px rgba(255, 184, 108, 0.18);
    transform: translateY(-2px);
  }}

  /* Twinkling stars on the moonrise side */
  @keyframes duskTwinkle {{
    0%, 100% {{ opacity: 0.25; transform: scale(0.85); }}
    50% {{ opacity: 1; transform: scale(1.2); }}
  }}
  [data-theme="dusk"] .dusk-star {{
    transform-box: fill-box;
    transform-origin: 50% 50%;
    animation: duskTwinkle 3.8s ease-in-out infinite;
  }}

  /* Dying crimson sunset glow breathing gently behind left mountain horizon */
  @keyframes duskDyingSunsetGlow {{
    0%, 100% {{ opacity: 0.72; filter: brightness(1); }}
    50% {{ opacity: 0.95; filter: brightness(1.18); }}
  }}
  [data-theme="dusk"] .dusk-dying-glow {{
    animation: duskDyingSunsetGlow 8s ease-in-out infinite;
  }}
  [data-theme="dusk"] .dusk-dying-rays {{
    animation: duskDyingSunsetGlow 12s ease-in-out infinite;
  }}

  /* Atmospheric mountain fog drifting slowly */
  @keyframes duskFogDrift {{
    0%   {{ transform: translateX(-35px); opacity: 0.45; }}
    50%  {{ transform: translateX(35px); opacity: 0.75; }}
    100% {{ transform: translateX(-35px); opacity: 0.45; }}
  }}
  [data-theme="dusk"] .dusk-fog {{
    animation: duskFogDrift 95s ease-in-out infinite;
  }}
  [data-theme="dusk"] .dusk-fog.alt {{
    animation-direction: reverse;
    animation-duration: 110s;
  }}

  /* Wildflowers swaying in a gentle valley breeze */
  @keyframes duskFlowerSway {{
    0%, 100% {{ transform: rotate(-3.5deg); }}
    50% {{ transform: rotate(3.5deg); }}
  }}
  [data-theme="dusk"] .dusk-flower {{
    transform-box: fill-box;
    transform-origin: 50% 100%;
    animation: duskFlowerSway 6s ease-in-out infinite;
  }}

  /* Floating light dust motes rising serenely */
  @keyframes duskLightMoteFloat {{
    0%   {{ transform: translateY(0) scale(0.8); opacity: 0.2; }}
    50%  {{ transform: translateY(-40px) scale(1.2); opacity: 0.85; }}
    100% {{ transform: translateY(-80px) scale(0.8); opacity: 0; }}
  }}
  [data-theme="dusk"] .dusk-mote {{
    animation: duskLightMoteFloat 14s ease-in-out infinite;
  }}

  /* Butterflies drifting on calm, graceful flight loops */
  @keyframes duskButterflyFlutter {{
    0%    {{ transform: translate(0, 0) rotate(0deg); }}
    25%   {{ transform: translate(35px, -20px) rotate(6deg); }}
    50%   {{ transform: translate(70px, 4px) rotate(-4deg); }}
    75%   {{ transform: translate(35px, 22px) rotate(5deg); }}
    100%  {{ transform: translate(0, 0) rotate(0deg); }}
  }}
  [data-theme="dusk"] .dusk-butterfly {{
    transform-box: fill-box;
    transform-origin: 50% 50%;
    animation: duskButterflyFlutter 26s ease-in-out infinite;
  }}

  /* Wing flap 3D perspective hinge */
  [data-theme="dusk"] .dusk-butterfly-body {{
    transform-style: preserve-3d;
    perspective: 140px;
  }}
  @keyframes duskWingFlap {{
    0%, 100% {{ transform: rotateY(0deg); }}
    50%      {{ transform: rotateY(68deg); }}
  }}
  [data-theme="dusk"] .dusk-wing-l {{
    transform-box: fill-box;
    transform-origin: 100% 50%;
    animation: duskWingFlap 0.75s ease-in-out infinite;
  }}
  [data-theme="dusk"] .dusk-wing-r {{
    transform-box: fill-box;
    transform-origin: 0% 50%;
    animation: duskWingFlap 0.75s ease-in-out infinite;
  }}

  /* 2 Wild Rabbits: realistic long calm resting pause, then two subtle, gentle hops */
  @keyframes duskRabbitSereneHop {{
    0%, 75%, 100% {{ transform: translate(0, 0) scale(1); }}
    80%  {{ transform: translate(6px, -8px) scaleY(1.06) scaleX(0.96); }}
    85%  {{ transform: translate(12px, -1px) scaleY(0.96) scaleX(1.03); }}
    90%  {{ transform: translate(18px, -9px) scaleY(1.06) scaleX(0.96); }}
    95%  {{ transform: translate(24px, 0px) scaleY(0.97) scaleX(1.02); }}
  }}
  [data-theme="dusk"] .dusk-rabbit {{
    transform-box: fill-box;
    transform-origin: 50% 100%;
    animation: duskRabbitSereneHop 18s ease-in-out infinite;
  }}
  @keyframes duskRabbitShadowPulse {{
    0%, 75%, 100% {{ opacity: 0.42; transform: scaleX(1); }}
    80%, 90% {{ opacity: 0.18; transform: scaleX(0.75); }}
    85%, 95% {{ opacity: 0.35; transform: scaleX(0.9); }}
  }}
  [data-theme="dusk"] .dusk-rabbit-shadow {{
    transform-box: fill-box;
    transform-origin: 50% 50%;
    animation: duskRabbitShadowPulse 18s ease-in-out infinite;
  }}

  /* Rim light on mountain ridges */
  @keyframes duskRimGlow {{
    0%, 100% {{ opacity: 0.55; }}
    50% {{ opacity: 0.85; }}
  }}
  [data-theme="dusk"] .dusk-rim {{
    animation: duskRimGlow 9s ease-in-out infinite;
  }}

  :focus-visible {{
    outline: 2px solid var(--focus-ring);
    outline-offset: 2px;
    border-radius: 4px;
  }}

  /* Header Section */
  .header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 18px;
  }}
  
  .brand-group {{
    display: flex;
    flex-direction: column;
    gap: 2px;
  }}
  
  .title-row {{
    display: flex;
    align-items: center;
    gap: 12px;
  }}
  
  h1 {{
    font-size: 22px;
    font-weight: 700;
    margin: 0;
    letter-spacing: -0.025em;
    color: var(--text-color);
  }}
  
  .subtitle {{
    color: var(--text-muted);
    font-size: 12px;
    font-variant-numeric: tabular-nums;
  }}

  .header-actions {{
    display: flex;
    align-items: center;
  }}
  
  /* Celestial Realistic Sun Setting & Moon Rising Button */
  .theme-toggle {{
    position: relative;
    width: 42px;
    height: 42px;
    border-radius: 50%;
    border: 1px solid var(--toggle-border);
    background: var(--toggle-bg);
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    transition: background 0.45s cubic-bezier(0.4, 0, 0.2, 1), border-color 0.45s cubic-bezier(0.4, 0, 0.2, 1), transform 0.2s ease, box-shadow 0.2s ease;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  }}
  
  .theme-toggle:hover {{
    transform: scale(1.08);
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
  }}

  .sun-icon, .moon-icon, .dusk-icon {{
    position: absolute;
    transition: transform 0.5s cubic-bezier(0.34, 1.56, 0.64, 1), opacity 0.4s ease;
  }}

  /* Light Mode: Radiant Sun in Sky, Moon & Dusk horizon set below */
  :root .sun-icon {{
    transform: translateY(0) rotate(0deg) scale(1);
    opacity: 1;
  }}
  :root .moon-icon, :root .dusk-icon {{
    transform: translateY(30px) rotate(-90deg) scale(0.4);
    opacity: 0;
  }}

  /* Dark Mode: Sun sets down into horizon, Crescent Moon rises up into midnight sky */
  [data-theme="dark"] .sun-icon, [data-theme="dark"] .dusk-icon {{
    transform: translateY(30px) rotate(90deg) scale(0.4);
    opacity: 0;
  }}
  [data-theme="dark"] .moon-icon {{
    transform: translateY(0) rotate(0deg) scale(1);
    opacity: 1;
  }}

  /* Dusk Mode: Sun & Moon settle to the horizon, twilight valley glyph rises */
  [data-theme="dusk"] .sun-icon, [data-theme="dusk"] .moon-icon {{
    transform: translateY(30px) rotate(-90deg) scale(0.4);
    opacity: 0;
  }}
  [data-theme="dusk"] .dusk-icon {{
    transform: translateY(0) rotate(0deg) scale(1);
    opacity: 1;
  }}

  /* Full-Width 4-Column Grid */
  .grid {{
    flex: 1;
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 18px;
    align-items: start;
  }}
  
  @media (max-width: 1120px) {{
    .grid {{
      grid-template-columns: repeat(2, 1fr);
    }}
  }}
  
  @media (max-width: 600px) {{
    .grid {{ grid-template-columns: 1fr; }}
  }}

  /* Column Cards */
  .col {{
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 14px;
    padding: 16px;
    box-shadow: var(--card-shadow);
    backdrop-filter: var(--card-blur);
    -webkit-backdrop-filter: var(--card-blur);
    display: flex;
    flex-direction: column;
    transform: translateZ(0);
    transition: background 0.5s ease, border-color 0.5s ease, box-shadow 0.5s ease, backdrop-filter 0.5s ease;
  }}

  .col-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
    padding-bottom: 6px;
  }}
  
  .col-title-group {{
    display: flex;
    align-items: center;
    gap: 8px;
  }}
  
  .col-title-indicator {{
    width: 4px;
    height: 14px;
    border-radius: 2px;
  }}
  
  .col.agents .col-title-indicator {{ background: var(--accent-agents); }}
  .col.infra .col-title-indicator {{ background: var(--accent-infra); }}
  .col.applied .col-title-indicator {{ background: var(--accent-applied); }}
  .col.opensource .col-title-indicator {{ background: var(--accent-opensource); }}

  .col h2 {{
    font-size: 15px;
    font-weight: 700;
    margin: 0;
    letter-spacing: -0.015em;
    color: var(--text-color);
  }}

  /* Tight Item List Layout */
  ul.item-list {{
    list-style: none;
    margin: 0;
    padding: 0;
    display: flex;
    flex-direction: column;
    gap: 8px;
  }}

  /* News Item Micro-Cards with Warm Surfaces */
  li.item {{
    padding: 10px 12px;
    border-radius: 8px;
    background: var(--item-bg);
    border: 1px solid var(--item-border);
    transition: background 0.15s ease, border-color 0.15s ease;
  }}
  
  li.item:hover {{
    background: var(--item-hover);
  }}

  .item-title {{
    color: var(--link-color);
    text-decoration: none;
    font-weight: 600;
    font-size: 13.5px;
    line-height: 1.4;
    display: block;
    margin-bottom: 5px;
    transition: color 0.15s ease;
  }}
  
  .item-title:hover {{
    color: var(--link-hover);
    text-decoration: underline;
  }}

  /* Meta & Badges */
  .meta {{
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 6px;
    margin-top: 4px;
    font-variant-numeric: tabular-nums;
  }}
  
  .badge {{
    font-size: 10.5px;
    font-weight: 500;
    padding: 1px 6px;
    border-radius: 4px;
    background: var(--badge-bg);
    color: var(--badge-text);
    border: 1px solid var(--badge-border);
    display: inline-flex;
    align-items: center;
    gap: 3px;
  }}
  
  .badge.comments {{ color: var(--accent-infra); font-weight: 500; }}
  .badge.stars {{ color: var(--accent-opensource); font-weight: 600; }}
  .badge.domain {{ color: var(--text-muted); }}
  .badge.arxiv {{ color: var(--accent-agents); font-weight: 600; }}

  .desc {{
    color: var(--text-muted);
    font-size: 12px;
    margin-top: 4px;
    line-height: 1.4;
  }}
  
  .quiet {{
    color: var(--text-muted);
    font-size: 12px;
    font-style: italic;
    padding: 12px;
    text-align: center;
  }}

  /* Footer Section */
  footer {{
    margin-top: 24px;
    color: var(--text-muted);
    font-size: 12px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }}
  
  .footer-links {{
    display: flex;
    gap: 16px;
  }}
  
  .footer-links a {{
    color: var(--text-muted);
    text-decoration: none;
    font-weight: 500;
  }}
  
  .footer-links a:hover {{
    color: var(--link-color);
  }}

  @media (prefers-reduced-motion: reduce) {{
    body, .col, .item, .item-title, .theme-toggle, .sun-icon, .moon-icon, .dusk-icon,
    .dusk-star, .dusk-glow, .dusk-rays, .dusk-cloud, .dusk-flower, .dusk-butterfly,
    .dusk-wing-l, .dusk-wing-r, .dusk-rabbit, .dusk-rabbit-shadow, .dusk-rim {{
      transition: none !important;
      animation: none !important;
    }}
  }}
</style>
</head>
<body>

<div class="dusk-backdrop-container" aria-hidden="true">
  <img class="dusk-bg-img" src="dusk_bg.png" alt="Serene Realistic Dusk Landscape">
  <div class="dusk-scene">
    <svg viewBox="0 0 1600 850" preserveAspectRatio="xMidYMid slice" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <!-- Sky: Dying crimson sunset red bleeding into warm coral, violet plum, and deep midnight navy -->
      <linearGradient id="duskSkyGrad" x1="0%" y1="20%" x2="100%" y2="0%">
        <stop offset="0%"   stop-color="#8a1829"/>
        <stop offset="14%"  stop-color="#b8382c"/>
        <stop offset="28%"  stop-color="#d65d40"/>
        <stop offset="42%"  stop-color="#aa486b"/>
        <stop offset="58%"  stop-color="#69346d"/>
        <stop offset="74%"  stop-color="#3c2656"/>
        <stop offset="88%"  stop-color="#1d163a"/>
        <stop offset="100%" stop-color="#0c0a22"/>
      </linearGradient>

      <!-- Dying Sun: Sun hidden below horizon line with deep crimson and golden dusk glow -->
      <radialGradient id="duskDyingSunsetHalo" cx="15%" cy="75%" r="60%">
        <stop offset="0%" stop-color="#ff4a2b" stop-opacity="0.85"/>
        <stop offset="25%" stop-color="#e63e26" stop-opacity="0.60"/>
        <stop offset="55%" stop-color="#b82d38" stop-opacity="0.30"/>
        <stop offset="85%" stop-color="#6c1d45" stop-opacity="0.08"/>
        <stop offset="100%" stop-color="#6c1d45" stop-opacity="0"/>
      </radialGradient>
      
      <linearGradient id="duskDyingRayGrad" x1="0%" y1="100%" x2="0%" y2="0%">
        <stop offset="0%" stop-color="#ff7b36" stop-opacity="0.45"/>
        <stop offset="60%" stop-color="#e63e26" stop-opacity="0.18"/>
        <stop offset="100%" stop-color="#b82d38" stop-opacity="0"/>
      </linearGradient>

      <!-- Realistic Moon: Luminous silver crescent with lunar surface texture -->
      <linearGradient id="duskMoonGrad" x1="20%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#ffffff"/>
        <stop offset="45%" stop-color="#f0f2ff"/>
        <stop offset="85%" stop-color="#cad0f5"/>
        <stop offset="100%" stop-color="#9ea7d9"/>
      </linearGradient>
      <radialGradient id="duskMoonHalo" cx="50%" cy="50%" r="50%">
        <stop offset="0%" stop-color="#d6deff" stop-opacity="0.55"/>
        <stop offset="40%" stop-color="#a8b8ff" stop-opacity="0.25"/>
        <stop offset="100%" stop-color="#8a99e6" stop-opacity="0"/>
      </radialGradient>
      
      <!-- Atmospheric Perspective Ridge Fills -->
      <!-- Distant Mountain Ridge: Pale hazy indigo/violet with fog blur -->
      <linearGradient id="farRidgeGrad" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stop-color="#766399"/>
        <stop offset="100%" stop-color="#463768"/>
      </linearGradient>
      <!-- Mid Ridge: Deep violet with pine silhouette accents catching warm red rim-light on left -->
      <linearGradient id="midRidgeGrad" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stop-color="#3d2c5c"/>
        <stop offset="100%" stop-color="#23173d"/>
      </linearGradient>
      <!-- Near Ridge & Meadow: Rich dark violet-black valley soil -->
      <linearGradient id="nearRidgeGrad" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stop-color="#1b122e"/>
        <stop offset="100%" stop-color="#0b0716"/>
      </linearGradient>
      
      <!-- Winding River Reflection -->
      <linearGradient id="duskRiverGrad" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" stop-color="#d65d40" stop-opacity="0.55"/>
        <stop offset="40%" stop-color="#aa486b" stop-opacity="0.45"/>
        <stop offset="100%" stop-color="#463768" stop-opacity="0.65"/>
      </linearGradient>

      <!-- Rim lighting gradient on left ridge edges -->
      <linearGradient id="rimGrad" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" stop-color="#ff7b36" stop-opacity="0.95"/>
        <stop offset="25%" stop-color="#e63e26" stop-opacity="0.65"/>
        <stop offset="60%" stop-color="#b82d38" stop-opacity="0.3"/>
        <stop offset="100%" stop-color="#69346d" stop-opacity="0"/>
      </linearGradient>

      <!-- Gaussian Blur Filters for Atmospheric Fog & Depth -->
      <filter id="duskBloom" x="-100%" y="-100%" width="300%" height="300%">
        <feGaussianBlur in="SourceGraphic" stdDeviation="14" result="blur"/>
        <feMerge>
          <feMergeNode in="blur"/>
          <feMergeNode in="SourceGraphic"/>
        </feMerge>
      </filter>
      <filter id="duskBlurSoft" x="-40%" y="-40%" width="180%" height="180%">
        <feGaussianBlur stdDeviation="2"/>
      </filter>
      <filter id="duskBlurMed" x="-60%" y="-60%" width="220%" height="220%">
        <feGaussianBlur stdDeviation="6"/>
      </filter>
      <filter id="duskBlurHaze" x="-60%" y="-60%" width="220%" height="220%">
        <feGaussianBlur stdDeviation="16"/>
      </filter>

      <!-- Sparkle Glyph for Night Stars -->
      <path id="duskSparkle" d="M0,-7 C0.7,-2.3 2.3,-0.7 7,0 C2.3,0.7 0.7,2.3 0,7 C-0.7,2.3 -2.3,0.7 -7,0 C-2.3,-0.7 -0.7,-2.3 0,-7 Z"/>

      <!-- Wildflower 1: Lupine / Lavender Spike (anchored at ground point 10,40) -->
      <symbol id="duskLupine" viewBox="0 0 20 40">
        <path d="M10,40 L10,12" stroke="#48683e" stroke-width="1.6" stroke-linecap="round"/>
        <ellipse cx="10" cy="8" rx="2.5" ry="4" fill="#a484e8"/>
        <ellipse cx="7" cy="13" rx="2.8" fill="#8862d8"/>
        <ellipse cx="13" cy="13" rx="2.8" fill="#8862d8"/>
        <ellipse cx="6" cy="19" rx="3.2" fill="#7248c8"/>
        <ellipse cx="14" cy="19" rx="3.2" fill="#7248c8"/>
        <ellipse cx="5" cy="25" rx="3.5" fill="#5f35b4"/>
        <ellipse cx="15" cy="25" rx="3.5" fill="#5f35b4"/>
        <path d="M10,32 Q5,28 3,31 Q8,34 10,32 Z" fill="#48683e"/>
        <path d="M10,30 Q15,26 17,29 Q12,32 10,30 Z" fill="#48683e"/>
      </symbol>

      <!-- Wildflower 2: Red Poppy -->
      <symbol id="duskPoppy" viewBox="0 0 22 34">
        <path d="M11,34 Q9,22 11,14" fill="none" stroke="#426038" stroke-width="1.5" stroke-linecap="round"/>
        <g>
          <path d="M11,14 C6,6 2,12 11,14 Z" fill="#e63e26" opacity="0.95"/>
          <path d="M11,14 C16,6 20,12 11,14 Z" fill="#e63e26" opacity="0.95"/>
          <path d="M11,14 C4,10 8,2 11,14 Z" fill="#ff5c42" opacity="0.9"/>
          <path d="M11,14 C18,10 14,2 11,14 Z" fill="#ff5c42" opacity="0.9"/>
        </g>
        <circle cx="11" cy="14" r="2.2" fill="#201018"/>
      </symbol>

      <!-- Wildflower 3: White Daisy -->
      <symbol id="duskDaisy" viewBox="0 0 20 32">
        <path d="M10,32 Q11,20 10,12" fill="none" stroke="#48683e" stroke-width="1.4"/>
        <g>
          <ellipse cx="10" cy="5" rx="1.6" ry="4.5" fill="#f5f0fb"/>
          <ellipse cx="10" cy="19" rx="1.6" ry="4.5" fill="#f5f0fb"/>
          <ellipse cx="3" cy="12" rx="4.5" ry="1.6" fill="#f5f0fb"/>
          <ellipse cx="17" cy="12" rx="4.5" ry="1.6" fill="#f5f0fb"/>
          <ellipse cx="5" cy="7" rx="4" ry="1.6" fill="#eae2f8" transform="rotate(-45 5 7)"/>
          <ellipse cx="15" cy="17" rx="4" ry="1.6" fill="#eae2f8" transform="rotate(-45 15 17)"/>
          <ellipse cx="15" cy="7" rx="4" ry="1.6" fill="#eae2f8" transform="rotate(45 15 7)"/>
          <ellipse cx="5" cy="17" rx="4" ry="1.6" fill="#eae2f8" transform="rotate(45 5 17)"/>
        </g>
        <circle cx="10" cy="12" r="2.4" fill="#ffc247"/>
      </symbol>

      <!-- Realistic Butterfly Symbol -->
      <symbol id="duskButterfly" viewBox="0 0 28 22">
        <g class="dusk-butterfly-body">
          <path d="M12.5,6 Q11,3.5 12,2.5" fill="none" stroke="#251a36" stroke-width="0.7" stroke-linecap="round"/>
          <path d="M15.5,6 Q17,3.5 16,2.5" fill="none" stroke="#251a36" stroke-width="0.7" stroke-linecap="round"/>
          <g class="dusk-wing-l">
            <path d="M14,11 C9.5,2 2,3.5 3.5,10 C2,13.5 7.5,14.5 14,11 Z" fill="currentColor" opacity="0.95"/>
            <path d="M14,11 C10.5,14 6,19 8.5,20 C11.5,19 14,14.5 14,11 Z" fill="currentColor" opacity="0.75"/>
            <circle cx="7" cy="7.5" r="1.1" fill="#fffdf5" opacity="0.7"/>
          </g>
          <g class="dusk-wing-r">
            <path d="M14,11 C18.5,2 26,3.5 24.5,10 C26,13.5 20.5,14.5 14,11 Z" fill="currentColor" opacity="0.95"/>
            <path d="M14,11 C17.5,14 22,19 19.5,20 C16.5,19 14,14.5 14,11 Z" fill="currentColor" opacity="0.75"/>
            <circle cx="21" cy="7.5" r="1.1" fill="#fffdf5" opacity="0.7"/>
          </g>
          <ellipse cx="14" cy="11" rx="1.2" ry="4.8" fill="#201530"/>
        </g>
      </symbol>

      <!-- Realistic Wild Rabbit Symbol (Anatomically detailed sitting posture) -->
      <symbol id="duskRabbit" viewBox="0 0 36 30">
        <!-- Fluffy tail -->
        <ellipse cx="4.5" cy="22" rx="2.5" ry="2.2" fill="#d9cbdf" opacity="0.9"/>
        <!-- Hind leg / thigh curve -->
        <path d="M6,25 C3,18 7,12 16,12 C24,12 30,17 29,23 C28,27 22,29 15,29 C9,29 6.5,27.5 6,25 Z" fill="#302343"/>
        <!-- Soft inner fur shadow -->
        <path d="M12,27 C8,27 7,24.5 9,21 C12,16 18,16 22,21 C24,24.5 20,27 12,27 Z" fill="#231834" opacity="0.6"/>
        <!-- Perked ears with realistic pinkish interior fill -->
        <path d="M20,6 C18.5,-2 21,-4.5 23.5,3.5 C23,6 21.5,7 20,6 Z" fill="#302343"/>
        <path d="M25.5,5 C26.8,-2.5 29.2,-3.5 29.2,4 C28.5,6.5 27,6.8 25.5,5 Z" fill="#302343"/>
        <path d="M21,3.5 C20.2,-0.5 21.8,-2 23,2.5" fill="#e8b8c8" opacity="0.45"/>
        <path d="M26.5,3 C27.3,-0.8 28.5,-1.5 28,2.8" fill="#e8b8c8" opacity="0.45"/>
        <!-- Rabbit Head & Eye -->
        <circle cx="24.5" cy="10" r="5" fill="#302343"/>
        <circle cx="26.8" cy="8.8" r="0.8" fill="#0c0714"/>
        <circle cx="27" cy="8.6" r="0.25" fill="#ffffff" opacity="0.8"/>
        <!-- Sniffing nose -->
        <path d="M28.8,10.2 Q29.8,10.5 29.2,11.2" stroke="#e8b8c8" stroke-width="0.6" fill="none"/>
      </symbol>
    </defs>

    <!-- 1. Sky Base -->
    <rect x="0" y="0" width="1600" height="850" fill="url(#duskSkyGrad)"/>

    <!-- 2. Stars on the Right Twilight Sky -->
    <g class="dusk-stars">
      <circle class="dusk-star" cx="980"  cy="85"  r="1.4" fill="#fbfaff" style="animation-delay:-0.5s"/>
      <circle class="dusk-star" cx="1060" cy="140" r="1.1" fill="#fbfaff" style="animation-delay:-2.1s"/>
      <circle class="dusk-star" cx="1140" cy="65"  r="1.6" fill="#fbfaff" style="animation-delay:-1.2s"/>
      <circle class="dusk-star" cx="1220" cy="125" r="1.2" fill="#fbfaff" style="animation-delay:-2.8s"/>
      <circle class="dusk-star" cx="1290" cy="45"  r="1.5" fill="#fbfaff" style="animation-delay:-1.5s"/>
      <circle class="dusk-star" cx="1370" cy="155" r="1.1" fill="#fbfaff" style="animation-delay:-3.2s"/>
      <circle class="dusk-star" cx="1460" cy="85"  r="1.7" fill="#fbfaff" style="animation-delay:-0.4s"/>
      <circle class="dusk-star" cx="1520" cy="165" r="1.1" fill="#fbfaff" style="animation-delay:-1.9s"/>
      <circle class="dusk-star" cx="1570" cy="95"  r="1.4" fill="#fbfaff" style="animation-delay:-2.5s"/>
      <circle class="dusk-star" cx="910"  cy="175" r="1.0" fill="#fbfaff" style="animation-delay:-3.6s"/>
      <circle class="dusk-star" cx="1190" cy="205" r="1.1" fill="#fbfaff" style="animation-delay:-0.8s"/>
      <use class="dusk-star" href="#duskSparkle" transform="translate(1320,175) scale(0.85)" fill="#ffffff" style="animation-delay:-1.4s"/>
      <use class="dusk-star" href="#duskSparkle" transform="translate(1495,120) scale(0.65)" fill="#ffffff" style="animation-delay:-2.7s"/>
    </g>

    <!-- 3. Dying Crimson Sunset Rays (Sun hidden below mountain horizon on left) -->
    <circle class="dusk-dying-glow" cx="180" cy="590" r="320" fill="url(#duskDyingSunsetHalo)"/>
    <g class="dusk-dying-rays" transform="translate(180,580)" opacity="0.6" filter="url(#duskBlurMed)">
      <rect x="-6" y="-300" width="12" height="300" fill="url(#duskDyingRayGrad)" transform="rotate(-38)"/>
      <rect x="-4" y="-270" width="8"  height="270" fill="url(#duskDyingRayGrad)" transform="rotate(-18)"/>
      <rect x="-5" y="-280" width="10" height="280" fill="url(#duskDyingRayGrad)" transform="rotate(8)"/>
      <rect x="-6" y="-250" width="12" height="250" fill="url(#duskDyingRayGrad)" transform="rotate(28)"/>
      <rect x="-3" y="-220" width="6"  height="220" fill="url(#duskDyingRayGrad)" transform="rotate(48)"/>
    </g>

    <!-- 4. Realistic Moon (Right Sky) -->
    <circle class="dusk-dying-glow" cx="1360" cy="140" r="140" fill="url(#duskMoonHalo)" style="animation-delay:-3.5s"/>
    <!-- Crescent Moon Path -->
    <path d="M1395,95 a50,50 0 1 0 4,82 a40,40 0 0 1 -4,-82 z" fill="url(#duskMoonGrad)" filter="url(#duskBloom)"/>

    <!-- 5. Distant Mountain Ridge (Pale indigo atmospheric depth haze) -->
    <path d="M0,520 C140,480 220,500 340,450 C440,410 520,460 620,420 C720,380 820,430 920,390 C1020,350 1120,410 1220,380 C1340,340 1460,400 1600,370 L1600,850 L0,850 Z"
          fill="url(#farRidgeGrad)" opacity="0.55" filter="url(#duskBlurSoft)"/>

    <!-- 6. Mid Mountain Ridge (Shaping valley & pine forest silhouettes) -->
    <path d="M0,590 C160,540 280,570 400,530 C500,500 580,560 670,540 C720,530 740,580 780,610 C820,630 850,570 890,540 C980,500 1080,560 1180,530 C1300,490 1420,550 1600,525 L1600,850 L0,850 Z"
          fill="url(#midRidgeGrad)" opacity="0.9"/>
    
    <!-- Warm rim light on left mountain peaks from dying sunset -->
    <path class="dusk-rim" d="M0,590 C160,540 280,570 400,530 C500,500 580,560 670,540"
          fill="none" stroke="url(#rimGrad)" stroke-width="4.5" stroke-linecap="round" filter="url(#duskBlurMed)" opacity="0.75"/>

    <!-- 7. Winding Valley River Stream reflecting sky -->
    <path d="M720,605 C710,630 735,660 760,680 C790,705 840,715 880,740 C910,760 930,790 940,850 L890,850 C880,800 860,775 830,755 C790,730 740,715 710,690 C690,670 675,640 685,615 Z"
          fill="url(#duskRiverGrad)"/>

    <!-- 8. Atmospheric Drifting Mist / Fog Layers -->
    <ellipse class="dusk-fog" cx="380" cy="540" rx="200" ry="18" fill="#d65d40" opacity="0.12" filter="url(#duskBlurHaze)"/>
    <ellipse class="dusk-fog alt" cx="1120" cy="500" rx="220" ry="22" fill="#aa486b" opacity="0.15" filter="url(#duskBlurHaze)"/>

    <!-- 9. Near Mountain Ridge & Valley Floor -->
    <path d="M0,670 C200,625 340,665 480,620 C580,588 670,655 780,625 C850,605 920,660 1000,630 C1100,595 1220,655 1340,620 C1440,592 1540,645 1600,618 L1600,850 L0,850 Z"
          fill="url(#nearRidgeGrad)"/>

    <!-- Dirt Path curving through meadow into the valley -->
    <path d="M460,850 C490,800 520,770 560,750 C600,730 650,720 680,690 C700,670 705,640 710,620"
          fill="none" stroke="#2a1d3b" stroke-width="16" stroke-linecap="round" opacity="0.75"/>
    <path d="M460,850 C490,800 520,770 560,750 C600,730 650,720 680,690 C700,670 705,640 710,620"
          fill="none" stroke="#3b2b4f" stroke-width="10" stroke-linecap="round" opacity="0.6"/>

    <!-- 10. Meadow Flowers (Rich Lupin, Poppy, Daisy, Bluebell clusters) -->
    <!-- Left Meadow Cluster -->
    <use href="#duskLupine" class="dusk-flower" x="65"  y="740" width="20" height="40" style="animation-delay:-0.4s"/>
    <use href="#duskLupine" class="dusk-flower" x="90"  y="750" width="20" height="40" style="animation-delay:-1.8s"/>
    <use href="#duskPoppy"  class="dusk-flower" x="145" y="755" width="22" height="34" style="animation-delay:-2.5s"/>
    <use href="#duskDaisy"  class="dusk-flower" x="180" y="760" width="20" height="32" style="animation-delay:-1.1s"/>
    <use href="#duskLupine" class="dusk-flower" x="220" y="745" width="20" height="40" style="animation-delay:-3.2s"/>
    <use href="#duskPoppy"  class="dusk-flower" x="270" y="765" width="22" height="34" style="animation-delay:-0.9s"/>
    
    <!-- Center Meadow Cluster -->
    <use href="#duskDaisy"  class="dusk-flower" x="340" y="770" width="20" height="32" style="animation-delay:-2.7s"/>
    <use href="#duskLupine" class="dusk-flower" x="500" y="765" width="20" height="40" style="animation-delay:-1.4s"/>
    <use href="#duskPoppy"  class="dusk-flower" x="545" y="775" width="22" height="34" style="animation-delay:-4.1s"/>
    
    <!-- Right Meadow Cluster -->
    <use href="#duskLupine" class="dusk-flower" x="980"  y="755" width="20" height="40" style="animation-delay:-0.7s"/>
    <use href="#duskDaisy"  class="dusk-flower" x="1030" y="765" width="20" height="32" style="animation-delay:-2.3s"/>
    <use href="#duskPoppy"  class="dusk-flower" x="1080" y="760" width="22" height="34" style="animation-delay:-1.6s"/>
    <use href="#duskLupine" class="dusk-flower" x="1140" y="745" width="20" height="40" style="animation-delay:-3.5s"/>
    <use href="#duskDaisy"  class="dusk-flower" x="1200" y="770" width="20" height="32" style="animation-delay:-0.3s"/>
    <use href="#duskPoppy"  class="dusk-flower" x="1270" y="755" width="22" height="34" style="animation-delay:-2.9s"/>

    <!-- 11. Subtle Flying Butterflies (Monarch orange/black & Morpho blue) -->
    <use href="#duskButterfly" class="dusk-butterfly"     x="210" y="660" width="28" height="22" color="#e63e26" style="animation-delay:-5s"/>
    <use href="#duskButterfly" class="dusk-butterfly alt" x="610" y="640" width="28" height="22" color="#8862d8" style="animation-delay:-12s"/>
    <use href="#duskButterfly" class="dusk-butterfly"     x="1050" y="670" width="28" height="22" color="#ff7b36" style="animation-delay:-18s"/>

    <!-- 12. 2 Realistic Wild Rabbits Resting / Hopping in the Meadow -->
    <!-- Rabbit 1: Resting peacefully in left meadow grass -->
    <ellipse class="dusk-rabbit-shadow" cx="396" cy="774" rx="14" ry="3.2" fill="#05030a" style="animation-delay:-2s"/>
    <use href="#duskRabbit" class="dusk-rabbit" x="378" y="746" width="36" height="30" style="animation-delay:-2s"/>

    <!-- Rabbit 2: Resting near center pathway -->
    <ellipse class="dusk-rabbit-shadow" cx="446" cy="784" rx="14" ry="3.2" fill="#05030a" style="animation-delay:-7s"/>
    <use href="#duskRabbit" class="dusk-rabbit" x="428" y="756" width="36" height="30" style="animation-delay:-7s"/>

    <!-- 13. Floating Ambient Light Dust Motes -->
    <circle class="dusk-mote" cx="240" cy="720" r="1.5" fill="#ffb86c" style="animation-delay:-1s"/>
    <circle class="dusk-mote" cx="420" cy="700" r="2.0" fill="#f0e6ff" style="animation-delay:-5s"/>
    <circle class="dusk-mote" cx="680" cy="680" r="1.2" fill="#ff7b36" style="animation-delay:-9s"/>
    <circle class="dusk-mote" cx="1090" cy="710" r="1.8" fill="#ffb86c" style="animation-delay:-3s"/>
    <circle class="dusk-mote" cx="1260" cy="690" r="1.4" fill="#f0e6ff" style="animation-delay:-7s"/>
  </svg>
  </div>
</div>

<div class="container">

  <header class="header">
    <div class="brand-group">
      <div class="title-row">
        <h1>AI News Dashboard</h1>
      </div>
      <div class="subtitle">Snapshot: <strong>{snapshot}</strong></div>
    </div>
    <div class="header-actions">
      <button id="themeToggle" class="theme-toggle" aria-label="Cycle light, dusk, and dark mode">
        <!-- Detailed Gradient Sun SVG -->
        <svg class="sun-icon" width="22" height="22" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <radialGradient id="sunGrad" cx="50%" cy="50%" r="50%">
              <stop offset="0%" stop-color="#ffe066"/>
              <stop offset="70%" stop-color="#f59e0b"/>
              <stop offset="100%" stop-color="#d97706"/>
            </radialGradient>
            <linearGradient id="rayGrad" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stop-color="#fbbf24"/>
              <stop offset="100%" stop-color="#f59e0b"/>
            </linearGradient>
          </defs>
          <circle cx="12" cy="12" r="5" fill="url(#sunGrad)" stroke="#d97706" stroke-width="0.75"/>
          <path d="M12 1.5v2.5M12 20v2.5M1.5 12h2.5M20 12h2.5M4.58 4.58l1.77 1.77M17.65 17.65l1.77 1.77M4.58 19.42l1.77-1.77M17.65 6.35l1.77-1.77" 
                stroke="url(#rayGrad)" stroke-width="2" stroke-linecap="round"/>
        </svg>
        <!-- Detailed Gradient Moon SVG -->
        <svg class="moon-icon" width="22" height="22" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <linearGradient id="moonGrad" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stop-color="#fef08a"/>
              <stop offset="50%" stop-color="#fde047"/>
              <stop offset="100%" stop-color="#eab308"/>
            </linearGradient>
            <filter id="craterGlow" x="-20%" y="-20%" width="140%" height="140%">
              <feDropShadow dx="0" dy="0.5" stdDeviation="0.5" flood-color="#713f12" flood-opacity="0.3"/>
            </filter>
          </defs>
          <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" fill="url(#moonGrad)" stroke="#ca8a04" stroke-width="0.75"/>
          <circle cx="10" cy="11.5" r="1.3" fill="#ca8a04" opacity="0.35" filter="url(#craterGlow)"/>
          <path d="M19 4l.4.8.8.4-.8.4-.4.8-.4-.8-.8-.4.8-.4z" fill="#fef08a" opacity="0.9"/>
          <path d="M15 18l.3.6.6.3-.6.3-.3.6-.3-.6-.6-.3.6-.3z" fill="#fef9c3" opacity="0.8"/>
        </svg>
        <!-- Dusk Valley Glyph: setting sun behind twin mountain peaks with a rising star -->
        <svg class="dusk-icon" width="22" height="22" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <linearGradient id="duskIconGrad" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stop-color="#fbbf24"/>
              <stop offset="55%" stop-color="#f472b6"/>
              <stop offset="100%" stop-color="#7c3aed"/>
            </linearGradient>
          </defs>
          <circle cx="9" cy="13" r="4.5" fill="url(#duskIconGrad)"/>
          <path d="M2 18h20" stroke="#a855f7" stroke-width="1.2" stroke-linecap="round" opacity="0.5"/>
          <path d="M2 18l5-6 4 4 3-4 8 6" fill="none" stroke="#6d28d9" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M18 5l.5 1 1 .5-1 .5-.5 1-.5-1-1-.5 1-.5z" fill="#fde68a"/>
        </svg>
      </button>
    </div>
  </header>

  <main class="grid" role="main">

    <section class="col agents" aria-label="Agents news section">
      <div class="col-header">
        <div class="col-title-group">
          <div class="col-title-indicator"></div>
          <h2>Agents</h2>
        </div>
      </div>
{agents_html}
    </section>

    <section class="col infra" aria-label="Infrastructure news section">
      <div class="col-header">
        <div class="col-title-group">
          <div class="col-title-indicator"></div>
          <h2>Infra</h2>
        </div>
      </div>
{infra_html}
    </section>

    <section class="col applied" aria-label="Applied AI news section">
      <div class="col-header">
        <div class="col-title-group">
          <div class="col-title-indicator"></div>
          <h2>Applied AI</h2>
        </div>
      </div>
{applied_html}
    </section>

    <section class="col opensource" aria-label="Open source repositories section">
      <div class="col-header">
        <div class="col-title-group">
          <div class="col-title-indicator"></div>
          <h2>Open-source</h2>
        </div>
      </div>
{opensource_html}
    </section>

  </main>

  <footer>
    <div class="footer-copy">&copy; 2026 AI News Dashboard</div>
    <nav class="footer-links" aria-label="Footer navigation">
      <a href="https://www.kabyik.dev" target="_blank" rel="noopener">About me</a>
      <a href="https://github.com/Kabyik-Kayal/ai-news-dashboard" target="_blank" rel="noopener">GitHub</a>
    </nav>
  </footer>

</div>

<script>
  (function() {{
    const toggleBtn = document.getElementById('themeToggle');
    const themeOrder = ['light', 'dusk', 'dark'];

    toggleBtn.addEventListener('click', function() {{
      const activeTheme = document.documentElement.getAttribute('data-theme');
      const currentIndex = themeOrder.indexOf(activeTheme);
      const newTheme = themeOrder[(currentIndex + 1) % themeOrder.length];
      document.documentElement.setAttribute('data-theme', newTheme);
      localStorage.setItem('theme', newTheme);
    }});
  }})();
</script>

</body>
</html>
"""
    return html_content
