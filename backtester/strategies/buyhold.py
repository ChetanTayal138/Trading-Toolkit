import backtrader as bt
import time

class BuyHoldStrategy(bt.Strategy):

    params = dict(
        quantity=0,
        status=0,
        printout=True,
        portfolio_value=10000,
        )



    def log(self, txt, dt=None):
            if self.p.printout:
                dt = dt or self.data.datetime[0]
                dt = bt.num2date(dt)
                print('%s, %s' % (dt.isoformat()[:10], txt))


    def notify_order(self, order):

        if order.status in [bt.Order.Submitted, bt.Order.Accepted]:
            return  # Await further notifications

        if order.status == order.Completed:
            if order.isbuy():
                buytxt = 'BUY COMPLETE, %.2f' % order.executed.price
                self.log(buytxt, order.executed.dt)
            else:
                selltxt = 'SELL COMPLETE, %.2f' % order.executed.price
                self.log(selltxt, order.executed.dt)

        elif order.status in [order.Expired, order.Canceled, order.Margin]:
            self.log('%s ,' % order.Status[order.status])
            pass  # Simply log

        # Allow new orders
        self.orderid = None


    def __init__(self):
        self.orderid = None
        self.quantity = self.p.quantity
        self.status = self.p.status
        self.portfolio_value = self.p.portfolio_value
        self.broker.set_coc(True)

    def next(self):
        print("---------------------------------")
        print(f"Trading Day {bt.num2date(self.data.datetime[0]).isoformat()[:10]} Summary")
        print(f"Start of Day Cash - {self.broker.getcash()}")

        if self.orderid:
            return

        if self.data.close[0] > self.data.close[-1] and self.data.close[-1] > self.data.close[-2]:
            self.log(f"Attempting Buy @ {self.data.close[0]}")
            self.buy()

            

        if self.data.close[0] < self.data.close[-1] and self.data.close[-1] < self.data.close[-2] :
            self.log(f"Closing Position @ {self.data.close[0]}")
            self.sell()
        #    self.log(f"Attempting Sell @ {self.data.close[0]}")
        #    self.sell()
        #129207.37289999991

        print(f"Current Asset Value : {self.data.close[0]}")
        print(f"End of Day Cash : {self.broker.getcash()}")
        print(f"End of Day Portfolio Value : {self.broker.getvalue()}")
        print(self.broker.get_fundshares())
        
    