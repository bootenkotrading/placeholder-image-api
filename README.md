# Placeholder Image API

A blazing-fast, self-hosted placeholder image API built with **FastAPI** and **Pillow**. Generate custom placeholder images on-the-fly for your designs, prototypes, and mockups — any size, any color, any format.

## ✨ Features

- **Instant image generation** — any size from 1×1 to 4000×4000 pixels
- **Custom colors** — hex codes (`3a7bd5`) or named colors (`red`, `blue`, `coral`, etc.)
- **Multiple formats** — PNG, JPG, WebP
- **Custom text overlays** — show custom text or auto-dimensions
- **7-day image caching** — MD5-hashed cache files for speed
- **API key system** — tiered rate limiting with usage tracking
- **Watermark system** — free tier includes subtle watermark; premium removes it
- **Interactive landing page** — live preview with customizer
- **Monitoring dashboard** — real-time stats with Chart.js graphs
- **SEO-optimized** — per-size landing pages, sitemap, Open Graph tags
- **Health check endpoint** — for uptime monitoring
- **SQLite backend** — lightweight, no external DB needed

## 🚀 Quick Start

### Simple URL patterns

```
https://placeholder.surge.sh/600x400
https://placeholder.surge.sh/600x400/3a7bd5/ffffff
https://placeholder.surge.sh/300x200/red/white
https://placeholder.surge.sh/800x600/000000/00d2ff?text=Banner
https://placeholder.surge.sh/150x150/ff6600/fff?text=Avatar&format=jpg
```

### In HTML

```html
<img src="https://placeholder.surge.sh/300x200" alt="Placeholder">
<img src="https://placeholder.surge.sh/800x600/1a1a2e/00d2ff?text=Hero+Banner" alt="Hero">
```

### In CSS

```css
.hero {
  background: url('https://placeholder.surge.sh/1200x400/0f3460/00d2ff?text=Header') no-repeat center;
}
```

## 📡 API Endpoints

| Endpoint | Description |
|---|---|
| `GET /` | Interactive landing page with live preview |
| `GET /{W}x{H}` | Generate image with default gray colors |
| `GET /{W}x{H}/{bg}/{fg}` | Generate image with custom background and text color |
| `GET /size/{W}x{H}` | SEO landing page for a specific size |
| `GET /dashboard` | Monitoring dashboard with stats and charts |
| `GET /health` | Health check endpoint |
| `GET /docs` | Interactive API documentation (Swagger) |
| `GET /redoc` | Alternative API documentation |
| `POST /api/v1/keys` | Create a new API key |
| `GET /api/v1/usage/{key}` | Get usage stats for an API key |
| `GET /api/v1/stats` | Global API statistics (JSON) |

### Query Parameters

- `text` — Custom text overlay (default: `{W}×{H}`)
- `format` — Image format: `png`, `jpg`, `webp` (default: `png`)

## 💰 Pricing Tiers

- **Free** — $0/mo · 100 images/day · all sizes & formats · named colors · small watermark
- **Basic** — €3/mo · 2,000 images/day · no watermark · custom text · priority caching
- **Pro** — €8/mo · 10,000 images/day · no watermark · custom fonts · API key auth · usage dashboard
- **Enterprise** — Custom · unlimited requests · SLA · dedicated support

## 🛠️ Deployment

### Local Development

```bash
# Clone the repo
git clone https://github.com/bootenkotrading/placeholder-image-api.git
cd placeholder-image-api

# Install dependencies
pip install fastapi uvicorn pillow

# Run the server
uvicorn app:app --host 0.0.0.0 --port 8892
```

### Production (systemd)

```bash
# Copy the systemd service file
sudo cp placeholder-api.service /etc/systemd/system/
sudo systemctl enable placeholder-api
sudo systemctl start placeholder-api
```

### Nginx Reverse Proxy

```bash
# Copy the nginx config
sudo cp nginx-placeholder.conf /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
```

### Docker (optional)

```bash
docker build -t placeholder-api .
docker run -d -p 8892:8892 --name placeholder-api placeholder-api
```

## 📁 Project Structure

```
placeholder-api/
├── app.py                  # Main FastAPI application
├── cache_cleanup.py        # Cache cleanup cron script
├── check_deps.py            # Dependency checker
├── generate_seo_pages.py    # SEO page generator
├── install_deps.py          # Dependency installer
├── nginx-placeholder.conf   # Nginx reverse proxy config
├── placeholder-api.service  # systemd service unit
├── static/                  # Generated static/SEO pages
└── templates/               # Jinja2 templates
```

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.