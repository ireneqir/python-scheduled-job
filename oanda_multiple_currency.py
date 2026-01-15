import os
import requests
import pandas as pd
from datetime import date
import smtplib
from email.message import EmailMessage

# =========================
# CONFIG
# =========================
API_KEY = "YOUR_API_KEY"
CURRENCIES = ["JPY","THB","INR","SGD","VND","USD","IDR","PHP","TWD","EUR","GBP","MYR"]
EXCEL_FILE = "currency_rates.xlsx"
TO_EMAIL = "recipient@example.com"

# =========================
# STEP 1: GET RATES (USD BASE)
# =========================
url = "https://currencyapi.net/api/v1/rates"
params = {
    "key": API_KEY,
    "output": "JSON"
}

data = requests.get(url, params=params).json()

usd_to_sgd = data["rates"]["SGD"]

# =========================
# STEP 2: CONVERT TO SGD BASE
# =========================
today = date.today().strftime("%Y-%m-%d")
rows = []

for cur in CURRENCIES:
    if cur == "SGD":
        rate = 1
    else:
        rate = round(data["rates"][cur] / usd_to_sgd, 5)

    rows.append({
        "Date": today,
        "Currency": cur,
        "Unit Per SGD": rate
    })

df = pd.DataFrame(rows)
df.to_excel(EXCEL_FILE, index=False)

# =========================
# STEP 3: SEND EMAIL (GMAIL)
# =========================
EMAIL_ADDRESS = os.environ.get("EMAIL_USER")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASS")

msg = EmailMessage()
msg["Subject"] = f"Currency Rates (SGD Base) - {today}"
msg["From"] = EMAIL_ADDRESS
msg["To"] = TO_EMAIL
msg.set_content("Please find attached the latest currency rates based on SGD.")

with open(EXCEL_FILE, "rb") as f:
    msg.add_attachment(
        f.read(),
        maintype="application",
        subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename=EXCEL_FILE
    )

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    smtp.send_message(msg)

print("✅ Email sent with Excel attachment")
