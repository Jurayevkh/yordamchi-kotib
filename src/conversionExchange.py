import requests

def conversionCurrency(amount: float):
    API_KEY="189ecff57c4bbd5afa20c32f"

    currency="UZS"

    url=f"https://v6.exchangerate-api.com/v6/{API_KEY}/pair/{currency}/USD"

    response = requests.get(url)

    jsondata = response.json()
    kurs = response.json()['conversion_rate']
    return amount*kurs