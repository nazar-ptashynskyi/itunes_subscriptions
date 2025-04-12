import requests
import json
import os
from datetime import datetime

CACHE_FILE = 'cache/.currency_cache.json'
os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)

if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, 'r') as f:
        currency_cache = json.load(f)
else:
    currency_cache = {}

unsupported_currency_set = set()

SUPPORTED_CURRENCIES = [
    'USD', 'EUR', 'GBP', 'CHF', 'SEK', 'NOK', 'DKK', 'JPY', 'AUD', 'CAD', 'CZK', 'PLN', 'HUF'
]

def get_usd_rate(date_str, currency):
    if currency == 'USD':
        return 1.0, True

    if currency not in SUPPORTED_CURRENCIES:
        unsupported_currency_set.add(currency)
        return 1.0, False

    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        fixed_date = dt.strftime("%Y-%m-%d")
    except:
        print(f"[WARN] Wrong date format: {date_str}")
        return 1.0, False

    cache_key = f"{fixed_date}_{currency}"

    if cache_key in currency_cache:
        return currency_cache[cache_key], True

    url = f"https://api.frankfurter.app/{fixed_date}?from={currency}&to=USD"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        rate = data['rates']['USD']

        currency_cache[cache_key] = rate
        with open(CACHE_FILE, 'w') as f:
            json.dump(currency_cache, f)

        return rate, True
    except Exception as e:
        print(f"[WARN] Failed to fetch rate for {currency} on {fixed_date}. Error: {e}")
        return 1.0, False

def print_unsupported_currency_summary():
    if unsupported_currency_set:
        print("\n⚠️ Unsupported currencies encountered:")
        print("   ", ", ".join(sorted(unsupported_currency_set)))
    else:
        print("\n✅ No unsupported currencies encountered.")
