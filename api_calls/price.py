import requests

# Get price for specific Coin
def get_futures_current_price(symbol, client):
    url = f"https://fapi.binance.com/fapi/v1/ticker/price?symbol={symbol}"
    response = requests.get(url).json()

    price = float(response['price'])
    return price

# Get price for several Coins (coinsPrice = {} Needed)
def get_futures_current_price_coins(coinsList, client):
    coinsPrice = {}
    # Symbol, Price, Time
    futuresPrice = client.futures_symbol_ticker()
    for coins in coinsList:
        for coin in futuresPrice:
            if str(coin["symbol"]) == coins:
                coinsPrice[coins] = float(coin["price"])
    return coinsPrice
