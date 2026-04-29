#!/usr/bin/env python3
"""
Generate SEO pages: index.html (browseable size directory) and sitemap.xml
for all popular placeholder image sizes.
"""
from pathlib import Path

BASE_DIR = Path(__file__).parent
BASE_URL = "https://placeholder.surge.sh"

# ── 50+ common sizes organized by category ──
SIZES = {
    "Social Media": [
        (1200, 628, "Facebook Link Share / OG Image"),
        (1080, 1080, "Instagram Square Post"),
        (1080, 1350, "Instagram Portrait Post"),
        (1080, 1920, "Instagram Story / Reel"),
        (1200, 630, "Facebook Event Cover"),
        (820, 312, "Facebook Cover Photo"),
        (1500, 500, "Twitter/X Header"),
        (1600, 900, "Twitter/X Post Image"),
        (744, 400, "Pinterest Pin (square-ish)"),
        (1000, 1500, "Pinterest Tall Pin"),
        (1584, 396, "LinkedIn Banner"),
        (1200, 1200, "LinkedIn Post Image"),
        (1280, 720, "YouTube Thumbnail"),
        (2560, 1440, "YouTube Channel Art"),
    ],
    "Ad Sizes": [
        (728, 90, "Leaderboard"),
        (300, 250, "Medium Rectangle"),
        (160, 600, "Wide Skyscraper"),
        (300, 600, "Half Page / Large Rectangle"),
        (320, 50, "Mobile Banner"),
        (320, 100, "Large Mobile Banner"),
        (970, 90, "Large Leaderboard"),
        (970, 250, "Billboard"),
        (468, 60, "Full Banner"),
        (234, 60, "Half Banner"),
        (120, 600, "Skyscraper"),
        (120, 240, "Vertical Banner"),
        (180, 150, "Small Rectangle"),
    ],
    "Banners & Headers": [
        (1920, 1080, "Full HD Hero Banner"),
        (2560, 1440, "2K Hero Banner"),
        (3840, 2160, "4K Hero Banner"),
        (1440, 900, "MacBook Wallpaper"),
        (1366, 768, "Laptop Wallpaper"),
        (1280, 360, "Website Header Banner"),
        (1170, 350, "Standard Web Banner"),
        (960, 300, "Sub-banner"),
        (600, 200, "Small Banner"),
    ],
    "Avatars & Profile Images": [
        (150, 150, "Standard Avatar"),
        (128, 128, "Forum Avatar"),
        (64, 64, "Small Avatar"),
        (48, 48, "Tiny Avatar"),
        (32, 32, "Favicon (PNG)"),
        (200, 200, "Large Avatar"),
        (400, 400, "XL Avatar / Profile Photo"),
    ],
    "Thumbnails & Cards": [
        (300, 200, "Blog Thumbnail"),
        (400, 300, "Standard Thumbnail"),
        (600, 400, "Large Thumbnail"),
        (250, 250, "Square Thumbnail"),
        (350, 150, "Card Thumbnail"),
        (500, 375, "Photo Thumbnail"),
        (640, 480, "VGA Preview"),
    ],
    "Common Web Dimensions": [
        (800, 600, "Classic 4:3"),
        (1024, 768, "XGA / iPad"),
        (640, 480, "VGA"),
        (400, 300, "Small Web Image"),
        (200, 200, "Square Web Image"),
        (500, 500, "Product Photo Square"),
        (600, 600, "Marketplace Listing"),
        (100, 100, "Icon Placeholder"),
        (250, 250, "Widget Placeholder"),
        (350, 200, "Embed Placeholder"),
    ],
    "Device Screens": [
        (1440, 900, "MacBook Air 13\""),
        (2560, 1600, "MacBook Pro 13\" Retina"),
        (1920, 1080, "Full HD Monitor"),
        (2732, 2048, "iPad Pro 12.9\""),
        (2048, 2732, "iPad Pro Portrait"),
        (1170, 2532, "iPhone 14 / 15"),
        (1179, 2556, "iPhone 15 Pro"),
        (1284, 2778, "iPhone 14 Pro Max"),
        (1080, 2400, "Android Standard"),
        (1080, 1920, "Android Portrait"),
        (720, 1280, "Android HD"),
        (1440, 3040, "Android QHD+"),
    ],
}


def dim_label(w: int, h: int) -> str:
    """Human-readable dimension string."""
    return f"{w}×{h}"


