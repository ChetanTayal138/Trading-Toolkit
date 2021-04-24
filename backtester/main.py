import argparse
import datetime
import backtrader as bt
import backtrader.feeds as btfeeds
import backtrader.indicators as btind
import sys
import pandas as pd
sys.path.append("../quant")
from alphabeta_regression import normal_equation
import argparse
from strategy import PairTradingStrategy


def main():
    args = parse_args()
    print(args)
    pairs_file = pd.read_csv("./sectorwise_pairs.csv")
    pair_val = 0
    for pair in pairs_file.values[:26]:
        pair_val = pair_val + runstrategy(args, pair[0], pair[1])
        
    print("Average Portfolio Value")
    print(pair_val / 26 )

def runstrategy(args, s1, s2):


    cerebro = bt.Cerebro()

    fromdate = datetime.datetime.strptime(args.fromdate, '%Y-%m-%d')
    todate = datetime.datetime.strptime(args.todate, '%Y-%m-%d')

    data0 = btfeeds.YahooFinanceCSVData(
        dataname=args.path + s1 + ".csv",
        fromdate=fromdate,
        todate=todate)

    data1 = btfeeds.YahooFinanceCSVData(
        dataname=args.path + s2 + ".csv", 
        fromdate=fromdate,
        todate=todate)
    
    cerebro.adddata(data0)
    cerebro.adddata(data1)

    # Add the strategy
    cerebro.addstrategy(PairTradingStrategy)

    # Add the commission - only stocks like a for each operation
    cerebro.broker.setcash(args.cash)

    # Add the commission - only stocks like a for each operation
    cerebro.broker.setcommission(commission=args.commperc)

    # And run it
    val = cerebro.run()[0]
    
    val = val.broker.getvalue()
    print(val)

    # Plot if requested
    if args.plot:
        cerebro.plot(numfigs=args.numfigs, volume=False, zdown=False)

    return val


def parse_args():
    parser = argparse.ArgumentParser(description='MultiData Strategy')

    parser.add_argument('--path', type=str, 
                        default="../data/nse/NSE_1920/",
                        help="Path to folder containing csv files of security")


    parser.add_argument('--fromdate', '-f',
                        default='2018-01-01',
                        help='Starting date in YYYY-MM-DD format')

    parser.add_argument('--todate', '-t',
                        default='2020-01-01',
                        help='Starting date in YYYY-MM-DD format')


    parser.add_argument('--cash', default=100000, type=int,
                        help='Starting Cash')

    parser.add_argument('--runnext', action='store_true',
                        help='Use next by next instead of runonce')

    parser.add_argument('--nopreload', action='store_true',
                        help='Do not preload the data')

    parser.add_argument('--oldsync', action='store_true',
                        help='Use old data synchronization method')

    parser.add_argument('--commperc', default=0.001, type=float,
                        help='Percentage commission (0.005 is 0.5 percent')

    parser.add_argument('--stake', default=10, type=int,
                        help='Stake to apply in each operation')

    parser.add_argument('--plot', '-p', default=False, action='store_true',
                        help='Plot the read data')

    parser.add_argument('--numfigs', '-n', default=1,
                        help='Plot using numfigs figures')

    return parser.parse_args()


if __name__ == "__main__":

    main()