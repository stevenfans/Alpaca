import alpaca_trade_api as tradeapi
import requests

# important keys
api_key    = "PKPYALRHNINVZLHLIXQX"
secret_key = "nIgH1J4D6SDVQ4QaC0RDHmvjBAXm744QsGOijFGr"

# URLS
BASE_URL = "https://paper-api.alpaca.markets"
ACCOUNT_URL = "{}/v2/account".format(BASE_URL)

# create the api object
api = tradeapi.REST(api_key,secret_key,BASE_URL)