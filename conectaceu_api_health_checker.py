#!/usr/bin/env python
"""Health check script - pings multiple API health endpoints"""
import os
import time
import requests
from dotenv import load_dotenv

# Load .env from the current directory
load_dotenv()

API_URLS = os.getenv("API_URLS", "").split(",")
API_URLS = [url.strip() for url in API_URLS if url.strip()]
DELAY_IN_SECONDS = int(os.getenv("DELAY_IN_SECONDS", "60"))

def check_health(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            print(f"✅ {url}: {response.json()}")
            return True
        else:
            print(f"❌ {url}: Status {response.status_code}")
            return False
    except requests.RequestException as e:
        print(f"❌ {url}: {e}")
        return False

if __name__ == "__main__":
    for url in API_URLS:
        url = url.strip()
        if not url:
            continue
        
        check_health(url)
        
        time.sleep(DELAY_IN_SECONDS)