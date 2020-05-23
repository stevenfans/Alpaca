import header
from header import api,api_key,secret_key
from stocks import Stock
from ta.trend import macd,macd_signal
from ta.momentum import rsi
import time
from datetime import date, timedelta

def aggregate(stockSymbol):

    stock_detail = {}
    today = date.today()
    yesterday = today - timedelta(1) # get yesterday's date 
    tomorrow = today + timedelta(1)

    # aggregate data for all the symbols in the stock dictionary
    for sym in stockSymbol:
        stock_detail[sym] = api.polygon.historic_agg_v2(symbol=str(sym),multiplier=1,
                                timespan='minute',_from=str(today),to=str(tomorrow)).df# Dictionary of most recent earning stats for each compan

    return stock_detail


def determineShare(symbol,budget):

    # Note: buy the maximum 

    # get the current market price from the close bars
    barset = api.get_barset(symbol,'minute',limit=2)
    bar = barset[symbol] 
    close_price = bar[-1].c

    # return the maximum share able to purchase
    shares = budget//close_price
    return int(shares)


def scan(stock_detail,buying_amount):

    # scan the macd on the stock
    stock_macd = {}
    stock_macd_signal = {}

    # get the macd of all the stocks
    for sym in stock_detail: 
        # perform a macd on the aggregated data
        stock_macd[sym] = macd(
            close = stock_detail[sym]['close'].dropna(),
            n_fast = 12,
            n_slow = 26
        )
        stock_macd_signal[sym] = macd_signal(
            close = stock_detail[sym]['close'].dropna(),
            n_fast = 12,
            n_slow = 26
        )

    # check the history for the macd
    for sym in stock_macd: 

        print("MACD: "+ str(stock_macd[sym][-1]))
        print("MACD SIGNAL: " + str(stock_macd_signal[sym][-1]))

        # check the macd is low and has a positive slope
        if stock_macd[sym][-1]> 0 and (stock_macd[sym][-3]<stock_macd[sym][-2]<stock_macd[sym][-1]): 
            # macd looks good so maybe trade now?
            # qty = determineShare(sym,buying_amount)
            # api.submit_order(sym,3,'buy','market','day')
            print("Buying Stock {symbol}".format(symbol=sym))



def main(): 

    stock = ['AAPL','DIS']

    # create account object 
    account = api.get_account()
    amount =  account.buying_power; 
    buying_amount = float(amount)/len(stock)

    while True: 
        stock_detail = aggregate(stock)
        scan(stock_detail,buying_amount)
        time.sleep(1)

    print("Done")


    # create clock entity
    # clock = api.get_clock()
    # while True: #inifinite loop
    #     while clock.is_open():
    #         # perform trades
    #         pass
    #     while clock.is_close(): 
    #         # read charts
    #         pass

if __name__ == "__main__": 
    main()