"""
Placeholder Image API - FastAPI application
Generates custom placeholder images on-the-fly with caching, API keys, and watermark tier system.
"""
import os
import io
import re
import hashlib
import sqlite3
import time
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from functools import lru_cache

from fastapi import FastAPI, Request, Response, HTTPException, Depends, Query
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from PIL import Image, ImageDraw, ImageFont

# ── Config ──
BASE_DIR = Path(__file__).parent
CACHE_DIR = BASE_DIR / "cache"
LOG_DIR = BASE_DIR / "logs"
DB_PATH = BASE_DIR / "data.db"
CACHE_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "api.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("placeholder-api")

# ── Database ──
def get_db():
    db = sqlite3.connect(str(DB_PATH))
    db.row_factory = sqlite3.Row
    return db

def init_db():
    db = get_db()
    db.executescript("""
        CREATE TABLE IF NOT EXISTS api_keys (
            key TEXT PRIMARY KEY,
            email TEXT,
            tier TEXT DEFAULT 'free',
            created_at TEXT DEFAULT (datetime('now')),
            requests_today INTEGER DEFAULT 0,
            total_requests INTEGER DEFAULT 0,
            last_reset TEXT DEFAULT (date('now')),
            active INTEGER DEFAULT 1
        );
        CREATE TABLE IF NOT EXISTS request_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            api_key TEXT,
            endpoint TEXT,
            width INTEGER,
            height INTEGER,
            bg_color TEXT,
            text_color TEXT,
            text TEXT,
            format TEXT,
            ip TEXT,
            user_agent TEXT,
            timestamp TEXT DEFAULT (datetime('now')),
            response_time_ms INTEGER,
            cached INTEGER DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS daily_stats (
            date TEXT PRIMARY KEY,
            total_requests INTEGER DEFAULT 0,
            unique_ips INTEGER DEFAULT 0,
            unique_keys INTEGER DEFAULT 0,
            cache_hits INTEGER DEFAULT 0,
            avg_response_ms REAL DEFAULT 0,
            bandwidth_bytes INTEGER DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS revenue (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT,
            amount REAL,
            currency TEXT DEFAULT 'EUR',
            description TEXT,
            timestamp TEXT DEFAULT (datetime('now'))
        );
        CREATE INDEX IF NOT EXISTS idx_log_timestamp ON request_log(timestamp);
        CREATE INDEX IF NOT EXISTS idx_log_api_key ON request_log(api_key);
    """)
    db.commit()
    db.close()
    logger.info("Database initialized")

init_db()

# ── App ──
app = FastAPI(
    title="Placeholder Image API",
    description="Generate custom placeholder images for your designs and prototypes. Free with watermark, premium without.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# ── Static files (generated SEO pages) ──
STATIC_DIR = BASE_DIR / "static"
if STATIC_DIR.is_dir():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# ── Rate Limiting ──
RATE_LIMITS = {
    "free": 100,      # 100 req/day
    "basic": 2000,    # 2000 req/day  (€3/mo)
    "pro": 10000,     # 10000 req/day (€8/mo)
    "enterprise": -1  # unlimited
}

def check_rate_limit(api_key: str = None):
    """Check and enforce rate limits. Returns (allowed, tier, remaining)"""
    if not api_key:
        return True, "anonymous", 50  # 50 req/day for anonymous
    
    db = get_db()
    row = db.execute("SELECT * FROM api_keys WHERE key=? AND active=1", (api_key,)).fetchone()
    db.close()
    
    if not row:
        return False, "invalid", 0
    
    # Reset daily counter
    today = datetime.now().strftime("%Y-%m-%d")
    if row["last_reset"] != today:
        db = get_db()
        db.execute("UPDATE api_keys SET requests_today=0, last_reset=? WHERE key=?", (today, api_key))
        db.commit()
        db.close()
        used_today = 0
    else:
        used_today = row["requests_today"]
    
    tier = row["tier"]
    limit = RATE_LIMITS.get(tier, 100)
    
    if limit == -1:  # unlimited
        return True, tier, -1
    
    remaining = max(0, limit - used_today)
    if used_today >= limit:
        return False, tier, 0
    
    return True, tier, remaining

def increment_usage(api_key: str):
    if not api_key:
        return
    db = get_db()
    db.execute("UPDATE api_keys SET requests_today=requests_today+1, total_requests=total_requests+1 WHERE key=?", (api_key,))
    db.commit()
    db.close()

# ── Image Generation ──
def parse_color(color_str: str) -> tuple:
    """Parse color string (hex or named) to RGB tuple"""
    color_str = color_str.strip().lstrip('#')
    
    named_colors = {
        'red': (255, 59, 48), 'orange': (255, 149, 0), 'yellow': (255, 204, 0),
        'green': (52, 199, 89), 'teal': (90, 200, 250), 'blue': (0, 122, 255),
        'indigo': (88, 86, 214), 'purple': (175, 82, 222), 'pink': (255, 45, 85),
        'gray': (142, 142, 147), 'grey': (142, 142, 147), 'white': (255, 255, 255),
        'black': (0, 0, 0), 'brown': (162, 132, 94), 'cyan': (50, 173, 230),
        'magenta': (255, 45, 85), 'lime': (52, 199, 89), 'navy': (0, 0, 128),
        'olive': (128, 128, 0), 'maroon': (128, 0, 0), 'coral': (255, 127, 80),
        'salmon': (250, 128, 114), 'gold': (255, 215, 0), 'silver': (192, 192, 192),
    }
    
    if color_str.lower() in named_colors:
        return named_colors[color_str.lower()]
    
    # 6-digit hex
    if len(color_str) == 6:
        return tuple(int(color_str[i:i+2], 16) for i in (0, 2, 4))
    # 3-digit hex
    if len(color_str) == 3:
        return tuple(int(c*2, 16) for c in color_str)
    
    return (204, 204, 204)  # default gray

def get_font(size: int) -> ImageFont.FreeTypeFont:
    """Get a font, falling back through system fonts"""
    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/ubuntu/Ubuntu-B.ttf",
    ]
    for fp in font_paths:
        if os.path.exists(fp):
            try:
                return ImageFont.truetype(fp, size)
            except Exception:
                continue
    return ImageFont.load_default()

