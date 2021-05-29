import time
import argparse
import datetime
import backtrader as bt
import backtrader.feeds as btfeeds
import backtrader.indicators as btind
import sys
import pandas as pd
sys.path.append("../../quant")
from alphabeta_regression import normal_equation
import argparse
sys.path.append("../strategies")
from buyhold import BuyHoldStrategy


def strat_BuyHold(capital):
    args = parse_args()
    
    x = runstrategy(args, capital)
    return x
        
    

def runstrategy(args, capital):


    cerebro = bt.Cerebro()

    fromdate = datetime.datetime.strptime(args.fromdate, '%Y-%m-%d')
    todate = datetime.datetime.strptime(args.todate, '%Y-%m-%d')
    print(f"Running Backtest from {fromdate} to {todate}")
    if(capital == 0):
        print("No starting capital. Exiting...")
        return 0

    data = btfeeds.YahooFinanceCSVData(
        dataname=args.path + args.asset + ".csv",
        fromdate=fromdate,
        todate=todate)

    cerebro.adddata(data)

    # Add the strategy
    cerebro.addstrategy(BuyHoldStrategy)

    # Add the commission - only stocks like a for each operation
    cerebro.broker.setcash(capital) #CAPITAL


    # Add the commission - only stocks like a for each operation
    cerebro.broker.setcommission(commission=args.commperc) 

    # And run it

    val = cerebro.run()[0]
    
    val = val.broker.getvalue()
    
    print(val)

    # Plot if requested
    if args.plot:
        cerebro.plot(numfigs=args.numfigs, volume=True, zdown=False)

    return val


def parse_args():
    parser = argparse.ArgumentParser(description='MultiData Strategy')

    parser.add_argument('--path', type=str, 
                        default="../../data/nse/NSE_1920/",
                        help="Path to folder containing csv files of security")

    parser.add_argument('--asset', type=str,
                        default="nifty",
                        help="Name of asset")

    parser.add_argument('--fromdate', '-f',
                        default='2017-01-01',
                        help='Starting date in YYYY-MM-DD format')

    parser.add_argument('--todate', '-t',
                        default='2020-01-01',
                        help='Starting date in YYYY-MM-DD format')


    parser.add_argument('--cash', default=100000, type=int,
                        help='Starting Cash')

    parser.add_argument('--commperc', default=0.001, type=float,
                        help='Percentage commission (0.005 is 0.5 percent')

    parser.add_argument('--plot', '-p', default=False, action='store_true',
                        help='Plot the read data')

    parser.add_argument('--numfigs', '-n', default=1,
                        help='Plot using numfigs figures')

    return parser.parse_args()


if __name__ == "__main__":

    strat_BuyHold()