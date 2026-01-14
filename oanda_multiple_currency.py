import requests
import pandas as pd
from datetime import date
import sys

BASE = "SGD"

CURRENCIES = [
    "INR", "SGD", "VND", "USD", "IDR",
    "PHP", "TWD", "EUR", "GBP", "MYR"
]

url = f"https://api.exchangerate.host/latest?base={BASE}"

try:
    r = requests.get(url, timeout=15)
    r.raise_for_status()
    data = r.json()
except Exception as e:
    print("❌ HTTP / Network error:", e)
    sys.exit(1)

# =========================
# VALIDATE RESPONSE
# =========================
if "rates" not in data:
    print("❌ API response missing 'rates'")
    print("Full response:")
    print(data)
    sys.exit(1)

rates = data["rates"]

rows = []
today = date.today().isoformat()

for ccy in CURRENCIES:
    rate = 1.0 if ccy == "SGD" else round(rates.get(ccy, 0), 6)
    rows.append({
        "Date": today,
        "Base": "SGD",
        "Currency": ccy,
        "Rate (1 SGD)": rate
    })

df = pd.DataFrame(rows)
df.to_excel("exchange_rate_per_sgd.xlsx", index=False)

print("✅ Exchange rates generated successfully")
print(df)
