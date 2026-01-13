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

# -----------------------------
# File setup
# -----------------------------
filename = "oanda_exchange_rate_sgd.xlsx"
if os.path.exists(filename):
    os.remove(filename)

# -----------------------------
# Function to scrape currency
# -----------------------------
def get_currency(in_currency, out_currency):
    url = f"https://www.oanda.com/currency-converter/en/?from={in_currency}&to={out_currency}&amount=1"

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Use webdriver-manager to install ChromeDriver automatically
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    currency_unit = soup.find(
        "input",
        {"class": "MuiInputBase-input MuiFilledInput-input"}
    ).get("value")

    driver.quit()
    return currency_unit

# -----------------------------
# Currency list
# -----------------------------
country = ["JPY","THB","INR","SGD","VND","USD","IDR","PHP","TWD","EUR","GBP","MYR"]

data = []
today = date.today()

for c in country:
    rate = get_currency(c, "SGD")
    data.append((today, c, rate))
    print(rate, "-", c)

# -----------------------------
# Save Excel
# -----------------------------
df = pd.DataFrame(data, columns=["Date", "Currency", "Unit Per SGD"])
df.to_excel(filename, index=False)

# -----------------------------
# Email via Microsoft 365
# -----------------------------
EMAIL_USER = os.environ["EMAIL_USER"]
EMAIL_PASS = os.environ["EMAIL_PASS"]

print(EMAIL_USER)
msg = EmailMessage()
msg["Subject"] = "Daily Currency Trigger"
msg["From"] = EMAIL_USER
msg["To"] = EMAIL_USER
msg.set_content("Please see attached file.")

with open(filename, "rb") as f:
    file_data = f.read()
    maintype, _, subtype = (mimetypes.guess_type(filename)[0] or "application/octet-stream").partition("/")
    msg.add_attachment(file_data, maintype=maintype, subtype=subtype, filename=filename)

context = ssl.create_default_context()

with smtplib.SMTP("smtp.office365.com", 587) as server:
    server.starttls(context=context)
    server.login(EMAIL_USER, EMAIL_PASS)
    server.send_message(msg)

print("Email sent successfully")
