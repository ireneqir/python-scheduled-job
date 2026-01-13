import requests
from datetime import date
import pandas as pd

FILENAME = "exchange_rate_sgd.xlsx"

# currencies you want
CURRENCIES = ["JPY","THB","INR","SGD","VND","USD","IDR","PHP","TWD","EUR","GBP","MYR"]

today = date.today()
data = []

for c in CURRENCIES:
    if c == "SGD":
        rate = 1.0  # 1 SGD = 1 SGD
    else:
        try:
            # Frankfurter API returns 1 FOREIGN = X SGD
            url = f"https://api.frankfurter.app/latest?from={c}&to=SGD"
            r = requests.get(url, timeout=10).json()
            foreign_to_sgd = r["rates"]["SGD"]
            # invert to get 1 SGD = ? FOREIGN
            rate = round(1 / foreign_to_sgd, 5)
        except Exception as e:
            print(f"Error fetching {c}: {e}")
            rate = "N/A"
    
    data.append((today, c, rate))

# create DataFrame
df = pd.DataFrame(data, columns=["Date", "Currency", "Unit Per SGD"])

# save Excel
df.to_excel(FILENAME, index=False)

print(df)
