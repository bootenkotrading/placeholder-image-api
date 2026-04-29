#!/usr/bin/env python3
"""Cash cache and manage old cached images"""
import os
import time
from pathlib import Path

CACHE_DIR = Path(__file__).parent / "cache"
MAX_AGE_DAYS = 7

def cleanup():
    now = time.time()
    removed = 0
    freed = 0
    for f in CACHE_DIR.glob("*.*"):
        age_days = (now - f.stat().st_mtime) / 86400
        if age_days > MAX_AGE_DAYS:
            size = f.stat().st_size
            f.unlink()
            removed += 1
            freed += size
    print(f"Cleaned {removed} files, freed {freed/1024/1024:.1f}MB")
    return removed, freed

if __name__ == "__main__":
    cleanup()