def slug(w: int, h: int) -> str:
    return f"{w}x{h}"


def build_index_html() -> str:
    categories_html = ""
    total = 0

    for cat_name, sizes in SIZES.items():
        total += len(sizes)
        rows = ""
        for w, h, desc in sizes:
            s = slug(w, h)
            dim = dim_label(w, h)
            rows += f"""
            <a href="/size/{s}" class="size-card" title="{dim} — {desc}">
                <div class="size-dim">{dim}</div>
                <div class="size-desc">{desc}</div>
                <div class="size-preview">
                    <img src="/{s}/3a7bd5/ffffff" alt="{dim} placeholder" loading="lazy" width="{min(w, 120)}" height="{min(h, 90)}">
                </div>
            </a>"""
        categories_html += f"""
        <section class="category" id="{cat_name.lower().replace(' & ', '-').replace(' ', '-')}">
            <h2>{cat_name}</h2>
            <div class="size-grid">{rows}
            </div>
        </section>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Placeholder Image Sizes — Complete Directory</title>
<meta name="description" content="Browse {total}+ popular placeholder image sizes for web design, social media, ads, and device mockups. Free instant download.">
<meta property="og:title" content="Placeholder Image Size Directory — {total}+ Sizes">
<meta property="og:description" content="Free placeholder images in every popular web dimension: social media, ad banners, avatars, devices, and more.">
<meta property="og:image" content="/1200x628/3a7bd5/ffffff">
<meta property="og:type" content="website">
<link rel="canonical" href="{BASE_URL}/sizes/">
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: #0a0a0a;
    color: #e0e0e0;
    line-height: 1.6;
    min-height: 100vh;
}}
a {{ color: #00d2ff; text-decoration: none; }}
a:hover {{ color: #3a7bd5; }}

/* Hero */
.hero {{
    text-align: center;
    padding: 60px 20px 40px;
    background: linear-gradient(135deg, #0a0a0a 0%, #111 50%, #0a0a0a 100%);
    border-bottom: 1px solid #1a1a1a;
}}
.hero h1 {{
    font-size: 2.4em;
    font-weight: 700;
    margin-bottom: 12px;
    background: linear-gradient(135deg, #00d2ff, #3a7bd5);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}}
.hero p {{
    font-size: 1.1em;
    color: #999;
    max-width: 600px;
    margin: 0 auto;
}}
.hero .stat {{
    display: inline-block;
    background: #1a1a1a;
    border: 1px solid #222;
    border-radius: 8px;
    padding: 8px 18px;
    margin: 8px;
    font-size: 0.95em;
}}
.hero .stat strong {{ color: #00d2ff; }}

/* Quick nav */
.quick-nav {{
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 8px;
    padding: 20px;
    background: #111;
    border-bottom: 1px solid #1a1a1a;
    position: sticky;
    top: 0;
    z-index: 10;
}}
.quick-nav a {{
    background: #1a1a1a;
    border: 1px solid #252525;
    border-radius: 20px;
    padding: 6px 16px;
    font-size: 0.85em;
    color: #ccc;
    transition: all 0.2s;
}}
.quick-nav a:hover {{
    background: #00d2ff;
    color: #0a0a0a;
    border-color: #00d2ff;
}}

/* Category */
.category {{
    max-width: 1100px;
    margin: 0 auto;
    padding: 40px 20px 20px;
}}
.category h2 {{
    font-size: 1.5em;
    margin-bottom: 20px;
    padding-bottom: 10px;
    border-bottom: 2px solid #1a1a1a;
    color: #fff;
}}
.category h2::before {{
    content: '';
    display: inline-block;
    width: 4px;
    height: 1em;
    background: linear-gradient(180deg, #00d2ff, #3a7bd5);
    border-radius: 2px;
    margin-right: 10px;
    vertical-align: middle;
}}

/* Size grid */
.size-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
    gap: 16px;
}}
.size-card {{
    display: block;
    background: #111;
    border: 1px solid #1a1a1a;
    border-radius: 12px;
    padding: 16px;
    transition: all 0.25s;
    text-align: center;
}}
.size-card:hover {{
    border-color: #00d2ff;
    transform: translateY(-2px);
    box-shadow: 0 4px 20px rgba(0, 210, 255, 0.1);
    text-decoration: none;
    color: #e0e0e0;
}}
.size-dim {{
    font-size: 1.2em;
    font-weight: 700;
    color: #fff;
    margin-bottom: 4px;
}}
.size-desc {{
    font-size: 0.82em;
    color: #888;
    margin-bottom: 12px;
}}
.size-preview {{
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 50px;
}}
.size-preview img {{
    max-width: 120px;
    max-height: 90px;
    border-radius: 6px;
}}

/* Footer */
.footer {{
    text-align: center;
    padding: 40px 20px;
    border-top: 1px solid #1a1a1a;
    color: #555;
    font-size: 0.85em;
}}
.footer a {{ color: #00d2ff; }}

/* Responsive */
@media (max-width: 600px) {{
    .hero h1 {{ font-size: 1.6em; }}
    .size-grid {{ grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 10px; }}
    .size-card {{ padding: 12px; }}
    .size-dim {{ font-size: 1em; }}
}}

/* Schema.org structured data */
</style>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "WebApplication",
  "name": "Placeholder Image API",
  "url": "{BASE_URL}",
  "description": "Free placeholder image generator with {total}+ popular sizes for web design, social media, ads, and device mockups.",
  "applicationCategory": "DesignApplication",
  "operatingSystem": "Web",
  "offers": [
    {{ "@type": "Offer", "price": "0", "priceCurrency": "EUR", "description": "Free tier – 100 images/day" }},
    {{ "@type": "Offer", "price": "3", "priceCurrency": "EUR", "description": "Basic tier – 2000 images/day" }},
    {{ "@type": "Offer", "price": "8", "priceCurrency": "EUR", "description": "Pro tier – 10000 images/day" }}
  ]
}}
</script>
</head>
<body>

<header class="hero">
    <h1>Placeholder Image Sizes</h1>
    <p> Browse {total} popular placeholder image dimensions organized by use case. Click any size to preview and download.</p>
    <div style="margin-top: 16px;">
        <span class="stat"><strong>{total}</strong> sizes</span>
        <span class="stat"><strong>{len(SIZES)}</strong> categories</span>
        <span class="stat">100% <strong>free</strong></span>
    </div>
</header>

<nav class="quick-nav">
    {''.join(f'<a href="#{c.lower().replace(" & ", "-").replace(" ", "-")}">{c}</a>' for c in SIZES)}
</nav>

{categories_html}

<footer class="footer">
    <p>Free placeholder images for web designers &amp; developers · <a href="/">Placeholder API Home</a> · <a href="/docs">API Docs</a></p>
    <p style="margin-top:8px;">{BASE_URL}/{'{'}width{'}'}x{'{'}height{'}'}/{'{'}bg{'}'}/{'{'}fg{'}'} — any size, any color, instant delivery</p>
</footer>

</body>
</html>"""


