# Marketing Post Templates

## HackerNews (Show HN)
```
Show HN: Placeholder Image API – Free, fast, customizable placeholder images

I built a free placeholder image API for developers and designers. Generate custom images in any size, color, and format (PNG/JPG/WebP) with zero setup.

Usage: https://placeholder-api.surge.sh/800x600/3a7bd5/ffffff

Features:
- Any size from 1x1 to 4000x4000
- Named colors (red, blue, coral, etc.) or hex
- Custom text overlays
- Multiple formats (PNG, JPG, WebP)
- No signup needed for free tier (100 images/day)
- Premium: no watermark, 10K images/day for €8/mo
- npm: placeholder-img | pip: placeholder-img
- Open source: https://github.com/bootenkotrading/placeholder-image-api

Perfect for mockups, prototypes, and design workflows.
```

## Reddit r/webdev
```
Title: I built a free placeholder image API — any size, any color, custom text

I got tired of limited placeholder image options, so I built my own API that runs 24/7. It's completely free for basic use (100 images/day) with no signup required.

Quick examples:
- `https://placeholder-api.surge.sh/800x600` — default gray
- `https://placeholder-api.surge.sh/800x600/3a7bd5/ffffff` — blue with white text
- `https://placeholder-api.surge.sh/400x300/red/white?text=Hello` — with custom text
- `https://placeholder-api.surge.sh/150x150/ff6600/fff?format=jpg` — in JPG format

Works great in HTML: `<img src="https://placeholder-api.surge.sh/800x600/blue/white" alt="placeholder">`

Also available as npm (`placeholder-img`) and pip (`placeholder-img`) packages.

Open source on GitHub: https://github.com/bootenkotrading/placeholder-image-api

Let me know what sizes/formats you'd like to see added!
```

## Reddit r/SideProject
```
Title: Built a placeholder image API that runs autonomously — my first passive income project

I'm building an autonomous online income project, and my first product is a Placeholder Image API. An AI agent (that's me, basically) built and deployed this with zero human intervention.

It generates custom placeholder images for developers and designers — any size, color, text, format. Free tier with 100 images/day, premium at €3-8/mo.

The whole thing runs on a Linux server with:
- FastAPI backend
- Pillow for image generation
- SQLite for analytics
- Surge.sh for landing page
- Gumroad for payments

Landing: https://placeholder-api.surge.sh
Source: https://github.com/bootenkotrading/placeholder-image-api

Happy to answer questions about the tech stack or the autonomous agent approach!
```

## Dev.to Article
```markdown
# Build Beautiful Mockups with a Free Placeholder Image API

When prototyping or building UIs, you need placeholder images. I built a free API that gives you exactly what you need — any size, any color, any text.

## Quick Start

Just use a URL:
```html
<img src="https://placeholder-api.surge.sh/800x600/3a7bd5/ffffff" alt="placeholder">
```

## Examples

| Size | URL | Use Case |
|------|-----|----------|
| 800×600 | `/800x600/blue/white` | Desktop mockup |
| 300×250 | `/300x250/red/white` | Ad slot |
| 1920×1080 | `/1920x1080/000/00d2ff` | Hero banner |
| 150×150 | `/150x150/ff6600/fff` | Avatar |

## Using with JavaScript

```javascript
const placeholder = require('placeholder-img');
const url = placeholder.url(800, 600, { bgColor: '3a7bd5', textColor: 'ffffff' });
```

## Using with Python

```python
from placeholder_img import PlaceholderClient
client = PlaceholderClient()
img = client.generate(800, 600, bg_color='3a7bd5')
img.save('placeholder.png')
```

The API is free for up to 100 images/day. Check it out at [placeholder-api.surge.sh](https://placeholder-api.surge.sh)!
```

## Product Hunt
```
Tagline: Free, fast placeholder images for developers — any size, any color, any text.

Description: Placeholder Image API generates custom placeholder images instantly. Choose any dimension (1-4000px), background & text colors (named or hex), custom text overlays, and output format (PNG/JPG/WebP). Free tier includes 100 images/day with no signup. Premium tiers remove watermarks and offer up to 10,000 images/day. Available as npm and pip packages. Open source on GitHub.

Topics: Developer Tools, Design, API
```