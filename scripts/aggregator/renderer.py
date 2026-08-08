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
    if (savedTheme === 'dark' || (!savedTheme && window.matchMedia('(prefers-color-scheme: dark)').matches)) {{
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

  .sun-icon, .moon-icon {{
    position: absolute;
    transition: transform 0.5s cubic-bezier(0.34, 1.56, 0.64, 1), opacity 0.4s ease;
  }}

  /* Light Mode: Radiant Sun in Sky, Moon set below horizon */
  :root .sun-icon {{
    transform: translateY(0) rotate(0deg) scale(1);
    opacity: 1;
  }}
  :root .moon-icon {{
    transform: translateY(30px) rotate(-90deg) scale(0.4);
    opacity: 0;
  }}

  /* Dark Mode: Sun sets down into horizon, Crescent Moon rises up into midnight sky */
  [data-theme="dark"] .sun-icon {{
    transform: translateY(30px) rotate(90deg) scale(0.4);
    opacity: 0;
  }}
  [data-theme="dark"] .moon-icon {{
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
    display: flex;
    flex-direction: column;
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
    body, .col, .item, .item-title, .theme-toggle, .sun-icon, .moon-icon {{
      transition: none !important;
      animation: none !important;
    }}
  }}
</style>
</head>
<body>

<div class="container">

  <header class="header">
    <div class="brand-group">
      <div class="title-row">
        <h1>AI News Dashboard</h1>
      </div>
      <div class="subtitle">Snapshot: <strong>{snapshot}</strong></div>
    </div>
    <div class="header-actions">
      <button id="themeToggle" class="theme-toggle" aria-label="Toggle dark/light mode">
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

    toggleBtn.addEventListener('click', function() {{
      const activeTheme = document.documentElement.getAttribute('data-theme');
      const newTheme = activeTheme === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', newTheme);
      localStorage.setItem('theme', newTheme);
    }});
  }})();
</script>

</body>
</html>
"""
    return html_content
