"""
Quick sanity check for .env — confirms Telegram and healthchecks.io are wired up
correctly before building the real script. Safe to run as many times as you want;
it doesn't touch any of the project's data files.

Usage:
    python test_env.py
"""

import os
import sys
import requests
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
HEALTHCHECKS_PING_URL = os.getenv("HEALTHCHECKS_PING_URL")

print("=== Checking .env values are loaded ===")
missing = []
for name, val in [
    ("TELEGRAM_BOT_TOKEN", TELEGRAM_BOT_TOKEN),
    ("TELEGRAM_CHAT_ID", TELEGRAM_CHAT_ID),
    ("HEALTHCHECKS_PING_URL", HEALTHCHECKS_PING_URL),
]:
    if val:
        # Don't print the full secret, just confirm it's non-empty
        preview = val if name == "TELEGRAM_CHAT_ID" else f"{val[:6]}...{val[-4:]}"
        print(f"  OK  {name} = {preview}")
    else:
        print(f"  MISSING  {name}")
        missing.append(name)

if missing:
    print(f"\nStopping — fill in {', '.join(missing)} in .env before continuing.")
    sys.exit(1)

print("\n=== Testing Telegram ===")
try:
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    resp = requests.post(
        url,
        json={"chat_id": TELEGRAM_CHAT_ID, "text": "✅ test_env.py: Telegram is working!"},
        timeout=10,
    )
    resp.raise_for_status()
    data = resp.json()
    if data.get("ok"):
        print("  Telegram message sent — check your phone.")
    else:
        print(f"  Telegram API returned an error: {data}")
except Exception as e:
    print(f"  Telegram request failed: {e}")

print("\n=== Testing healthchecks.io ===")
try:
    resp = requests.get(HEALTHCHECKS_PING_URL, timeout=10)
    resp.raise_for_status()
    print(f"  Ping sent — status code {resp.status_code}. Check your healthchecks.io dashboard, the check should now show 'Up' with a recent ping time.")
except Exception as e:
    print(f"  Healthchecks ping failed: {e}")

print("\nDone.")
