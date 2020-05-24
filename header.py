import alpaca_trade_api as tradeapi
import requests
from alpha_vantage.techindicators import TechIndicators

# important keys
api_key    = "PKPYALRHNINVZLHLIXQX"
secret_key = "nIgH1J4D6SDVQ4QaC0RDHmvjBAXm744QsGOijFGr"

alpha_api_key = " INYRU0Y7TU47R2BN"

# URLS
BASE_URL = "https://paper-api.alpaca.markets"
ACCOUNT_URL = "{}/v2/account".format(BASE_URL)

# create the api object
api = tradeapi.REST(api_key,secret_key,BASE_URL)

ti = TechIndicators(key=alpha_api_key,output_format='pandas')

data_ti,meta_data_ti = ti.get_macd(symbol='AAPL',interval='daily',
                                series_type='close',fastperiod=12,
                                slowperiod=26,signalperiod=9)

print(data_ti['MACD_Hist'][-1])

