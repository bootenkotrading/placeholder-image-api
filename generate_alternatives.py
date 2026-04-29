#!/usr/bin/env python3
"""Generate SEO "alternatives" pages for the Placeholder Image API."""

import os
import json

OUTPUT_DIR = "/home/hermes/workspace/placeholder-api/static/alternatives"
API_BASE = "http://149.202.58.157:8892"
LANDING = "https://placeholder-api.surge.sh"

# Competitor data: domain, display name, weaknesses, description
COMPETITORS = [
    {
        "domain": "placeholder.com",
        "name": "Placeholder.com",
        "short": "placeholder.com",
        "tagline": "The original placeholder image service — but it's 2026 and there are better options.",
        "weaknesses": [
            "Limited customization options",
            "No text overlay customization",
            "Few supported formats",
            "Slow response times reported by users",
            "No gradient or advanced color support",
        ],
        "description": "Placeholder.com was one of the first placeholder image services on the web. While it served developers well for years, its feature set has stagnated. If you're looking for a modern, faster, and more customizable alternative, Placeholder Image API delivers on every front.",
    },
    {
        "domain": "placekitten.com",
        "name": "Placekitten",
        "short": "placekitten.com",
        "tagline": "Cute kitten photos are great — but what about real placeholder images for development?",
        "weaknesses": [
            "Only provides kitten photos, not proper placeholder images",
            "No text overlay or dimension labels",
            "No color customization",
            "Unreliable uptime",
            "No format options",
        ],
        "description": "Placekitten.com became famous for serving adorable cat photos at any size. While fun, it's not a serious placeholder image tool. Placeholder Image API gives you proper development placeholders with custom text, colors, formats, and blazing-fast responses.",
    },
    {
        "domain": "placehold.co",
        "name": "Placehold.co",
        "short": "placehold.co",
        "tagline": "Placehold.co is popular — but lacks the speed and features modern devs need.",
        "weaknesses": [
            "Limited color palette support",
            "No gradient backgrounds",
            "Text customization is minimal",
            "No advanced format support",
            "Occasional slow response times",
        ],
        "description": "Placehold.co is a widely-used placeholder image service with a clean interface. However, developers increasingly need more: faster responses, richer customization, and modern features. Placeholder Image API checks every box and then some.",
    },
    {
        "domain": "placebeast.com",
        "name": "Placebeast",
        "short": "placebeast.com",
        "tagline": "Animal photos are fun, but your mockups deserve proper placeholders.",
        "weaknesses": [
            "Only animal photos — not true placeholder images",
            "No dimension labels or text overlay",
            "No custom colors or backgrounds",
            "Limited size options",
            "No developer-focused features",
        ],
        "description": "Placebeast.com serves random animal photos as placeholders. While visually interesting, it doesn't offer the developer-focused features needed for serious prototyping. Placeholder Image API provides proper, customizable placeholder images built for developers.",
    },
    {
        "domain": "dummyimage.com",
        "name": "DummyImage",
        "short": "dummyimage.com",
        "tagline": "DummyImage was solid for its time — here's why developers are switching.",
        "weaknesses": [
            "Outdated interface and feature set",
            "Limited text customization",
            "No gradient backgrounds",
            "Fewer format options",
            "Slower than modern alternatives",
        ],
        "description": "DummyImage.com has been a reliable placeholder image generator for years. But the web has evolved, and developers need more: faster responses, richer customization, and modern format support. Placeholder Image API is the upgrade your workflow deserves.",
    },
    {
        "domain": "lorempixel.com",
        "name": "LoremPixel",
        "short": "lorempixel.com",
        "tagline": "Random stock photos aren't true placeholders. Time for a real alternative.",
        "weaknesses": [
            "Serves random stock photos, not placeholder images",
            "No custom text or dimension labels",
            "No background color customization",
            "Unpredictable content for mockups",
            "Often slow to load",
        ],
        "description": "LoremPixel.com provides random stock photos categorized by topic. While useful for visual mockups, it's not a proper placeholder image service. Placeholder Image API delivers clean, customizable, dimension-labeled placeholders designed for development.",
    },
    {
        "domain": "placeimg.com",
        "name": "PlaceIMG",
        "short": "placeimg.com",
        "tagline": "PlaceIMG was great for photos — but you need actual placeholder images.",
        "weaknesses": [
            "Photo-based, not true placeholder images",
            "No text overlay or labels",
            "No background color options",
            "Service has been unreliable",
            "No format flexibility",
        ],
        "description": "PlaceIMG.com offered categorized random photos for design mockups. However, for developers who need proper placeholder images with dimensions, text, and colors, it falls short. Placeholder Image API is the purpose-built tool for the job.",
    },
    {
        "domain": "fakeimg.pl",
        "name": "FakeImg.pl",
        "short": "fakeimg.pl",
        "tagline": "FakeImg.pl does the basics — but modern devs need more power.",
        "weaknesses": [
            "Minimal feature set",
            "Limited text and font options",
            "No gradient backgrounds",
            "Fewer format choices",
            "Smaller community and support",
        ],
        "description": "FakeImg.pl provides basic placeholder image generation with some text customization. It works for simple needs, but developers looking for speed, advanced customization, and a modern API will find Placeholder Image API a significant upgrade.",
    },
    {
        "domain": "fillscreen.com",
        "name": "FillScreen",
        "short": "fillscreen.com",
        "tagline": "FillScreen fills your screen — but does it fill your development needs?",
        "weaknesses": [
            "Limited to screen-filling images",
            "No custom dimensions or sizing",
            "No text overlay features",
            "No color customization for placeholders",
            "Not developer-API focused",
        ],
        "description": "FillScreen.com focuses on full-screen background images rather than placeholder image generation. For developers who need proper, dimensioned placeholder images with full customization, Placeholder Image API is the clear choice.",
    },
    {
        "domain": "placehold.it",
        "name": "Placehold.it",
        "short": "placehold.it",
        "tagline": "Placehold.it was a pioneer — but the world has moved on.",
        "weaknesses": [
            "Very limited customization",
            "No text overlay beyond basic dimensions",
            "No gradient or advanced styling",
            "Minimal format support",
            "Dated feature set compared to modern APIs",
        ],
        "description": "Placehold.it was one of the earliest placeholder image services and helped define the category. However, its feature set hasn't kept pace with modern development needs. Placeholder Image API brings you the speed, customization, and features that Placehold.it lacks.",
    },
]

