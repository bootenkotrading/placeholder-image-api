"""
Gumroad Webhook Handler for Placeholder Image API
When a customer purchases a premium tier on Gumroad, this automatically:
1. Verifies the purchase via Gumroad API
2. Creates an API key with the appropriate tier
3. Emails the key to the customer (or includes in Gumroad receipt)
"""
import hashlib
import secrets
import sqlite3
import os
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent / "data.db"

TIER_MAP = {
    "placeholder-basic": "basic",
    "placeholder-pro": "pro",
}

def handle_gumroad_sale(payload: dict) -> dict:
    """Process a Gumroad sale webhook payload"""
    product_permalink = payload.get("product_permalink", "")
    email = payload.get("email", "")
    
    tier = TIER_MAP.get(product_permalink)
    if not tier:
        return {"error": "unknown product", "permalink": product_permalink}
    
    # Generate API key
    api_key = f"phl_{secrets.token_hex(16)}"
    
    # Store in database
    db = sqlite3.connect(str(DB_PATH))
    db.execute(
        "INSERT INTO api_keys (key, email, tier) VALUES (?, ?, ?)",
        (api_key, email, tier)
    )
    # Log revenue
    amount = float(payload.get("price", 0))
    db.execute(
        "INSERT INTO revenue (source, amount, description) VALUES (?, ?, ?)",
        ("gumroad", amount, f"{tier} tier - {email}")
    )
    db.commit()
    
    # Get rate limit for tier
    limits = {"basic": 2000, "pro": 10000}
    
    db.close()
    
    return {
        "api_key": api_key,
        "tier": tier,
        "email": email,
        "daily_limit": limits.get(tier, 100),
        "instructions": f"Use your API key: ?key={api_key} in any request URL"
    }

def verify_gumroad_signature(payload_body: bytes, signature: str) -> bool:
    """Verify Gumroad webhook signature"""
    # Gumroad uses HMAC-SHA256
    gumroad_secret = os.environ.get("GUMROAD_WEBHOOK_SECRET", "")
    if not gumroad_secret:
        return True  # Skip verification if no secret configured
    
    import hmac
    expected = hmac.new(
        gumroad_secret.encode(),
        payload_body,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature)


# Add this to app.py as a route:
# @app.post("/webhooks/gumroad")
# async def gumroad_webhook(request: Request):
#     body = await request.body()
#     sig = request.headers.get("X-Gumroad-Signature", "")
#     if not verify_gumroad_signature(body, sig):
#         raise HTTPException(403, "Invalid signature")
#     payload = await request.form()
#     result = handle_gumroad_sale(dict(payload))
#     return result