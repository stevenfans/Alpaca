import header
from header import api,api_key,secret_key, ti,clock
from stocks import Stock
from ta.trend import macd,macd_signal,macd_diff,sma_indicator
from ta.momentum import RSIIndicator
import time
from datetime import date, timedelta

# TODO: make it so that global variable is not needed
stock = ['AAPL','DIS']
stock_shares = {'AAPL':0,'DIS':0} # how many shares of stock do you have

def aggregate(stockSymbol):

    stock_detail = {}
    today = date.today()
    yesterday = today - timedelta(1) # get yesterday's date 
    tomorrow = today + timedelta(1)

    # aggregate data for all the symbols in the stock dictionary
    for sym in stockSymbol:
        stock_detail[sym] = api.polygon.historic_agg_v2(symbol=str(sym),multiplier=1,
                                timespan='day',_from='5-1-2019',to='5-23-2020').df# Dictionary of most recent earning stats for each compan

    # print(stock_detail)
    return stock_detail


def determineShare(symbol,budget):

    # Note: buy the maximum 

    close_price = currentClosePrice(symbol,'day')

    # return the maximum share able to purchase
    shares = budget//close_price
    return int(shares)

def currentClosePrice(symbol,timeframe):

    #get the current market price fromt he close bars
    barset = api.get_barset(symbol,timeframe=timeframe,limit=2)
    bar = barset[symbol]
    close_price = bar[-1].c
    
    return close_price

def scan(stock_detail,stock_budget):

    # scan the macd on the stock
    stock_macd = {}
    stock_macd_signal = {}
    stock_macd_diff = {}
    stock_sma = {}

    # get the macd of all the stocks
    for sym in stock_detail: 
        # perform a macd on the aggregated data
        stock_macd[sym] = macd(
            close = stock_detail[sym]['close'].dropna(),
        )
        stock_macd_signal[sym] = macd_signal(
            close = stock_detail[sym]['close'].dropna(),
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
        curr_price = currentClosePrice(sym,'day')

        print('PRICE: ' + str(curr_price))
        print("MACD: "+ str(stock_macd[sym][-1]))
        print("MACD SIGNAL: " + str(stock_macd_signal[sym][-1]))
        print("MACD DIFF:" + str(stock_macd_diff[sym][-1]))
        print("SMA: " + str(stock_sma[sym][-1])+'\n')


        # Buy Signal
        if ((stock_macd[sym][-1]<stock_macd_diff[sym][-1] and stock_macd_signal[sym][-1]<stock_macd_diff[sym][-1]) and #check for macd and signal neg ovr hist
            not(stock_macd_diff[sym][-3]>0 and stock_macd_diff[sym][-2]>0 and stock_macd_diff[sym][-1]>0) and #hist is not going neg
            (curr_price<stock_macd[sym][-1])):  #close price below 200 moving average

            # check how many share that the budget can afford
            shares = determineShare(sym, stock_budget[sym])

            # so macd looks good, so maybe want to buy?
            if shares>0 and clock.is_open():
                stock_shares[sym] = shares #update the shares about to buy
                api.submit_order(sym,shares,'buy','market','day')
                print("Buying Stock {symbol}".format(symbol=sym))

        # Sell Signal
        elif((stock_macd[sym][-1]>stock_macd_diff[sym][-1] and stock_macd_signal[sym][-1]>stock_macd_diff[sym][-1]) and #check for macd and signal pos ovr hist
            not(stock_macd_diff[sym][-3]<0 and stock_macd_diff[sym][-2]<0 and stock_macd_diff[sym][-1]<0) and #hist is not going pos
            (curr_price>stock_macd[sym][-1])):  #close price above 200 moving average

            # check if we have any shares of this stock
            if stock_shares[sym]>0 and clock.is_open():  
                print(stock_shares[sym])
                # sell all the shares
                api.submit_order(sym,stock_budget[sym],'sell','market','day')
                stock_shares[sym] = 0 #update the shares dictionary to 0, b/c sold all
                print("Selling Stock {symbol}".format(symbol=sym))


def main(): 

    # create account object 
    account = api.get_account()
    amount =  account.buying_power; 
    stock_budget = {'AAPL':100_000,'DIS':100_000}

    # Create clock entity

    while True: 
        stock_detail = aggregate(stock)
        scan(stock_detail,stock_budget)
        time.sleep(15)

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