# Feature comparison data
OUR_FEATURES = {
    "speed": {"label": "Response Speed", "us": "⚡ <50ms avg", "color": "#00d2ff"},
    "customization": {"label": "Customization", "us": "Full control — size, text, font, style", "color": "#00d2ff"},
    "colors": {"label": "Color Options", "us": "Any color + gradients", "color": "#00d2ff"},
    "text_overlay": {"label": "Text Overlay", "us": "Custom text, font size & color", "color": "#00d2ff"},
    "formats": {"label": "Output Formats", "us": "PNG, JPG, WebP, SVG", "color": "#00d2ff"},
    "pricing": {"label": "Pricing", "us": "Free & open — no limits", "color": "#00d2ff"},
}

# Mapping of competitor weakness keywords to feature keys
WEAKNESS_MAP = {
    "speed": ["slow", "faster", "uptime", "unreliable", "load"],
    "customization": ["customization", "customize", "limited", "minimal", "basic", "outdated"],
    "colors": ["color", "gradient", "background"],
    "text_overlay": ["text", "overlay", "label", "dimension"],
    "formats": ["format", "svg", "webp", "png"],
    "pricing": ["free", "price", "cost", "open"],
}


def slugify(domain: str) -> str:
    """Convert a domain like 'placeholder.com' to a slug like 'placeholder-com'."""
    return domain.replace(".", "-").replace(" ", "-").lower()


