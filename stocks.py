import alpaca_trade_api as tradeapi

class Stock:
    # important keys
    api_key    = "PKQ16Z77F6U39OELHIS2"
    secret_key = "2Ni8SNoFSpuVN92ZxRApFood7HGlyMqyo5ovvD1q"
    BASE_URL = "https://paper-api.alpaca.markets"

    # create the api object
    api = tradeapi.REST(api_key,secret_key,BASE_URL)

    def __init__(self,name,quantity,price):
        self.name = name
        self.quantity = quantity
        self.price = price

    def createOrder(self,symbol,qty,side,type,time_in_force,limit_price):
        details = {
            "symbol":self.symbol,
            "qty":self.qty,
            "side":self.side,
            "type":self.type,
            "time_in_force":self.time_in_force,
            "limit":self.limit_price
        }
        api.submit_order(symbol,qty,side,type,time_in_force,limit_price)
        return details 