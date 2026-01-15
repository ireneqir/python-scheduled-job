import requests
import pandas as pd
from datetime import date

# =========================
# CONFIG
# =========================
API_KEY = "fbae506908296f448259d594"
URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD"

CURRENCIES = [
    "JPY","THB","INR","SGD","VND",
    "USD","IDR","PHP","TWD",
    "EUR","GBP","MYR"
]

EXCEL_FILE = "exchange_rate_sgd.xlsx"

# =========================
# STEP 1: CALL API
# =========================
response = requests.get(URL, timeout=10)
data = response.json()

if data.get("result") != "success":
    raise Exception(f"ExchangeRate-API error: {data}")

rates = data["conversion_rates"]
usd_to_sgd = rates["SGD"]

# =========================
# STEP 2: CONVERT TO SGD BASE
# =========================
today = date.today().strftime("%Y-%m-%d")
rows = []

for cur in CURRENCIES:
    if cur == "SGD":
        rate = 1
    else:
        rate = round(rates[cur] / usd_to_sgd, 5)

    rows.append({
        "Date": today,
        "Currency": cur,
        "Unit Per SGD": rate
    })

df = pd.DataFrame(rows)

# =========================
# STEP 3: PRINT RESULT
# =========================
print("\n=== Currency Rates (Base SGD) ===")
print(df.to_string(index=False))

# =========================
# STEP 4: SAVE TO EXCEL
# =========================
df.to_excel(EXCEL_FILE, index=False)

print(f"\n✅ Excel created: {EXCEL_FILE}")
