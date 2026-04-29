# Placeholder Image API - Project Memory Database
# Last updated: 2026-04-29

## Project Location
- Base dir: /home/hermes/workspace/placeholder-api/
- App file: /home/hermes/workspace/placeholder-api/app.py
- Cache dir: /home/hermes/workspace/placeholder-api/cache/
- Logs dir: /home/hermes/workspace/placeholder-api/logs/
- DB: /home/hermes/workspace/placeholder-api/data.db
- Server: running on port 8892 (background process proc_52c868ef563a)
- Server public IP: 149.202.58.157
- IPv6: 2001:41d0:305:2100::1:2ef0

## Tech Stack
- Python 3.11.15 (venv at /home/hermes/.hermes/hermes-agent/venv/)
- FastAPI 0.136.0
- Pillow 12.2.0
- uvicorn 0.44.0
- SQLite3

## Features Built
- Image generation: any size (1-4000px), any color (hex + named), PNG/JPG/WebP
- Custom text overlays
- Watermark for free tier ("placeholder.surge.sh"), no watermark for premium
- API key system with rate limiting (free:100/day, basic:2000/day €3/mo, pro:10000/day €8/mo)
- SQLite database: api_keys, request_log, daily_stats, revenue tables
- Image caching (7 days, MD5 hash filenames)
- Cache cleanup script: /home/hermes/workspace/placeholder-api/cache_cleanup.py
- SEO landing pages per size (/size/WxH)
- Live monitoring dashboard (/dashboard) with Chart.js graphs
- API docs (/docs)
- Health check (/health)

## Gumroad Account
- User: bootenko
- Existing products: free-ai-prompts, ssuder (personal finance dashboard)
- Need to create: placeholder-basic (€3/mo), placeholder-pro (€8/mo)

## Endpoints
- GET / — Landing page
- GET /dashboard — Monitor dashboard  
- GET /health — Health check
- GET /{W}x{H}/{bg}/{fg} — Generate image
- GET /{W}x{H} — Simple generation (gray default)
- GET /size/{W}x{H} — SEO page
- POST /api/v1/keys — Create API key
- GET /api/v1/usage/{key} — Key usage stats
- GET /api/v1/stats — API stats JSON

## Completed
- [x] API built and running on port 8892
- [x] Monitoring dashboard at /dashboard  
- [x] SEO pages: 72 sizes + sitemap.xml
- [x] Surge.sh landing page: https://placeholder-api.surge.sh
- [x] GitHub repo: https://github.com/bootenkotrading/placeholder-image-api
- [x] npm package built: /home/hermes/workspace/placeholder-api/npm-package/ (needs npm login to publish)
- [x] pip package built: /home/hermes/workspace/placeholder-api/pip-package/ (needs PyPI token to publish)
- [x] Gumroad "Placeholder Basic" created (one-time, needs manual conversion to membership)
- [x] Gumroad webhook handler at /webhooks/gumroad (auto-creates API keys)
- [x] Marketing templates for HN, Reddit, Dev.to, Product Hunt (MARKETING_TEMPLATES.md)
- [x] API directory submission templates (API_DIRECTORY_TEMPLATES.md)
- [x] Cron: Cache cleanup daily at 3am (job_id: bdbae5a21d62)
- [x] Cron: Health check every 30min with auto-restart (job_id: 3d19b56a9027)
- [x] Cron: Weekly stats report every Monday 9am (job_id: bab104ac4aa7)
- [x] All code pushed to GitHub

## TODO - Requires Your Manual Action
- [ ] Nginx: `sudo cp /home/hermes/workspace/placeholder-api/nginx-placeholder.conf /etc/nginx/sites-enabled/ && sudo nginx -t && sudo systemctl reload nginx`
- [ ] Gumroad: Log in at app.gumroad.com → convert Placeholder Basic to Membership → create Placeholder Pro membership
- [ ] npm publish: Login with `npm login` then `cd npm-package && npm publish`
- [ ] pip publish: Get PyPI token, set TWINE_USERNAME/TWINE_PASSWORD, then `cd pip-package && twine upload dist/*`
- [ ] Set Gumroad webhook URL: https://placeholder-api.surge.sh/webhooks/gumroad (or http://149.202.58.157:8892/webhooks/gumroad)

## Server Environment
- Port 8891 occupied by unknown process (connection reset)
- Port 8892 = our API (working)
- No sudo access for hermes user
- nginx configs at /etc/nginx/sites-enabled/ (owned by root)
- Surge.sh available for static hosting

## Marketing Plan (from earlier conversation)
1. Product Hunt launch
2. GitHub open-source
3. Dev community posts (HN, Reddit, Dev.to, Lobsters, IndieHackers)
4. Programmatically SEO pages per size/color combo
5. API directories (RapidAPI, ProgrammableWeb, APIs.io, PublicAPIs.dev, AnyAPI)
6. "Alternatives" pages for competitor SEO
7. Free tier = organic growth (embeds in tutorials, Stack Overflow)
8. Cross-link from existing niche sites
9. npm/pip SDK packages
10. Uptime + speed = retention

## Revenue Expectations
- Month 1: 50-200 free users, 2-5 paid (~€6-15)
- Month 3: 500+ users, 10-20 paid (~€30-80/mo)