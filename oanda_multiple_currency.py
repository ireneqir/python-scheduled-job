import requests
import pandas as pd
from datetime import date
import smtplib
import mimetypes
from email.message import EmailMessage

# =========================
# STEP 1: API (UNCHANGED)
# =========================
url = "https://currencyapi.net/api/v1/rates"
params = {
    "key": "YOUR_API_KEY",
    "output": "JSON"
}

response = requests.get(url, params=params)
data = response.json()

usd_to_sgd = data["rates"]["SGD"]

CURRENCIES = ["JPY","THB","INR","SGD","VND","USD","IDR","PHP","TWD","EUR","GBP","MYR"]

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
excel_file = "oanda_exchange_rate_sgd.xlsx"
df.to_excel(excel_file, index=False)

# =========================
# STEP 2: EMAIL (SMTP ONLY)
# =========================
msg = EmailMessage()
msg['Subject'] = 'Daily Currency Trigger'
msg['From'] = 'irene.ng@takenaka.com.sg'
msg['To'] = 'irene.ng@takenaka.com.sg'
msg.set_content('Please see attached file')

def attach_file_to_email(email, filename):
    """Attach a file identified by filename, to an email message"""
    with open(filename, 'rb') as fp:
        file_data = fp.read()
        maintype, _, subtype = (
            mimetypes.guess_type(filename)[0] or 'application/octet-stream'
        ).partition("/")
        email.add_attachment(
            file_data,
            maintype=maintype,
            subtype=subtype,
            filename=filename
        )

attach_file_to_email(msg, excel_file)

def send_mail_smtp(mail, host):
    s = smtplib.SMTP(host, port=25)
    s.starttls()
    s.send_message(mail)
    s.quit()

send_mail_smtp(msg, 'mx.securemx.jp')

print("✅ API data retrieved, Excel created, email sent via SMTP")
