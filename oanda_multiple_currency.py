import requests

url = "https://currencyapi.net/api/v1/rates"
params = {
    "key": "d0ce1c78aeac8044582639108c9e93967846",
    "base": "USD",
    "output": "JSON"
}

response = requests.get(url, params=params)
data = response.json()

print(data)
