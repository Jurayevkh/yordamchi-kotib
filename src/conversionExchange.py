import requests

def conversionCurrency(which_currency: str,to_which_currency: str,amount: float):
    API_KEY="189ecff57c4bbd5afa20c32f"

    url=f"https://v6.exchangerate-api.com/v6/{API_KEY}/pair/{which_currency}/{to_which_currency}"

    response = requests.get(url)

    jsondata = response.json()
    kurs = jsondata["conversion_rate"]
    rounded_value=round(float(amount*kurs), 3)
    formatted_value = f"{rounded_value:,.2f}"
    return formatted_value