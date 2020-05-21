# initial test to understand how the alpaca api works

import alpaca_trade_api as tradeapi
import requests

# https://algotrading101.com/learn/alpaca-trading-api-guide/

# important keys
api_key    = "PKQ16Z77F6U39OELHIS2"
secret_key = "2Ni8SNoFSpuVN92ZxRApFood7HGlyMqyo5ovvD1q"

# URLS
BASE_URL = "https://paper-api.alpaca.markets"
ACCOUNT_URL = "{}/v2/account".format(BASE_URL)

# create the api object
api = tradeapi.REST(api_key,secret_key,BASE_URL)

# get account info 
account = api.get_account()
print(account)

# Daily OHLCV dataframe
# aapl_daily = ap   i.polygon.historic_agg('day', 'AAPL', limit=1000).df# Dictionary of most recent earning stats for each company
list_earning = api.polygon.earnings(['MSFT','FB','AMZN'])# Returns a list articles and their meta-data
tsla_news = api.polygon.news('TSLA')

print(list_earning)
