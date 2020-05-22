import header
from header import api,api_key,secret_key
from stocks import Stock
from ta.trend import macd
import time

def main(): 
    aapl_daily = api.polygon.historic_agg_v2(symbol='aapl',multiplier=1,
                            timespan='day',_from='2020-1-1',to='5-21-2020').df# Dictionary of most recent earning stats for each company
    aapl_len = len(aapl_daily)
    hist = macd(
        close = aapl_daily['close'].dropna(),
        n_slow = 26,
        n_fast = 12,
    )
    histLen = len(hist)
    for i in hist:
        print(i)
    print("Done")


    # create clock entity
    clock = api.get_clock()
    while clock.is_open():
        # perform trades
        pass
    while clock.is_close(): 
        # read charts
        pass

if __name__ == "__main__": 
    main()