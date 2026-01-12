# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 15:19:05 2023

@author: irene.ng
"""


from bs4 import BeautifulSoup
from datetime import date
import pandas as pd
import os
import time
import smtplib
import mimetypes
from email.message import EmailMessage

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

#delete file first before create one to avoid some issue
filename = 'oanda_exchange_rate_sgd.xlsx'
if os.path.exists(filename):
    os.remove(filename)


def get_currency(in_currency,out_currency):
   url=f'https://www.oanda.com/currency-converter/en/?from={in_currency}&to={out_currency}&amount=1'
   s = Service(r"D:/chromedriver-win64/chromedriver.exe")
  
  
   options = webdriver.ChromeOptions()
   
   options.add_argument('--ignore-certificate-errors-spki-list')
   options.add_argument('--ignore-ssl-errors')
   driver = webdriver.Chrome(options)
   driver = webdriver.Chrome(service=s)
   driver.get(url)
   time.sleep(15)
  #driver = webdriver.Chrome('C:/chromedriver-win64/chromedriver.exe')
   #driver.get(url)
   c = driver.page_source
   soup = BeautifulSoup(c, "html.parser")
 
   currency_unit = soup.find('input', {'class':"MuiInputBase-input MuiFilledInput-input",'tabindex':"4"}).get('value')
   
   #print (currency_unit)
   driver.close()
   return currency_unit
   
   

#country = ["CNY","USD","JPY","EUR","THB","KRW","INR","HKD","NOK","SGD","MMK","VND","GBP","IDR","SEK","CZK","TWD","PLN","CHF","AED","ILS","KHR","PHP","MYR","HUF","RON","RSD","ADA"] 
country = ["JPY","THB","INR","SGD","VND","USD","IDR","PHP","TWD","EUR","GBP","MYR"]   
cols=['Date', 'Currency','Unit Per SGD']

data = []
today = date.today()

for x in range(len(country)):
    exchange_rate=get_currency(country[x], "SGD")
    data.append((today, 
                     country[x], 
                     exchange_rate))
    print(exchange_rate,"-",country[x])


result = pd.DataFrame(data, columns=cols)
result.to_excel('D:\BusinessTripScraping/oanda_exchange_rate_sgd.xlsx', sheet_name='rate')
print(result)

# Create message and set text content
msg = EmailMessage()
msg['Subject'] = 'Daily Currency Trigger'
msg['From'] = 'irene.ng@takenaka.com.sg'
msg['To'] = 'irene.ng@takenaka.com.sg'
# Set text content
msg.set_content('Please see attached file')
def attach_file_to_email(email, filename):
    """Attach a file identified by filename, to an email message"""
    with open(filename, 'rb') as fp:
        file_data = fp.read()
        maintype, _, subtype = (mimetypes.guess_type(filename)[0] or 'application/octet-stream').partition("/")
        email.add_attachment(file_data, maintype=maintype, subtype=subtype, filename=filename)
# Attach files
attach_file_to_email(msg, "oanda_exchange_rate_sgd.xlsx")
def send_mail_smtp(mail, host):
    s = smtplib.SMTP(host,port=25)
    s.starttls()
    #s.login(username, password)
    s.send_message(mail)
    s.quit()
send_mail_smtp(msg, 'mx.securemx.jp')