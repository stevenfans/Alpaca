import header
from header import api,api_key,secret_key, ti
from stocks import Stock
from ta.trend import macd,macd_signal,macd_diff,sma_indicator
from ta.momentum import RSIIndicator
import time
from datetime import date, timedelta

posMACD = False; 

def aggregate(stockSymbol):

    stock_detail = {}
    today = date.today()
    yesterday = today - timedelta(1) # get yesterday's date 
    tomorrow = today + timedelta(1)

    # aggregate data for all the symbols in the stock dictionary
    for sym in stockSymbol:
        stock_detail[sym] = api.polygon.historic_agg_v2(symbol=str(sym),multiplier=1,
                                timespan='minute',_from='5-20-2020',to='5-22-2020').df# Dictionary of most recent earning stats for each compan

    # print(stock_detail)
    return stock_detail


def determineShare(symbol,budget):

    # Note: buy the maximum 

    close_price = currentClosePrice(symbol,'daily')

    # return the maximum share able to purchase
    shares = budget//close_price
    return int(shares)

def currentClosePrice(symbol,timeframe):

    #get the current market price fromt he clseo bars
    barset = api.get_barset(symbol=symbol,timeframe=timeframe,limit=2)
    bar = barset[symbol]
    close_price = bar[-1].c
    
    return close_price

def scan(stock_detail,buying_amount):

    # scan the macd on the stock
    stock_macd = {}
    stock_macd_signal = {}
    stock_macd_diff = {}
    stock_sma = {}
    # data_ti = {}
    # meta_data_ti = {}
    # moving_data = {}

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
        stock_macd_diff[sym] = macd_diff(
            close = stock_detail[sym]['close'].dropna(),
        )

        # get 200 day sma
        stock_sma[sym] = sma_indicator(
            close = stock_detail[sym]['close'].dropna(),
            n = 200
        )


    for sym in stock_macd: 
        # print(stock_macd[sym])
        print("MACD: "+ str(stock_macd[sym][-1]))
        print("MACD SIGNAL: " + str(stock_macd_signal[sym][-1]))
        print("MACD DIFF:" + str(stock_macd_diff[sym][-1]))
        print("SMA: " + str(stock_sma[sym][-1]))

        # Buy Signal
        if ((stock_macd[sym][-1]<0 and stock_macd_signal[-1]<0) and #check for macd and signal negative
            not(stock_macd_diff[-3]>0 and stock_macd_diff[-2]>0 and stock_macd_diff[-1]>0)): #hist is not going neg: #close price above 200 moving average
            pass
        #     # macd looks good so maybe trade now?
        #     # qty = determineShare(sym,buying_amount)
        #     # api.submit_order(sym,3,'buy','market','day')
        #     print("Buying Stock {symbol}".format(symbol=sym))


#######################################################################################
        # # Getting MACD using alpha vantage
        # # 5 calls per min 
        # data_ti[sym],meta_data_ti[sym] = ti.get_macd(symbol=sym,interval='daily',
        #                                 series_type='close',fastperiod=12,
        #                                 slowperiod=26,signalperiod=9)

        # # Get the simple moving average
        # moving_data[sym] = ti.get_sma(symbol=sym,interval='daily',time_period=200,series_type='close')

        # print(moving_data['AAPL'][0]['SMA'])

        # # check the history for the macd
        # # determine when to buy
        # if ((data_ti[sym]['MACD'][-1]<0 and data_ti[sym]['MACD_Signal'][-1]<0) and 
        #     not(data_ti[sym]['MACD_Hist'][-3]>data_ti['MACD_Hist'][sym][-2]>data_ti['MACD_Hist'][sym][-1])):
        #     print('BUY STOCK')

        # # determine whent to sell the stock
        # elif((data_ti[sym]['MACD'][-1]>0 and data_ti[sym]['MACD_Signal'][-1]>0) and 
        #     not(data_ti['MACD_Hist'][sym][-3]<data_ti['MACD_Hist'][sym][-2]<data_ti['MACD_Hist'][sym][-1])):
        #     print("SELL")






def main(): 

    stock = ['AAPL','DIS']

    # create account object 
    account = api.get_account()
    amount =  account.buying_power; 
    buying_amount = float(amount)/len(stock)


    # check initial histogram from MACD


    while True: 
        stock_detail = aggregate(stock)
        scan(stock_detail,buying_amount)
        time.sleep(30)

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