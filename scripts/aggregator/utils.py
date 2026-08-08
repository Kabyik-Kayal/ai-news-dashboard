"""
Utility functions, constants, and network headers for AI News Aggregator.
"""

import os
from datetime import timezone, timedelta
from urllib.parse import urlparse

# Try zoneinfo for IST, fallback to fixed offset (+05:30)
try:
    from zoneinfo import ZoneInfo
    IST = ZoneInfo("Asia/Kolkata")
except Exception:
    IST = timezone(timedelta(hours=5, minutes=30))

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AI-News-Dashboard/1.0"
}

def get_github_headers():
    headers = {"User-Agent": "AI-News-Dashboard-Bot/1.0"}
    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers

def extract_domain(url):
    if not url:
        return ""
    try:
        netloc = urlparse(url).netloc.lower()
        if netloc.startswith("www."):
            netloc = netloc[4:]
        return netloc
    except Exception:
        return ""
