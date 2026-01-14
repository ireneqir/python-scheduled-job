import os
import sys
import requests
import pandas as pd
from datetime import date

# =========================
# CONFIG
# =========================
API_KEY = os.getenv("EXCHANGE_API_KEY")  # Get API key from environment

if not API_KEY:
    raise ValueError("❌ EXCHANGE_API_KEY not set in environment variables.")

BASE_CURRENCY = "SGD"

CURRENCIES = [
    "INR", "SGD", "VND", "USD", "IDR",
    "PHP", "TWD", "EUR", "GBP", "MYR"
]

OUTPUT_FILE = "exchange_rate_per_sgd.xlsx"

# =========================
# API REQUEST
# =========================
url = "https://api.exchangerate.host/latest"
params = {
    "base": BASE_CURRENCY,
    "access_key": API_KEY
}

try:
    response = requests.get(url, params=params, timeout=15)
    response.raise_for_status()
    data = response.json()
except requests.exceptions.RequestException as e:
    print("❌ HTTP / Network error:", e)
    sys.exit(1)

# =========================
# VALIDATE RESPONSE
# =========================
if "rates" not in data:
    print("❌ API error or missing 'rates' in response")
    print("Full API response:")
    print(data)
    sys.exit(1)

rates = data["rates"]
today = date.today().isoformat()

# =========================
# BUILD DATAFRAME
# =========================
rows = []

for ccy in CURRENCIES:
    rate = 1.0 if ccy == BASE_CURRENCY else round(rates.get(ccy, 0), 6)
    rows.append({
        "Date": today,
        "Base": BASE_CURRENCY,
        "Currency": ccy,
        "Rate (1 SGD)": rate
    })

df = pd.DataFrame(rows)

# =========================
# SAVE TO EXCEL
# =========================
try:
    df.to_excel(OUTPUT_FILE, index=False)
    print(f"✅ Exchange rates saved to {OUTPUT_FILE}")
except Exception as e:
    print("❌ Failed to save Excel file:", e)
    sys.exit(1)

# =========================
# PRINT TO CONSOLE
# =========================
print(df)