def generate_placeholder(
    width: int, height: int,
    bg_color: str = "cccccc",
    text_color: str = "666666",
    text: str = None,
    fmt: str = "png",
    add_watermark: bool = True,
    font_size: int = None
) -> bytes:
    """Generate a placeholder image and return as bytes"""
    # Clamp dimensions
    width = max(1, min(4000, width))
    height = max(1, min(4000, height))
    
    # Check cache
    cache_key = hashlib.md5(f"{width}x{height}_{bg_color}_{text_color}_{text}_{fmt}_{add_watermark}".encode()).hexdigest()
    cache_file = CACHE_DIR / f"{cache_key}.{fmt}"
    if cache_file.exists():
        # Check age (max 7 days)
        if time.time() - cache_file.stat().st_mtime < 604800:
            return cache_file.read_bytes()
    
    # Parse colors
    bg_rgb = parse_color(bg_color)
    text_rgb = parse_color(text_color)
    
    # Create image
    img = Image.new("RGB", (width, height), bg_rgb)
    draw = ImageDraw.Draw(img)
    
    # Auto-text
    if text is None:
        text = f"{width}×{height}"
    
    # Font size
    if font_size is None:
        font_size = max(12, min(width, height) // 8)
    
    font = get_font(font_size)
    
    # Draw crosshair lines (subtle)
    line_color = tuple(max(0, c - 25) for c in bg_rgb)
    if width > 40 and height > 40:
        draw.line([(0, height//2), (width, height//2)], fill=line_color, width=1)
        draw.line([(width//2, 0), (width//2, height)], fill=line_color, width=1)
    
    # Draw text
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    x = (width - text_w) // 2
    y = (height - text_h) // 2
    draw.text((x, y), text, fill=text_rgb, font=font)
    
    # Watermark for free tier
    if add_watermark and width > 120 and height > 40:
        wm_text = "placeholder.surge.sh"
        wm_size = max(8, min(14, width // 25))
        wm_font = get_font(wm_size)
        wm_bbox = draw.textbbox((0, 0), wm_text, font=wm_font)
        wm_w = wm_bbox[2] - wm_bbox[0]
        draw.text((width - wm_w - 4, height - wm_size - 4), wm_text, fill=text_rgb, font=wm_font)
    
    # Save to buffer + cache
    buffer = io.BytesIO()
    fmt_upper = fmt.upper()
    if fmt_upper == "JPG":
        fmt_upper = "JPEG"
    save_kwargs = {"format": fmt_upper}
    if fmt_upper == "JPEG":
        save_kwargs["quality"] = 85
    if fmt_upper == "PNG":
        save_kwargs["optimize"] = True
    
    img.save(buffer, **save_kwargs)
    img_bytes = buffer.getvalue()
    
    # Write cache
    try:
        cache_file.write_bytes(img_bytes)
    except Exception:
        pass
    
    return img_bytes

# ── API Endpoints ──

@app.get("/")
async def landing_page(request: Request):
    """Landing page with docs and API explorer"""
    db = get_db()
    stats = db.execute("SELECT * FROM daily_stats ORDER BY date DESC LIMIT 1").fetchone()
    total_images = db.execute("SELECT COUNT(*) as c FROM request_log").fetchone()["c"]
    db.close()
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Placeholder Image API — Free Custom Placeholder Images</title>
    <meta name="description" content="Generate custom placeholder images instantly. Free API for developers and designers. Any size, any color, any format.">
    <meta property="og:title" content="Placeholder Image API">
    <meta property="og:description" content="Free custom placeholder images for developers and designers">
    <meta property="og:type" content="website">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0a0a0a; color: #e0e0e0; }}
        .hero {{ text-align: center; padding: 60px 20px 40px; background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%); }}
        .hero h1 {{ font-size: 3em; margin-bottom: 16px; background: linear-gradient(90deg, #00d2ff, #3a7bd5); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
        .hero p {{ font-size: 1.2em; color: #a0a0a0; max-width: 600px; margin: 0 auto 30px; }}
        .try-it {{ background: #111; border-radius: 16px; padding: 40px; max-width: 800px; margin: -20px auto 40px; position: relative; box-shadow: 0 20px 60px rgba(0,0,0,0.5); }}
        .preview-area {{ text-align: center; margin: 20px 0; min-height: 200px; display: flex; align-items: center; justify-content: center; background: #1a1a1a; border-radius: 12px; padding: 20px; }}
        .preview-area img {{ max-width: 100%; border-radius: 8px; box-shadow: 0 4px 20px rgba(0,0,0,0.3); }}
        .controls {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 16px; margin-bottom: 20px; }}
        .control-group label {{ display: block; font-size: 0.85em; color: #888; margin-bottom: 6px; text-transform: uppercase; letter-spacing: 1px; }}
        .control-group input, .control-group select {{ width: 100%; padding: 10px 14px; background: #222; border: 1px solid #333; border-radius: 8px; color: #fff; font-size: 1em; }}
        .control-group input:focus {{ border-color: #3a7bd5; outline: none; }}
        .url-output {{ background: #1a1a1a; border-radius: 8px; padding: 16px; font-family: 'Fira Code', monospace; font-size: 0.9em; word-break: break-all; color: #00d2ff; margin-top: 16px; }}
        .url-output code {{ color: #00d2ff; }}
        .pricing {{ max-width: 900px; margin: 40px auto; padding: 0 20px; }}
        .pricing h2 {{ text-align: center; font-size: 2em; margin-bottom: 30px; }}
        .pricing-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; }}
        .price-card {{ background: #111; border-radius: 12px; padding: 30px; text-align: center; border: 1px solid #222; transition: transform 0.2s, border-color 0.2s; }}
        .price-card:hover {{ transform: translateY(-4px); border-color: #3a7bd5; }}
        .price-card h3 {{ font-size: 1.3em; margin-bottom: 10px; }}
        .price {{ font-size: 2.5em; font-weight: bold; margin: 16px 0; }}
        .price small {{ font-size: 0.4em; color: #888; }}
        .features {{ list-style: none; text-align: left; margin-top: 16px; }}
        .features li {{ padding: 6px 0; border-bottom: 1px solid #1a1a1a; font-size: 0.9em; }}
        .features li::before {{ content: "✓ "; color: #00d2ff; }}
        .cta-btn {{ display: inline-block; margin-top: 20px; padding: 12px 28px; background: linear-gradient(90deg, #00d2ff, #3a7bd5); color: #fff; border: none; border-radius: 8px; font-size: 1em; cursor: pointer; text-decoration: none; }}
        .stats {{ text-align: center; padding: 40px 20px; }}
        .stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 20px; max-width: 600px; margin: 0 auto; }}
        .stat {{ padding: 20px; }}
        .stat .number {{ font-size: 2em; font-weight: bold; color: #00d2ff; }}
        .stat .label {{ font-size: 0.85em; color: #888; margin-top: 4px; }}
        .examples {{ max-width: 800px; margin: 40px auto; padding: 0 20px; }}
        .examples h2 {{ text-align: center; margin-bottom: 20px; }}
        .example-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; }}
        .example {{ text-align: center; }}
        .example img {{ border-radius: 8px; margin-bottom: 8px; }}
        .example code {{ font-size: 0.8em; color: #888; }}
        footer {{ text-align: center; padding: 40px 20px; color: #555; font-size: 0.85em; border-top: 1px solid #1a1a1a; }}
    </style>
</head>
<body>
    <div class="hero">
        <h1>Placeholder Image API</h1>
        <p>Generate custom placeholder images instantly. Any size, any color, any text. Free for developers.</p>
    </div>
    
    <div class="try-it">
        <h2 style="margin-bottom:20px; text-align:center;">🎯 Try It Now</h2>
        <div class="controls">
            <div class="control-group">
                <label>Width</label>
                <input type="number" id="inp-w" value="600" min="1" max="4000">
            </div>
            <div class="control-group">
                <label>Height</label>
                <input type="number" id="inp-h" value="400" min="1" max="4000">
            </div>
            <div class="control-group">
                <label>Background</label>
                <input type="text" id="inp-bg" value="3a7bd5" placeholder="hex or name">
            </div>
            <div class="control-group">
                <label>Text Color</label>
                <input type="text" id="inp-fg" value="ffffff" placeholder="hex or name">
            </div>
            <div class="control-group">
                <label>Text</label>
                <input type="text" id="inp-text" value="" placeholder="auto: WxH">
            </div>
            <div class="control-group">
                <label>Format</label>
                <select id="inp-fmt">
                    <option value="png">PNG</option>
                    <option value="jpg">JPG</option>
                    <option value="webp">WebP</option>
                </select>
            </div>
        </div>
        <div class="preview-area" id="preview">
            <img src="/600x400/3a7bd5/ffffff" alt="Preview">
        </div>
        <div class="url-output">
            <code id="url-out">https://placeholder.surge.sh/600x400/3a7bd5/ffffff</code>
        </div>
    </div>

    <div class="examples">
        <h2>📐 Examples</h2>
        <div class="example-grid">
            <div class="example"><img src="/300x200/red/white" alt="Red"><br><code>/300x200/red/white</code></div>
            <div class="example"><img src="/800x600/000000/00d2ff" alt="Dark"><br><code>/800x600/000000/00d2ff</code></div>
            <div class="example"><img src="/150x150/ff6600/ffffff?text=Avatar" alt="Avatar"><br><code>/150x150/ff6600/fff?text=Avatar</code></div>
            <div class="example"><img src="/1200x300/1a1a2e/00d2ff?text=Banner" alt="Banner"><br><code>/1200x300/1a1a2e/00d2ff?text=Banner</code></div>
        </div>
    </div>

    <div class="pricing">
        <h2>💰 Pricing</h2>
        <div class="pricing-grid">
            <div class="price-card">
                <h3>Free</h3>
                <div class="price">$0<small>/mo</small></div>
                <ul class="features">
                    <li>100 images/day</li>
                    <li>All sizes & formats</li>
                    <li>Named colors</li>
                    <li>Small watermark</li>
                </ul>
                <a href="#" class="cta-btn">Get Started</a>
            </div>
            <div class="price-card" style="border-color: #3a7bd5;">
                <h3>Basic</h3>
                <div class="price">€3<small>/mo</small></div>
                <ul class="features">
                    <li>2,000 images/day</li>
                    <li>No watermark</li>
                    <li>Custom text</li>
                    <li>Priority caching</li>
                </ul>
                <a href="https://bootenko.gumroad.com/l/placeholder-basic" class="cta-btn">Subscribe</a>
            </div>
            <div class="price-card" style="border-color: #00d2ff;">
                <h3>Pro</h3>
                <div class="price">€8<small>/mo</small></div>
                <ul class="features">
                    <li>10,000 images/day</li>
                    <li>No watermark</li>
                    <li>Custom fonts</li>
                    <li>API key auth</li>
                    <li>Usage dashboard</li>
                </ul>
                <a href="https://bootenko.gumroad.com/l/placeholder-pro" class="cta-btn">Subscribe</a>
            </div>
        </div>
    </div>

    <div class="stats">
        <h2 style="margin-bottom:20px;">📊 API Stats</h2>
        <div class="stats-grid">
            <div class="stat"><div class="number">{total_images:,}</div><div class="label">Images Generated</div></div>
            <div class="stat"><div class="number">{'{:,}'.format(stats['total_requests'] if stats else 0)}</div><div class="label">Requests Today</div></div>
            <div class="stat"><div class="number">{'{:.0f}'.format(stats['avg_response_ms'] if stats else 0)}ms</div><div class="label">Avg Response</div></div>
        </div>
    </div>

    <footer>
        <p>Placeholder Image API — Open Source | <a href="/docs" style="color:#3a7bd5;">API Docs</a> | <a href="/dashboard" style="color:#3a7bd5;">Dashboard</a></p>
        <p style="margin-top:8px;">Built with ❤️ by an AI agent that runs 24/7</p>
    </footer>

    <script>
        const inputs = ['inp-w','inp-h','inp-bg','inp-fg','inp-text','inp-fmt'];
        inputs.forEach(id => document.getElementById(id).addEventListener('input', updatePreview));
        function updatePreview() {{
            const w = document.getElementById('inp-w').value;
            const h = document.getElementById('inp-h').value;
            const bg = document.getElementById('inp-bg').value;
            const fg = document.getElementById('inp-fg').value;
            const txt = document.getElementById('inp-text').value;
            const fmt = document.getElementById('inp-fmt').value;
            let url = `/${{w}}x${{h}}/${{bg}}/${{fg}}`;
            const params = new URLSearchParams();
            if (txt) params.set('text', txt);
            if (fmt !== 'png') params.set('format', fmt);
            if ([...params].length) url += '?' + params.toString();
            document.getElementById('preview').innerHTML = `<img src="${{url}}" alt="Preview">`;
            document.getElementById('url-out').textContent = 'https://placeholder.surge.sh' + url;
        }}
    </script>
</body>
</html>"""
    return HTMLResponse(html)

@app.get("/dashboard")
async def dashboard():
    """Owner monitoring dashboard"""
    db = get_db()
    
    # Stats
    today = datetime.now().strftime("%Y-%m-%d")
    total_requests = db.execute("SELECT COUNT(*) as c FROM request_log").fetchone()["c"]
    today_requests = db.execute("SELECT COUNT(*) as c FROM request_log WHERE date(timestamp)=?", (today,)).fetchone()["c"]
    unique_ips = db.execute("SELECT COUNT(DISTINCT ip) as c FROM request_log WHERE date(timestamp)=?", (today,)).fetchone()["c"]
    total_keys = db.execute("SELECT COUNT(*) as c FROM api_keys WHERE active=1").fetchone()["c"]
    premium_keys = db.execute("SELECT COUNT(*) as c FROM api_keys WHERE tier != 'free' AND active=1").fetchone()["c"]
    cache_count = len(list(CACHE_DIR.glob("*.*")))
    
    # Daily trends (last 14 days)
    daily = db.execute("""
        SELECT date(timestamp) as d, COUNT(*) as c, COUNT(DISTINCT ip) as ips,
               AVG(response_time_ms) as avg_ms
        FROM request_log 
        WHERE timestamp > date('now', '-14 days')
        GROUP BY date(timestamp) ORDER BY d
    """).fetchall()
    
    # Top sizes
    top_sizes = db.execute("""
        SELECT width, height, COUNT(*) as c FROM request_log 
        GROUP BY width, height ORDER BY c DESC LIMIT 10
    """).fetchall()
    
    # Recent requests
    recent = db.execute("""
        SELECT * FROM request_log ORDER BY id DESC LIMIT 20
    """).fetchall()
    
    # Revenue
    total_revenue = db.execute("SELECT COALESCE(SUM(amount),0) as s FROM revenue").fetchone()["s"]
    
    db.close()
    
    daily_labels = json.dumps([r["d"] for r in daily])
    daily_requests = json.dumps([r["c"] for r in daily])
    daily_ips = json.dumps([r["ips"] for r in daily])
    daily_avg = json.dumps([round(r["avg_ms"] or 0, 1) for r in daily])
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Placeholder API — Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0a0a0a; color: #e0e0e0; padding: 20px; }}
        h1 {{ text-align: center; margin-bottom: 30px; background: linear-gradient(90deg, #00d2ff, #3a7bd5); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 2em; }}
        .stats-row {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 16px; margin-bottom: 30px; }}
        .stat-card {{ background: #111; border-radius: 12px; padding: 20px; text-align: center; border: 1px solid #222; }}
        .stat-card .val {{ font-size: 2em; font-weight: bold; color: #00d2ff; }}
        .stat-card .lbl {{ font-size: 0.8em; color: #888; margin-top: 4px; text-transform: uppercase; letter-spacing: 1px; }}
        .chart-container {{ background: #111; border-radius: 12px; padding: 20px; margin-bottom: 30px; }}
        .chart-container h2 {{ margin-bottom: 16px; font-size: 1.1em; color: #888; }}
        table {{ width: 100%; background: #111; border-radius: 12px; overflow: hidden; border-collapse: collapse; }}
        th {{ background: #1a1a2e; padding: 12px; text-align: left; font-size: 0.85em; text-transform: uppercase; letter-spacing: 1px; color: #00d2ff; }}
        td {{ padding: 10px 12px; border-bottom: 1px solid #1a1a1a; font-size: 0.9em; }}
        tr:hover td {{ background: #1a1a1a; }}
        .section {{ margin-bottom: 30px; }}
        .section h2 {{ margin-bottom: 12px; font-size: 1.2em; }}
        .live-dot {{ display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: #00d2ff; animation: pulse 2s infinite; margin-right: 8px; }}
        @keyframes pulse {{ 0%,100% {{ opacity: 1; }} 50% {{ opacity: 0.3; }} }}
        .refresh-btn {{ position: fixed; bottom: 20px; right: 20px; background: #3a7bd5; color: #fff; border: none; border-radius: 50%; width: 50px; height: 50px; font-size: 1.5em; cursor: pointer; box-shadow: 0 4px 20px rgba(0,0,0,0.5); }}
    </style>
</head>
<body>
    <h1><span class="live-dot"></span>Placeholder API Dashboard</h1>
    
    <div class="stats-row">
        <div class="stat-card"><div class="val">{total_requests:,}</div><div class="lbl">Total Requests</div></div>
        <div class="stat-card"><div class="val">{today_requests:,}</div><div class="lbl">Today</div></div>
        <div class="stat-card"><div class="val">{unique_ips}</div><div class="lbl">Unique IPs Today</div></div>
        <div class="stat-card"><div class="val">{total_keys}</div><div class="lbl">API Keys</div></div>
        <div class="stat-card"><div class="val">{premium_keys}</div><div class="lbl">Premium Keys</div></div>
        <div class="stat-card"><div class="val">€{total_revenue:.2f}</div><div class="lbl">Revenue</div></div>
        <div class="stat-card"><div class="val">{cache_count}</div><div class="lbl">Cached Images</div></div>
    </div>

    <div class="section">
        <div class="chart-container">
            <h2>📈 Requests (14 days)</h2>
            <canvas id="chart-requests" height="100"></canvas>
        </div>
    </div>

    <div class="section">
        <div class="chart-container">
            <h2>⚡ Response Time (avg ms)</h2>
            <canvas id="chart-latency" height="80"></canvas>
        </div>
    </div>

    <div class="section">
        <h2>🏆 Top Image Sizes</h2>
        <table>
            <tr><th>Size</th><th>Requests</th></tr>
            {"".join(f'<tr><td>{r["width"]}×{r["height"]}</td><td>{r["c"]:,}</td></tr>' for r in top_sizes)}
        </table>
    </div>

    <div class="section">
        <h2>🕐 Recent Requests</h2>
        <table>
            <tr><th>Time</th><th>Size</th><th>Colors</th><th>IP</th><th>ms</th><th>Cached</th></tr>
            {"".join(f'<tr><td>{r["timestamp"][-8:]}</td><td>{r["width"]}×{r["height"]}</td><td>{r["bg_color"]}/{r["text_color"]}</td><td>{r["ip"][-10:] if r["ip"] else "-"}</td><td>{r["response_time_ms"]}</td><td>{"✓" if r["cached"] else ""}</td></tr>' for r in recent)}
        </table>
    </div>

    <button class="refresh-btn" onclick="location.reload()">↻</button>

    <script>
        const labels = {daily_labels};
        new Chart(document.getElementById('chart-requests'), {{
            type: 'line',
            data: {{
                labels,
                datasets: [
                    {{ label: 'Requests', data: {daily_requests}, borderColor: '#00d2ff', fill: true, backgroundColor: 'rgba(0,210,255,0.1)', tension: 0.3 }},
                    {{ label: 'Unique IPs', data: {daily_ips}, borderColor: '#ff6b6b', fill: false, tension: 0.3 }}
                ]
            }},
            options: {{ responsive: true, plugins: {{ legend: {{ labels: {{ color: '#888' }} }} }}, scales: {{ x: {{ ticks: {{ color: '#555' }} }}, y: {{ ticks: {{ color: '#555' }} }} }} }}
        }});
        new Chart(document.getElementById('chart-latency'), {{
            type: 'bar',
            data: {{
                labels,
                datasets: [{{ label: 'Avg ms', data: {daily_avg}, backgroundColor: 'rgba(58,123,213,0.6)' }}]
            }},
            options: {{ responsive: true, plugins: {{ legend: {{ labels: {{ color: '#888' }} }} }}, scales: {{ x: {{ ticks: {{ color: '#555' }} }}, y: {{ ticks: {{ color: '#555' }} }} }} }}
        }});
        // Auto-refresh every 60s
        setTimeout(() => location.reload(), 60000);
    </script>
</body>
</html>"""
    return HTMLResponse(html)

# ── Image Generation Endpoints ──

@app.get("/{width:int}x{height:int}/{bg_color:path}/{text_color:path}")
async def generate_image(
    request: Request,
    width: int,
    height: int,
    bg_color: str,
    text_color: str,
    text: str = Query(None),
    format: str = Query("png"),
    api_key: str = Query(None, alias="key")
):
    start = time.time()
    
    # Clean color params (remove extension if any)
    bg_color = bg_color.rsplit(".", 1)[0] if "." in bg_color else bg_color
    text_color = text_color.rsplit(".", 1)[0] if "." in text_color else text_color
    
    # Validate format
    if format.lower() not in ("png", "jpg", "jpeg", "webp"):
        format = "png"
    
    # Rate limit check
    allowed, tier, remaining = check_rate_limit(api_key)
    if not allowed:
        raise HTTPException(429, f"Rate limit exceeded ({tier} tier). Upgrade at https://placeholder.surge.sh")
    
    # Watermark only for free/anonymous
    add_watermark = tier in ("free", "anonymous")
    
    # Generate
    try:
        img_bytes = generate_placeholder(
            width=width, height=height,
            bg_color=bg_color, text_color=text_color,
            text=text, fmt=format.lower(),
            add_watermark=add_watermark
        )
    except Exception as e:
        logger.error(f"Image generation error: {e}")
        raise HTTPException(500, "Image generation failed")
    
    # Log request
    elapsed_ms = int((time.time() - start) * 1000)
    ip = request.client.host if request.client else "unknown"
    user_agent = request.headers.get("user-agent", "")[:200]
    
    try:
        db = get_db()
        db.execute(
            """INSERT INTO request_log (api_key, endpoint, width, height, bg_color, text_color, text, format, ip, user_agent, response_time_ms, cached)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (api_key, "generate", width, height, bg_color, text_color, text, format.lower(), ip, user_agent, elapsed_ms, 1 if elapsed_ms < 5 else 0)
        )
        db.commit()
        db.close()
    except Exception:
        pass
    
    if api_key:
        increment_usage(api_key)
    
    # Content type
    content_types = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg", "webp": "image/webp"}
    ct = content_types.get(format.lower(), "image/png")
    
    headers = {
        "X-Response-Time": f"{elapsed_ms}ms",
        "X-Tier": tier,
        "X-Rate-Limit-Remaining": str(remaining),
        "Cache-Control": "public, max-age=604800",
        "Access-Control-Allow-Origin": "*",
    }
    
    return Response(content=img_bytes, media_type=ct, headers=headers)

# Shorter URL format: /800x600
@app.get("/{width:int}x{height:int}")
async def generate_simple(request: Request, width: int, height: int, format: str = Query("png")):
    return await generate_image(request, width, height, "cccccc", "666666", format=format)

# SEO: Sizes index page
@app.get("/sizes/", response_class=HTMLResponse)
async def sizes_index(request: Request):
    """Browse all popular placeholder image sizes organized by category"""
    sizes_path = STATIC_DIR / "sizes" / "index.html"
    if sizes_path.is_file():
        return HTMLResponse(sizes_path.read_text(encoding="utf-8"))
    return HTMLResponse("<h1>Sizes directory not yet generated</h1><p>Run: python generate_seo_pages.py</p>", status_code=404)

# SEO: Sitemap
@app.get("/sitemap.xml")
async def sitemap():
    """XML sitemap for Google Search Console"""
    sitemap_path = STATIC_DIR / "sitemap.xml"
    if sitemap_path.is_file():
        return Response(content=sitemap_path.read_text(encoding="utf-8"), media_type="application/xml")
    return Response(content="<?xml version='1.0'?><urlset xmlns='http://www.sitemaps.org/schemas/sitemap/0.9'/>", media_type="application/xml")

# SEO pages for common sizes
@app.get("/size/{width:int}x{height:int}")
async def size_page(request: Request, width: int, height: int):
    """SEO landing page for each size combination"""
    colors = [
        ("3a7bd5", "ffffff", "Blue"), ("ff6600", "ffffff", "Orange"),
        ("2ECC71", "ffffff", "Green"), ("E74C3C", "ffffff", "Red"),
        ("9B59B6", "ffffff", "Purple"), ("1ABC9C", "ffffff", "Teal"),
        ("34495E", "ffffff", "Dark"), ("F39C12", "ffffff", "Amber"),
    ]
    preview_html = "".join(
        f'<div class="preview"><a href="/{width}x{height}/{bg}/{fg}"><img src="/{width}x{height}/{bg}/{fg}" alt="{width}x{height} {name} placeholder" loading="lazy"></a><small>{name}</small></div>'
        for bg, fg, name in colors
    )
    
    html = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{width}×{height} Placeholder Image — Free Download</title>
<meta name="description" content="Download free {width}×{height} placeholder images in any color. Perfect for web design mockups and prototypes.">
<meta property="og:image" content="/{width}x{height}/3a7bd5/ffffff">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}body{{font-family:-apple-system,sans-serif;background:#0a0a0a;color:#e0e0e0;padding:20px}}
h1{{text-align:center;margin:30px 0;font-size:1.8em}}.previews{{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:20px;max-width:900px;margin:0 auto 40px}}
.preview{{text-align:center;background:#111;border-radius:12px;padding:16px}}.preview img{{max-width:100%;border-radius:8px;margin-bottom:8px}}.preview small{{color:#888}}
.use{{max-width:600px;margin:0 auto;text-align:center;background:#111;border-radius:12px;padding:30px}}code{{background:#1a1a1a;padding:8px 12px;border-radius:6px;display:block;margin:10px 0;color:#00d2ff;font-size:0.9em}}
</style></head><body>
<h1>{width}×{height} Placeholder Images</h1>
<div class="previews">{preview_html}</div>
<div class="use"><h3>Quick Use</h3><code>&lt;img src="https://placeholder.surge.sh/{width}x{height}" alt="placeholder"&gt;</code>
<code>https://placeholder.surge.sh/{width}x{height}/3a7bd5/ffffff?text=Hello</code></div>
</body></html>"""
    return HTMLResponse(html)

# API key management
@app.post("/api/v1/keys")
async def create_key(email: str = Query(...), tier: str = Query("free")):
    import secrets
    key = f"phl_{secrets.token_hex(16)}"
    db = get_db()
    db.execute("INSERT INTO api_keys (key, email, tier) VALUES (?,?,?)", (key, email, tier))
    db.commit()
    db.close()
    return {"key": key, "tier": tier, "daily_limit": RATE_LIMITS.get(tier, 100)}

@app.get("/api/v1/usage/{api_key}")
async def get_usage(api_key: str):
    db = get_db()
    row = db.execute("SELECT * FROM api_keys WHERE key=?", (api_key,)).fetchone()
    if not row:
        db.close()
        raise HTTPException(404, "Key not found")
    result = dict(row)
    db.close()
    return result

@app.get("/api/v1/stats")
async def api_stats():
    db = get_db()
    today = datetime.now().strftime("%Y-%m-%d")
    total = db.execute("SELECT COUNT(*) as c FROM request_log").fetchone()["c"]
    today_count = db.execute("SELECT COUNT(*) as c FROM request_log WHERE date(timestamp)=?", (today,)).fetchone()["c"]
    db.close()
    return {"total_images": total, "today": today_count}

# Health check
@app.get("/health")
async def health():
    return {"status": "ok", "timestamp": datetime.now().isoformat()}

# ── Gumroad Webhook ──
TIER_MAP = {
    "placeholder-basic": "basic",
    "placeholder-pro": "pro",
}

@app.post("/webhooks/gumroad")
async def gumroad_webhook(request: Request):
    """Handle Gumroad sale webhooks — auto-create API keys for premium purchases"""
    import hmac as hmac_mod
    import secrets as secrets_mod
    
    body = await request.body()
    form_data = await request.form()
    payload = dict(form_data)
    
    logger.info(f"Gumroad webhook received: {payload.get('product_permalink', 'unknown')}")
    
    product_permalink = payload.get("product_permalink", "")
    email = payload.get("email", "")
    
    tier = TIER_MAP.get(product_permalink)
    if not tier:
        logger.warning(f"Unknown Gumroad product: {product_permalink}")
        return {"status": "ignored", "reason": "unknown product"}
    
    # Generate API key
    api_key = f"phl_{secrets_mod.token_hex(16)}"
    
    db = get_db()
    db.execute("INSERT INTO api_keys (key, email, tier) VALUES (?, ?, ?)", (api_key, email, tier))
    
    # Log revenue
    try:
        amount = float(payload.get("price", 0))
    except (ValueError, TypeError):
        amount = 0
    db.execute("INSERT INTO revenue (source, amount, description) VALUES (?, ?, ?)", 
               ("gumroad", amount, f"{tier} tier - {email}"))
    db.commit()
    db.close()
    
    limits = {"basic": 2000, "pro": 10000}
    logger.info(f"Created {tier} API key for {email}: {api_key[:12]}...")
    
    return {
        "status": "created",
        "api_key": api_key,
        "tier": tier,
        "daily_limit": limits.get(tier, 100),
        "instructions": f"Append ?key={api_key} to any API request URL"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8892)