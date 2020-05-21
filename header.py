import alpaca_trade_api as tradeapi
import requests

# important keys
api_key    = "PKQ16Z77F6U39OELHIS2"
secret_key = "2Ni8SNoFSpuVN92ZxRApFood7HGlyMqyo5ovvD1q"

# URLS
BASE_URL = "https://paper-api.alpaca.markets"
ACCOUNT_URL = "{}/v2/account".format(BASE_URL)

# create the api object
api = tradeapi.REST(api_key,secret_key,BASE_URL)