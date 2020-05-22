import header
from header import api,api_key,secret_key
from stocks import Stock
from ta.trend import macd
from ta.momentum import rsi
import time
from datetime import date, timedelta

def aggregate(stockSymbol):

    stock_detail = {}
    today = date.today()
    yesterday = today - timedelta(1) # get yesterday's date 

    # aggregate data for all the symbols in the stock dictionary
    for sym in stockSymbol:
        stock_detail[sym] = api.polygon.historic_agg_v2(symbol=str(sym),multiplier=1,
                                timespan='minute',_from=str(yesterday),to=str(today)).df# Dictionary of most recent earning stats for each compan

    return stock_detail

def main(): 
    stock = ['AAPL','DIS']

    stock_detail = aggregate(stock)
    stock_macd = {}

    # get the macd of all the stocks
    for sym in stock_detail: 
        # perform a macd on the aggregated data
        stock_macd[sym] = macd(
            close = stock_detail[sym]['close'].dropna(),
            n_fast = 12,
            n_slow = 26
        )

        print(str(sym))
    
    # check the history for the macd
    for sym in stock_macd: 

        if stock_macd[sym][]

    # while True: 
    #     # playing with apple for now
    #     aapl_daily = api.polygon.historic_agg_v2(symbol='AAPL',multiplier=1,
    #                             timespan='minute',_from='5-20-2020',to='5-21-2020').df# Dictionary of most recent earning stats for each company
    #     aapl_len = len(aapl_daily)
    #     hist = macd(
    #         close = aapl_daily['close'].dropna(),
    #         n_slow = 26,
    #         n_fast = 12,
    #     )
    #     hist2 = rsi(
    #         close = aapl_daily['close'].dropna(),
    #         n = 12
    #     ) 
    #     time.sleep(1)


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