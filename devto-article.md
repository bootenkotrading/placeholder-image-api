---
title: "Build Beautiful Mockups with a Free Placeholder Image API"
published: false
description: "Generate custom placeholder images instantly — any size, color, text, format. Free for developers."
tags: webdev, api, productivity, beginners
cover_image: http://149.202.58.157:8892/1200x600/1a1a2e/00d2ff?text=Placeholder+Image+API
---

When prototyping or building UIs, you need placeholder images. I built a **free** API that gives you exactly what you need — any size, any color, any text.

## Quick Start

Just use a URL pattern:

```html
<img src="https://placeholder-api.surge.sh/800x600/3a7bd5/ffffff" alt="placeholder">
```

That's it. No signup, no API key for basic use. Just URLs.

## Examples

**Default gray:**
```
https://placeholder-api.surge.sh/800x600
```

**Custom colors (named or hex):**
```
https://placeholder-api.surge.sh/800x600/red/white
https://placeholder-api.surge.sh/400x300/ff6600/ffffff
```

**Custom text:**
```
https://placeholder-api.surge.sh/400x300/3a7bd5/ffffff?text=Hero+Image
```

**Different formats (PNG, JPG, WebP):**
```
https://placeholder-api.surge.sh/800x600/000000/00d2ff?format=jpg
https://placeholder-api.surge.sh/800x600/000000/00d2ff?format=webp
```

**Small sizes for avatars and thumbnails:**
```
https://placeholder-api.surge.sh/150x150/9B59B6/ffffff?text=JD
https://placeholder-api.surge.sh/50x50/E74C3C/ffffff
```

## Common Use Cases

| Use Case | URL Pattern |
|----------|------------|
| Hero banner | `/1200x400/1a1a2e/00d2ff?text=Hero` |
| Blog thumbnail | `/800x450/2ECC71/ffffff` |
| Avatar | `/150x150/9B59B6/ffffff?text=JD` |
| Ad slot (300x250) | `/300x250/E74C3C/ffffff?text=Ad` |
| Profile card | `/400x300/ff6600/ffffff?text=Profile` |
| Favicon | `/32x32/3a7bd5/ffffff` |

## Using with JavaScript / npm

```bash
npm install placeholder-img
```

```javascript
const placeholder = require('placeholder-img');

// Get URL
const url = placeholder.url(800, 600, { bgColor: '3a7bd5', textColor: 'ffffff' });
// → https://placeholder-api.surge.sh/800x600/3a7bd5/ffffff

// Download as buffer
const buffer = await placeholder.download(800, 600, { text: 'Hello' });
```

## Using with Python / pip

```bash
pip install placeholder-img
```

```python
from placeholder_img import PlaceholderClient

client = PlaceholderClient()

# Get URL
url = client.url(800, 600, bg_color='3a7bd5', text_color='ffffff')

# Generate PIL Image directly
img = client.generate(800, 600, text='Hero Section')
img.save('placeholder.png')

# Download to file
client.download(800, 600, 'output.jpg', bg_color='000000', text_color='00d2ff')
```

## Using with CSS

```css
.empty-state {
  background-image: url('https://placeholder-api.surge.sh/800x400/1a1a2e/00d2ff?text=Coming+Soon');
  background-size: cover;
}

.avatar-placeholder {
  background-image: url('https://placeholder-api.surge.sh/150x150/9B59B6/ffffff?text=JD');
  border-radius: 50%;
}
```

## Using with React / Next.js

```jsx
function Card({ title }) {
  return (
    <div>
      <img 
        src={`https://placeholder-api.surge.sh/400x300/3a7bd5/ffffff?text=${encodeURIComponent(title)}`}
        alt={title}
      />
      <h3>{title}</h3>
    </div>
  );
}
```

## Why I Built This

Existing placeholder image services have limitations — limited sizes, no custom text, no format options, or they're just slow. I wanted something that:

- ✅ Supports **any size** from 1×1 to 4000×4000
- ✅ Accepts **named colors** (red, blue, coral) or hex codes
- ✅ Allows **custom text overlays**
- ✅ Outputs in **PNG, JPG, or WebP**
- ✅ Has **no signup** for basic use
- ✅ Is **open source** on [GitHub](https://github.com/bootenkotrading/placeholder-image-api)

## Pricing

| Tier | Images/Day | Watermark | Price |
|------|-----------|-----------|-------|
| Free | 100 | Small | $0/mo |
| Basic | 2,000 | None | €3/mo |
| Pro | 10,000 | None | €8/mo |

The free tier is perfect for most prototyping and mockup needs. Premium removes the small watermark and bumps your daily limit.

## API Documentation

Full interactive docs are available at:
- Swagger UI: [http://149.202.58.157:8892/docs](http://149.202.58.157:8892/docs)
- ReDoc: [http://149.202.58.157:8892/redoc](http://149.202.58.157:8892/redoc)

## Available Sizes

Check out the [sizes directory](https://placeholder-api.surge.sh/sizes/) for pre-built pages with the most common web design dimensions — social media, ad sizes, avatars, device screens, and more.

---

**Try it now:** [https://placeholder-api.surge.sh](https://placeholder-api.surge.sh)

**Source code:** [https://github.com/bootenkotrading/placeholder-image-api](https://github.com/bootenkotrading/placeholder-image-api)

Feedback and feature requests welcome! What sizes or features would you like to see?