def classify_weaknesses(competitor: dict) -> dict:
    """Map competitor weaknesses to our feature strengths."""
    result = {}
    all_text = " ".join(competitor["weaknesses"]).lower()
    for key, keywords in WEAKNESS_MAP.items():
        for kw in keywords:
            if kw in all_text:
                result[key] = OUR_FEATURES[key]
                break
    # Ensure all features are represented
    for key in OUR_FEATURES:
        if key not in result:
            result[key] = OUR_FEATURES[key]
    return result


def generate_page(competitor: dict) -> str:
    slug = slugify(competitor["domain"])
    title = f"Best {competitor['name']} Alternative in 2026 — Placeholder Image API"
    desc = f"Looking for a {competitor['name']} alternative? Placeholder Image API is faster, more customizable, and free. Compare features, see live examples, and switch today."
    url = f"{LANDING}/alternatives/{slug}.html"

    features = classify_weaknesses(competitor)

    # Build feature comparison rows
    feature_rows = ""
    for key in ["speed", "customization", "colors", "text_overlay", "formats", "pricing"]:
        feat = features[key]
        feature_rows += f"""
        <div class="feature-row">
          <div class="feature-label">{feat['label']}</div>
          <div class="feature-them">{competitor['name']}</div>
          <div class="feature-us">{feat['us']}</div>
        </div>"""

    # Build weakness bullets
    weakness_bullets = ""
    for w in competitor["weaknesses"]:
        weakness_bullets += f"        <li>{w}</li>\n"

    # Live API examples
    examples = f"""
      <div class="examples-grid">
        <div class="example-card">
          <img src="{API_BASE}/800x600" alt="800x600 placeholder image" loading="lazy" />
          <code>GET /800x600</code>
        </div>
        <div class="example-card">
          <img src="{API_BASE}/400x300/00d2ff/ffffff?text=Hello+World" alt="Custom text placeholder" loading="lazy" />
          <code>GET /400x300/00d2ff/ffffff?text=Hello+World</code>
        </div>
        <div class="example-card">
          <img src="{API_BASE}/600x400/3a7bd5/ffffff" alt="Blue accent placeholder" loading="lazy" />
          <code>GET /600x400/3a7bd5/ffffff</code>
        </div>
        <div class="example-card">
          <img src="{API_BASE}/300x300/e74c3c/ffffff?text=Alert" alt="Red alert placeholder" loading="lazy" />
          <code>GET /300x300/e74c3c/ffffff?text=Alert</code>
        </div>
      </div>"""

    # Schema.org structured data
    schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": title,
        "description": desc,
        "url": url,
        "isPartOf": {
            "@type": "WebApplication",
            "name": "Placeholder Image API",
            "url": LANDING,
            "applicationCategory": "DeveloperApplication",
            "operatingSystem": "Web"
        },
        "about": {
            "@type": "SoftwareApplication",
            "name": competitor["name"],
            "url": f"https://{competitor['domain']}",
            "applicationCategory": "DeveloperApplication"
        },
        "mainEntity": {
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": f"Why switch from {competitor['name']} to Placeholder Image API?",
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": f"Placeholder Image API offers faster response times, richer customization (custom text, colors, gradients, font sizes), multiple output formats (PNG, JPG, WebP, SVG), and is completely free with no rate limits."
                    }
                },
                {
                    "@type": "Question",
                    "name": f"Is Placeholder Image API free?",
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": "Yes! Placeholder Image API is completely free and open. No rate limits, no API keys required, no hidden costs."
                    }
                },
                {
                    "@type": "Question",
                    "name": f"How do I migrate from {competitor['name']}?",
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": f"Simply replace the {competitor['name']} URL pattern with the Placeholder Image API URL pattern. Our API uses a simple, intuitive URL structure: {API_BASE}/WIDTHxHEIGHT/BGCOLOR/FGCOLOR?text=CUSTOM+TEXT"
                    }
                }
            ]
        }
    }, indent=2)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <meta name="description" content="{desc}" />
  <meta name="keywords" content="{competitor['name']} alternative, {competitor['short']} replacement, placeholder image API, placeholder image generator, dummy image, mockup image" />
  <meta name="robots" content="index, follow" />
  <link rel="canonical" href="{url}" />

  <!-- Open Graph -->
  <meta property="og:type" content="website" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{desc}" />
  <meta property="og:url" content="{url}" />
  <meta property="og:image" content="{API_BASE}/1200x630/0a0a0a/00d2ff?text={competitor['name']}+Alternative" />
  <meta property="og:site_name" content="Placeholder Image API" />

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{title}" />
  <meta name="twitter:description" content="{desc}" />
  <meta name="twitter:image" content="{API_BASE}/1200x630/0a0a0a/00d2ff?text={competitor['name']}+Alternative" />

  <!-- Schema.org -->
  <script type="application/ld+json">
{schema}
  </script>

  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
      background: #0a0a0a;
      color: #e0e0e0;
      line-height: 1.7;
    }}
    a {{ color: #00d2ff; text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}

    .container {{ max-width: 900px; margin: 0 auto; padding: 0 24px; }}

    /* Hero */
    .hero {{
      text-align: center;
      padding: 80px 0 48px;
      background: linear-gradient(135deg, #0a0a0a 0%, #111 50%, #0a0a0a 100%);
      border-bottom: 1px solid #1a1a1a;
    }}
    .hero h1 {{
      font-size: 2.4rem;
      font-weight: 800;
      background: linear-gradient(90deg, #00d2ff, #3a7bd5);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
      margin-bottom: 16px;
    }}
    .hero p {{
      font-size: 1.15rem;
      color: #aaa;
      max-width: 640px;
      margin: 0 auto;
    }}

    /* Tagline */
    .tagline {{
      text-align: center;
      font-size: 1.1rem;
      color: #888;
      padding: 32px 0;
      font-style: italic;
      border-bottom: 1px solid #1a1a1a;
    }}

    /* Sections */
    section {{ padding: 48px 0; }}
    section h2 {{
      font-size: 1.6rem;
      margin-bottom: 20px;
      color: #fff;
    }}
    section h3 {{
      font-size: 1.15rem;
      margin: 20px 0 10px;
      color: #ccc;
    }}

    /* Weaknesses */
    .weaknesses ul {{
      list-style: none;
      padding: 0;
    }}
    .weaknesses li {{
      position: relative;
      padding: 8px 0 8px 28px;
      color: #bbb;
    }}
    .weaknesses li::before {{
      content: '✗';
      position: absolute;
      left: 0;
      color: #e74c3c;
      font-weight: 700;
    }}

    /* Feature comparison table */
    .comparison {{
      display: grid;
      gap: 2px;
      background: #1a1a1a;
      border-radius: 12px;
      overflow: hidden;
      margin-top: 20px;
    }}
    .feature-row {{
      display: grid;
      grid-template-columns: 160px 1fr 1fr;
      gap: 2px;
    }}
    .feature-row > div {{
      padding: 14px 18px;
      background: #0f0f0f;
    }}
    .feature-label {{
      font-weight: 600;
      color: #888;
      display: flex;
      align-items: center;
    }}
    .feature-them {{
      color: #777;
      display: flex;
      align-items: center;
    }}
    .feature-us {{
      color: #00d2ff;
      font-weight: 600;
      display: flex;
      align-items: center;
    }}
    .comparison-header {{
      display: grid;
      grid-template-columns: 160px 1fr 1fr;
      gap: 2px;
      margin-bottom: 2px;
    }}
    .comparison-header > div {{
      padding: 14px 18px;
      background: #111;
      font-weight: 700;
    }}
    .comparison-header .them-col {{ color: #888; text-align: center; }}
    .comparison-header .us-col {{ color: #00d2ff; text-align: center; }}

    /* Examples */
    .examples-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 20px;
      margin-top: 20px;
    }}
    .example-card {{
      background: #111;
      border-radius: 12px;
      overflow: hidden;
      border: 1px solid #1a1a1a;
      text-align: center;
    }}
    .example-card img {{
      width: 100%;
      height: auto;
      display: block;
    }}
    .example-card code {{
      display: block;
      padding: 12px;
      font-size: 0.8rem;
      color: #00d2ff;
      background: #0a0a0a;
      word-break: break-all;
    }}

    /* Quick start */
    .quick-start {{
      background: #111;
      border: 1px solid #1a1a1a;
      border-radius: 12px;
      padding: 28px 32px;
      margin-top: 20px;
    }}
    .quick-start code {{
      display: block;
      background: #0a0a0a;
      padding: 16px;
      border-radius: 8px;
      margin-top: 12px;
      font-size: 0.9rem;
      color: #00d2ff;
      overflow-x: auto;
    }}

    /* CTA */
    .cta {{
      text-align: center;
      padding: 64px 0;
      border-top: 1px solid #1a1a1a;
    }}
    .cta h2 {{
      font-size: 2rem;
      margin-bottom: 12px;
    }}
    .cta p {{
      color: #888;
      margin-bottom: 28px;
      font-size: 1.1rem;
    }}
    .cta-button {{
      display: inline-block;
      padding: 14px 36px;
      background: linear-gradient(135deg, #00d2ff, #3a7bd5);
      color: #0a0a0a;
      font-weight: 700;
      font-size: 1.05rem;
      border-radius: 8px;
      text-decoration: none;
      transition: transform 0.2s, box-shadow 0.2s;
    }}
    .cta-button:hover {{
      transform: translateY(-2px);
      box-shadow: 0 8px 30px rgba(0, 210, 255, 0.3);
      text-decoration: none;
    }}

    /* FAQ */
    .faq-item {{
      margin-bottom: 18px;
    }}
    .faq-item h3 {{
      color: #fff;
      cursor: default;
    }}
    .faq-item p {{
      color: #aaa;
    }}

    /* Footer */
    footer {{
      text-align: center;
      padding: 32px 0;
      color: #555;
      font-size: 0.85rem;
      border-top: 1px solid #1a1a1a;
    }}

    @media (max-width: 640px) {{
      .hero h1 {{ font-size: 1.7rem; }}
      .feature-row, .comparison-header {{
        grid-template-columns: 1fr;
      }}
      .feature-them, .feature-us, .feature-label {{
        padding: 8px 14px;
        font-size: 0.9rem;
      }}
    }}
  </style>
</head>
<body>

  <div class="hero">
    <div class="container">
      <h1>Best {competitor['name']} Alternative in 2026</h1>
      <p>{desc}</p>
    </div>
  </div>

  <div class="tagline container">
    "{competitor['tagline']}"
  </div>

  <section class="container weaknesses">
    <h2>Problems with {competitor['name']}</h2>
    <p>Developers love {competitor['name']}, but it has real limitations that hold modern workflows back:</p>
    <ul>
{weakness_bullets}    </ul>
  </section>

  <section class="container" id="comparison">
    <h2>{competitor['name']} vs Placeholder Image API</h2>
    <p>See how Placeholder Image API compares feature-by-feature:</p>

    <div class="comparison">
      <div class="comparison-header">
        <div>Feature</div>
        <div class="them-col">{competitor['name']}</div>
        <div class="us-col">Placeholder Image API</div>
      </div>
{feature_rows}
    </div>
  </section>

  <section class="container" id="examples">
    <h2>Live Examples</h2>
    <p>Real images served right now by the Placeholder Image API — no tricks:</p>
{examples}
  </section>

  <section class="container" id="quick-start">
    <h2>Migrate in Seconds</h2>
    <p>Switching from {competitor['name']} is trivial. Just update your image URLs:</p>
    <div class="quick-start">
      <strong>Before ({competitor['name']}):</strong>
      <code>https://{competitor['domain']}/800x600</code>
      <strong style="display:block; margin-top:16px;">After (Placeholder Image API):</strong>
      <code>{API_BASE}/800x600</code>
      <strong style="display:block; margin-top:16px;">With custom text and colors:</strong>
      <code>{API_BASE}/800x600/3a7bd5/ffffff?text=My+App</code>
    </div>
  </section>

  <section class="container" id="faq">
    <h2>Frequently Asked Questions</h2>

    <div class="faq-item">
      <h3>Why should I switch from {competitor['name']}?</h3>
      <p>Placeholder Image API offers faster response times, richer customization (custom text, colors, gradients, font sizes), multiple output formats (PNG, JPG, WebP, SVG), and is completely free with no rate limits.</p>
    </div>

    <div class="faq-item">
      <h3>Is Placeholder Image API free?</h3>
      <p>Yes! Placeholder Image API is completely free and open. No API keys required, no rate limits, no hidden costs.</p>
    </div>

    <div class="faq-item">
      <h3>How do I migrate from {competitor['name']}?</h3>
      <p>Simply replace the {competitor['name']} URL pattern with the Placeholder Image API URL. Our intuitive URL structure makes migration a breeze: <code>{API_BASE}/WIDTHxHEIGHT/BGCOLOR/FGCOLOR?text=CUSTOM+TEXT</code></p>
    </div>

    <div class="faq-item">
      <h3>What output formats are supported?</h3>
      <p>Placeholder Image API supports PNG, JPG, WebP, and SVG — giving you flexibility for any project.</p>
    </div>
  </section>

  <div class="cta container" id="try">
    <h2>Ready to Make the Switch?</h2>
    <p>Try Placeholder Image API now — it's free, fast, and built for developers.</p>
    <a href="{LANDING}" class="cta-button">Try Placeholder Image API →</a>
  </div>

  <footer>
    <div class="container">
      <p>Placeholder Image API — The modern placeholder image service for developers.</p>
      <p style="margin-top:8px;"><a href="{LANDING}/alternatives/">← All Alternatives</a></p>
    </div>
  </footer>

</body>
</html>"""

    return html


def generate_index() -> str:
    title = "Placeholder Image Alternatives — All Competitor Comparisons | Placeholder Image API"
    desc = "Comparing Placeholder Image API against all popular placeholder image services: placeholder.com, placekitten, placehold.co, and more. Find the best alternative for your workflow."
    url = f"{LANDING}/alternatives/"

    cards = ""
    for comp in COMPETITORS:
        slug = slugify(comp["domain"])
        card_url = f"{LANDING}/alternatives/{slug}.html"
        cards += f"""
      <a href="{slug}.html" class="alt-card">
        <div class="alt-card-domain">{comp['domain']}</div>
        <div class="alt-card-name">{comp['name']}</div>
        <div class="alt-card-arrow">→</div>
      </a>"""

    schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": title,
        "description": desc,
        "url": url,
        "isPartOf": {
            "@type": "WebApplication",
            "name": "Placeholder Image API",
            "url": LANDING,
            "applicationCategory": "DeveloperApplication",
            "operatingSystem": "Web"
        }
    }, indent=2)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <meta name="description" content="{desc}" />
  <meta name="keywords" content="placeholder image alternative, placeholder.com alternative, placekitten alternative, placehold.co alternative, dummy image alternative" />
  <meta name="robots" content="index, follow" />
  <link rel="canonical" href="{url}" />

  <meta property="og:type" content="website" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{desc}" />
  <meta property="og:url" content="{url}" />
  <meta property="og:image" content="{API_BASE}/1200x630/0a0a0a/00d2ff?text=Placeholder+Alternatives" />
  <meta property="og:site_name" content="Placeholder Image API" />

  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{title}" />
  <meta name="twitter:description" content="{desc}" />

  <script type="application/ld+json">
{schema}
  </script>

  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
      background: #0a0a0a;
      color: #e0e0e0;
      line-height: 1.7;
    }}
    a {{ color: #00d2ff; text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}

    .container {{ max-width: 900px; margin: 0 auto; padding: 0 24px; }}

    .hero {{
      text-align: center;
      padding: 80px 0 48px;
      background: linear-gradient(135deg, #0a0a0a 0%, #111 50%, #0a0a0a 100%);
      border-bottom: 1px solid #1a1a1a;
    }}
    .hero h1 {{
      font-size: 2.4rem;
      font-weight: 800;
      background: linear-gradient(90deg, #00d2ff, #3a7bd5);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
      margin-bottom: 16px;
    }}
    .hero p {{
      font-size: 1.15rem;
      color: #aaa;
      max-width: 640px;
      margin: 0 auto;
    }}

    section {{ padding: 48px 0; }}
    section h2 {{ font-size: 1.6rem; margin-bottom: 20px; color: #fff; }}

    .alt-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
      gap: 16px;
      margin-top: 20px;
    }}
    .alt-card {{
      display: flex;
      align-items: center;
      gap: 14px;
      background: #111;
      border: 1px solid #1a1a1a;
      border-radius: 12px;
      padding: 20px 22px;
      text-decoration: none;
      transition: border-color 0.2s, transform 0.2s;
    }}
    .alt-card:hover {{
      border-color: #00d2ff;
      transform: translateY(-2px);
      text-decoration: none;
    }}
    .alt-card-domain {{
      font-family: monospace;
      color: #888;
      font-size: 0.85rem;
    }}
    .alt-card-name {{
      flex: 1;
      font-weight: 600;
      color: #e0e0e0;
    }}
    .alt-card-arrow {{
      color: #00d2ff;
      font-size: 1.2rem;
      font-weight: 700;
    }}

    .cta {{
      text-align: center;
      padding: 64px 0;
      border-top: 1px solid #1a1a1a;
    }}
    .cta h2 {{ font-size: 2rem; margin-bottom: 12px; }}
    .cta p {{ color: #888; margin-bottom: 28px; font-size: 1.1rem; }}
    .cta-button {{
      display: inline-block;
      padding: 14px 36px;
      background: linear-gradient(135deg, #00d2ff, #3a7bd5);
      color: #0a0a0a;
      font-weight: 700;
      font-size: 1.05rem;
      border-radius: 8px;
      text-decoration: none;
      transition: transform 0.2s, box-shadow 0.2s;
    }}
    .cta-button:hover {{
      transform: translateY(-2px);
      box-shadow: 0 8px 30px rgba(0, 210, 255, 0.3);
      text-decoration: none;
    }}

    footer {{
      text-align: center;
      padding: 32px 0;
      color: #555;
      font-size: 0.85rem;
      border-top: 1px solid #1a1a1a;
    }}
  </style>
</head>
<body>

  <div class="hero">
    <div class="container">
      <h1>Placeholder Image Service Alternatives</h1>
      <p>See how Placeholder Image API compares to every popular placeholder image service. Find the best tool for your development workflow.</p>
    </div>
  </div>

  <section class="container">
    <h2>All Comparisons</h2>
    <div class="alt-grid">
{cards}
    </div>
  </section>

  <div class="cta container">
    <h2>Try Placeholder Image API</h2>
    <p>Free, fast, and built for developers — no signup required.</p>
    <a href="{LANDING}" class="cta-button">Get Started →</a>
  </div>

  <footer>
    <div class="container">
      <p>Placeholder Image API — The modern placeholder image service for developers.</p>
    </div>
  </footer>

</body>
</html>"""

    return html


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Generate individual pages
    for comp in COMPETITORS:
        slug = slugify(comp["domain"])
        html = generate_page(comp)
        path = os.path.join(OUTPUT_DIR, f"{slug}.html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"  ✓ {slug}.html")

    # Generate index
    index_html = generate_index()
    index_path = os.path.join(OUTPUT_DIR, "index.html")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(index_html)
    print(f"  ✓ index.html")

    print(f"\nDone! Generated {len(COMPETITORS) + 1} pages in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()