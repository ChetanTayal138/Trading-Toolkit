import backtrader as bt
from backtrader import indicators
import time

class AverageCrossOverStrategy(bt.Strategy):

    params = dict(
        quantity=0,
        status=0,
        printout=True,
        portfolio_value=10000,
        p1= 50,
        p2=200,
        level = 1 # 3 levels of log, print daily logs if level is 1
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
                if self.level == 1:
                    self.log(buytxt, order.executed.dt)
            else:
                selltxt = 'SELL COMPLETE, %.2f' % order.executed.price
                if self.level == 1:
                    self.log(selltxt, order.executed.dt)

        elif order.status in [order.Expired, order.Canceled, order.Margin]:
            if self.level == 1:
                self.log('%s ,' % order.Status[order.status])
            pass  # Simply log

        # Allow new orders
        self.orderid = None


    def __init__(self):
        self.orderid = None
        self.status = self.p.status
        self.portfolio_value = self.p.portfolio_value
        self.broker.set_coc(True)
        self.sma1 = indicators.MovingAverageSimple(period=self.p.p1)
        self.sma2 = indicators.MovingAverageSimple(period=self.p.p2)
        self.level = self.p.level

    def next(self):
        if self.level == 1:
            print("---------------------------------")
            print(f"Trading Day {bt.num2date(self.data.datetime[0]).isoformat()[:10]} Summary")
            print(f"Start of Day Cash - {self.broker.getcash()}")

        if self.orderid:
            return
   
        if self.status == 0:
            if self.sma1 > self.sma2 : #Indicates that the fast moving average has crossed over the slow moving average
                self.buy()
                self.status = 1 

        elif self.status == 1:
            if self.sma1 <= self.sma2 :#Indicates that the slow moving average has crossed over the fast moving average
                self.close()
                self.status = 0

        if self.level == 1 :                
            print(f"f{self.p.p1}-Day Moving Average : {self.sma1}")
            print(f"f{self.p.p2}-Day Moving Average : {self.sma2}")
            print(f"Current Asset Value : {self.data.close[0]}")
            print(f"End of Day Cash : {self.broker.getcash()}")
            print(f"End of Day Portfolio Value : {self.broker.getvalue()}")
        
