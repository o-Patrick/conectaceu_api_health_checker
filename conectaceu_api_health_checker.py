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

def tryDeserialize(response):
    canDeserialize = False
    deserializedObject = None
    try:
        if response.content:
            canDeserialize = True
            deserializedObject = response.json()
    except Exception as e:
        pass
    return (canDeserialize, deserializedObject)

def check_health(url):
    try:
        response = requests.get(url, timeout=10)
        statusCode = response.status_code
        statusCodeMessage = f'Response status code: {statusCode}'
        deserialization = tryDeserialize(response)
        if statusCode == 200:
            print(f"{now()} | ✅ {statusCodeMessage}. Content: {deserialization[1]}")
            return True
        else:
            print(f"{now()} | ❌ {statusCodeMessage}. Content: {deserialization[1] if deserialization[0] else '[no content]'}")
            return False
    except requests.RequestException as e:
        print(f"{now()} | ❌ {e}")
        return False

if __name__ == "__main__":
    print(f'{now()} | Starting validations')
    while True:
        for url in API_URLS:
            url = url.strip()
            print(f'{now()} | Querying: {url}')
            if not url:
                continue
            
            check_health(url)
            
            print(f'{now()} | Waiting for {DELAY_IN_SECONDS} seconds')
            time.sleep(DELAY_IN_SECONDS)