import requests
from datetime import date
import pandas as pd

FILENAME = "exchange_rate_sgd.xlsx"
CURRENCIES = ["JPY","THB","INR","SGD","VND","USD","IDR","PHP","TWD","EUR","GBP","MYR"]

today = date.today()
data = []

for c in CURRENCIES:
    if c == "SGD":
        rate = 1.0
    else:
        url = f"https://api.frankfurter.app/latest?from={c}&to=SGD"
        try:
            r = requests.get(url, timeout=10).json()
            rate_foreign_to_sgd = r["rates"]["SGD"]
            # convert to "Unit per SGD" = 1 SGD = X foreign units
            unit_per_sgd = round(1 / rate_foreign_to_sgd, 6)
            rate = unit_per_sgd
        except:
            rate = "N/A"
    data.append((today, c, rate))

df = pd.DataFrame(data, columns=["Date", "Currency", "Unit Per SGD"])
df.to_excel(FILENAME, index=False)

print(df)
