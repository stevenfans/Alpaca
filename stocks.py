from header import api, api_key,secret_key

class Stock:

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