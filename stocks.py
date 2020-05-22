from header import api, api_key,secret_key

class Stock:

    def __init__(self,symbol,qty,side,type,time_in_force,limit_price):
        self.symbol = symbol
        self.qty = qty
        self.side = side
        self.type = type
        self.time_in_force = time_in_force
        self.limit_price

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