def build_sitemap_xml() -> str:
    """Generate sitemap.xml for Google Search Console."""
    urls = []
    # Root page
    urls.append(f"""  <url>
    <loc>{BASE_URL}/</loc>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>""")
    # Size index page
    urls.append(f"""  <url>
    <loc>{BASE_URL}/sizes/</loc>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>""")
    # Individual size pages
    for cat_name, sizes in SIZES.items():
        for w, h, desc in sizes:
            s = slug(w, h)
            dim = dim_label(w, h)
            urls.append(f"""  <url>
    <loc>{BASE_URL}/size/{s}</loc>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>""")

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(urls)}
</urlset>"""


def main():
    # Generate index.html
    index_html = build_index_html()
    index_path = BASE_DIR / "static" / "sizes" / "index.html"
    index_path.parent.mkdir(parents=True, exist_ok=True)
    index_path.write_text(index_html, encoding="utf-8")
    print(f"✅ index.html → {index_path} ({len(index_html):,} bytes)")

    # Generate sitemap.xml
    sitemap_xml = build_sitemap_xml()
    sitemap_path = BASE_DIR / "static" / "sitemap.xml"
    sitemap_path.parent.mkdir(parents=True, exist_ok=True)
    sitemap_path.write_text(sitemap_xml, encoding="utf-8")
    print(f"✅ sitemap.xml → {sitemap_path} ({len(sitemap_xml):,} bytes)")

    # Stats
    total_sizes = sum(len(v) for v in SIZES.values())
    print(f"\n📊 Generated {total_sizes} size pages across {len(SIZES)} categories")
    print(f"   Categories: {', '.join(SIZES.keys())}")


if __name__ == "__main__":
    main()