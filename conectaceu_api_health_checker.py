#!/usr/bin/env python
"""Health check script - pings multiple API health endpoints"""
from datetime import datetime
import os
import time
import requests
from dotenv import load_dotenv

# Load .env from the current directory
load_dotenv()

API_URLS = os.getenv("API_URLS", "").split(",")
API_URLS = [url.strip() for url in API_URLS if url.strip()]
DELAY_IN_SECONDS = int(os.getenv("DELAY_IN_SECONDS", "60"))

def now():
    return datetime.now()

def check_health(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            print(f"{now()} | ✅ {url}: {response.json()}")
            return True
        else:
            print(f"{now()} | ❌ {url}: Status {response.status_code}")
            return False
    except requests.RequestException as e:
        print(f"{now()} | ❌ {url}: {e}")
        return False

if __name__ == "__main__":
    print(f'{now()} | Starting validations')
    for url in API_URLS:
        url = url.strip()
        if not url:
            continue
        
        check_health(url)
        
        print(f'{now()} | Waiting for {DELAY_IN_SECONDS} seconds')
        time.sleep(DELAY_IN_SECONDS)