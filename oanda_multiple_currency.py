from bs4 import BeautifulSoup
from datetime import date
import pandas as pd
import os
import time
import smtplib
import mimetypes
import ssl
from email.message import EmailMessage

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# =========================
# CONFIG
# =========================
FILENAME = "oanda_exchange_rate_sgd.xlsx"

CURRENCIES = [
    "JPY", "THB", "INR", "SGD", "VND",
    "USD", "IDR", "PHP", "TWD",
    "EUR", "GBP", "MYR"
]

# =========================
# SCRAPE FUNCTION
# =========================
def get_currency(in_currency, out_currency="SGD"):
    url = f"https://www.oanda.com/currency-converter/en/?from={in_currency}&to={out_currency}&amount=1"

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    driver.get(url)
    time.sleep(6)  # wait for JS to render

    soup = BeautifulSoup(driver.page_source, "html.parser")
    
    # Grab the actual converted value
    try:
        value = soup.find("p", class_="fx-output").text.strip()
    except:
        value = "N/A"

    driver.quit()
    return value

# =========================
# MAIN
# =========================
if os.path.exists(FILENAME):
    os.remove(FILENAME)

today = date.today()
data = []

for c in CURRENCIES:
    rate = get_currency(c)
    print(f"{rate} - {c}")
    data.append((today, c, rate))

df = pd.DataFrame(data, columns=["Date", "Currency", "Unit Per SGD"])
df.to_excel(FILENAME, index=False)

# =========================
# EMAIL (GMAIL → irene.ng@takenaka.com.sg)
# =========================
EMAIL_USER = os.environ["EMAIL_USER"]
EMAIL_PASS = os.environ["EMAIL_PASS"]

msg = EmailMessage()
msg["Subject"] = "Daily Currency Trigger"
msg["From"] = EMAIL_USER                # Gmail sender
msg["To"] = "irene.ng@takenaka.com.sg" # Corporate recipient
msg.set_content("Please see attached currency exchange file.")

with open(FILENAME, "rb") as f:
    file_data = f.read()
    maintype, _, subtype = (mimetypes.guess_type(FILENAME)[0] or "application/octet-stream").partition("/")
    msg.add_attachment(
        file_data,
        maintype=maintype,
        subtype=subtype,
        filename=FILENAME
    )

context = ssl.create_default_context()

with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(EMAIL_USER, EMAIL_PASS)
    server.send_message(msg)

print("✅ Email sent successfully via Gmail to irene.ng@takenaka.com.sg")
