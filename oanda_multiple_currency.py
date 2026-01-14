import requests
import pandas as pd
from datetime import date

# =========================
# CONFIG
# =========================
BASE_CURRENCY = "SGD"

CURRENCIES = [
    "INR",
    "SGD",
    "VND",
    "USD",
    "IDR",
    "PHP",
    "TWD",
    "EUR",
    "GBP",
    "MYR"
]

OUTPUT_FILE = "exchange_rate_per_sgd.xlsx"

# =========================
# FETCH RATES
# =========================
url = f"https://api.exchangerate.host/latest?base={BASE_CURRENCY}"
response = requests.get(url, timeout=10)
data = response.json()

rates = data["rates"]
today = date.today().isoformat()

rows = []

for ccy in CURRENCIES:
    if ccy == "SGD":
        rate = 1.0
    else:
        rate = round(rates.get(ccy, 0), 6)

    rows.append({
        "Date": today,
        "Base": "SGD",
        "Currency": ccy,
        "Rate (1 SGD)": rate
    })

# =========================
# SAVE TO EXCEL
# =========================
df = pd.DataFrame(rows)
df.to_excel(OUTPUT_FILE, index=False)

print("Exchange rates saved to", OUTPUT_FILE)
print(df)
