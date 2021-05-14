import numpy as np
import argparse
import datetime

import backtrader as bt
import backtrader.feeds as btfeeds
import backtrader.indicators as btind


import sys
sys.path.append("../quant")
from alphabeta_regression import normal_equation
import matplotlib.pyplot as plt
sys.path.append("../utils")
from pairs import OLS_TransformationN, OLS_TransformationN




class PairsTradingStrategy(bt.Strategy):

    params = dict(
        period=10,
        stake=10,
        qty1=0,
        qty2=0,
        printout=True,
        upper=2,
        lower=-2,
        up_medium=0.5,
        low_medium=-0.5,
        status=False,
        portfolio_value=100000,
    )


    def log(self, txt, dt=None):
            if self.p.printout:
                dt = dt or self.data.datetime[0]
                dt = bt.num2date(dt)
                print('%s, %s' % (dt.isoformat(), txt))

    def notify_order(self, order):


        if order.status in [bt.Order.Submitted, bt.Order.Accepted]:
            return  # Await further notifications

        if order.status == order.Completed:
            if order.isbuy():
                buytxt = 'BUY COMPLETE @ %.2f' % order.executed.price
                self.log(buytxt, order.executed.dt)
            else:
                selltxt = 'SELL COMPLETE @ %.2f' % order.executed.price
                self.log(selltxt, order.executed.dt)

        elif order.status in [order.Expired, order.Canceled, order.Margin]:
            self.log('%s ,' % order.Status[order.status])
            pass  # Simply log

        # Allow new orders
        self.orderid = None


    def __init__(self):

        self.orderid = None
        self.qty1 = self.p.qty1
        self.qty2 = self.p.qty2
        self.upper_limit = self.p.upper
        self.lower_limit = self.p.lower
        self.up_medium = self.p.up_medium
        self.low_medium = self.p.low_medium
        self.status = self.p.status
        self.portfolio_value = self.p.portfolio_value
        self.broker.set_coc(True)
        self.stock_1 = "AARTIDRUGS"
        self.stock_2 = "VAIBHAVGBL"
        self.spread_history = []

        
        #self.spread_indicator = SpreadIndicator(self.data0, self.data1, self.beta)
        #print(type(self.spread_indicator))
        #self.my_spread = self.spread_indicator.lines.spread
        self.transform = OLS_TransformationN(self.data0, self.data1, period=self.p.period)
        self.zscore = self.transform.zscore 

        #self.data1 - self.beta * self.data0
        
        

        #self.normalized_spread =(self.spread - self.spread.mean()) / self.spread.std()

        #plt.plot(self.normalized_spread)
        #plt.show()


    def next(self):


        if self.orderid:
            return  # if an order is active, no new orders are allowed

        """if self.p.printout:
            
            print('Data0 len:', len(self.data0))
            print('Data1 len:', len(self.data1))
            print('Data0 len == Data1 len:',
                  len(self.data0) == len(self.data1))

            print('Data0 dt:', self.data0.datetime.datetime())
            print('Data1 dt:', self.data1.datetime.datetime())"""

        #print('status is', self.status)
        print(f"Trading Day {bt.num2date(self.data.datetime[0]).isoformat()[:10]} Summary")

        print('Normalized Spread is', self.zscore[0])
        self.spread_history.append(self.zscore[0])
        #arr = vars(self.zscore)['array']

        # Step 2: Check conditions for SHORT & place the order
        # Checking the condition for SHORT
        if (self.zscore[0] > self.upper_limit) and (self.status != True):

            # Calculating the number of shares for each stock
            value = 0.25 * self.portfolio_value  # Divide the cash equally
            x = int(value / (self.data0.close))  # Find the number of shares for Stock1
            y = int(value / (self.data1.close))  # Find the number of shares for Stock2
            #print('x + self.qty1 is', x + self.qty1)
            #print('y + self.qty2 is', y + self.qty2)

            # Placing the order
            self.log('SELL CREATE %s, price = %.2f, qty = %d' % (self.stock_1, self.data0.close[0], x + self.qty1))
            self.sell(data=self.data0, size=(x + self.qty1))  # Place an order for buying y + qty2 shares
            self.log('BUY CREATE %s, price = %.2f, qty = %d' % (self.stock_2, self.data1.close[0], y + self.qty2))
            self.buy(data=self.data1, size=(y + self.qty2))  # Place an order for selling x + qty1 shares

            # Updating the counters with new value
            self.qty1 = x  # The new open position quantity for Stock1 is x shares
            self.qty2 = y  # The new open position quantity for Stock2 is y shares

            self.status = True  # The current status is "short the spread"

            # Step 3: Check conditions for LONG & place the order
            # Checking the condition for LONG
        elif (self.zscore[0] < self.lower_limit) and (self.status != True):

            # Calculating the number of shares for each stock
            value = 0.25 * self.portfolio_value  # Divide the cash equally
            x = int(value / (self.data0.close))  # Find the number of shares for Stock1
            y = int(value / (self.data1.close))  # Find the number of shares for Stock2
            print('x + self.qty1 is', x + self.qty1)
            print('y + self.qty2 is', y + self.qty2)

            # Place the order
            self.log('BUY CREATE %s, price = %.2f, qty = %d' % (self.stock_1, self.data0.close[0], x + self.qty1))
            self.buy(data=self.data0, size=(x + self.qty1))  # Place an order for buying x + qty1 shares
            self.log('SELL CREATE %s, price = %.2f, qty = %d' % (self.stock_2, self.data1.close[0], y + self.qty2))
            self.sell(data=self.data1, size=(y + self.qty2))  # Place an order for selling y + qty2 shares

            # Updatinqg the counters with new value
            self.qty1 = x  # The new open position quantity for Stock1 is x shares
            self.qty2 = y  # The new open position quantity for Stock2 is y shares
            self.status = True  # The current status is "long the spread"""


            # Step 4: Check conditions for No Trade
            # If the z-score is within the two bounds, close all
        
        elif (self.zscore[0] < self.up_medium and self.zscore[0] > self.low_medium and self.status == True):
            self.log('CLOSE %s, price = %.2f' % (self.stock_1, self.data0.close[0]))
            self.close(self.data0)
            self.log('CLOSE  %s, price = %.2f' % (self.stock_2, self.data1.close[0]))
            self.close(self.data1)
            self.status = False

        print("End of Day Portfolio Value is " + str(self.broker.getcash()))

    def stop(self):
        print('==================================================')
        print('Starting Value - %.2f' % self.broker.startingcash)
        print('Ending   Value - %.2f' % self.broker.getvalue())
        print('==================================================')
        print("Spread Length")
        print(len(self.spread_history))
        #plt.plot(self.spread_history)
        #plt.show()

















