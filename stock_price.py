import requests

def get_stock_price(symbol):
    API_KEY = "key-here"
    url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={API_KEY}"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        price = data["c"]
        return price
    else:
        print("Error occurred:", response.status_code)
        return None
