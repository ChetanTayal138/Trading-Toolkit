import argparse
import datetime
import backtrader as bt
import backtrader.feeds as btfeeds
import backtrader.indicators as btind
import backtrader.analyzers as btanalyzers

import sys
import pandas as pd
import numpy as np
sys.path.append("../../quant")
from alphabeta_regression import normal_equation
import argparse
sys.path.append("../strategies")
from pairstrading import PairsTradingStrategy
import pyfolio as pf

def strat_PairsTrading(write_to_file=False):
    args = parse_args()
    CHOICE = "cluster"
    START = "2017-01-01"
    END = "2019-01-01"
    print(args)
    """Average Portfolio Value - Sector wise - clusters formed from 2017-2019 and backtest from 2019-2021
    91015.05030088508
    Average Drawdown
    24.223947690718358
    Average Sharpe
    -0.6838018071780648
    Average Std Dev
    0.05519555976405521

    Average Portfolio Value - Cluster wise - clusters formed from 2017-2019 and backtest from 2019-2021
    102078.95401333341
    Average Drawdown
    13.563933427331653
    Average Sharpe
    1.4313811311074438
    Average Std Dev
    0.00993864773758297
    
    Average Portfolio Value - Cluster Wise - clusters formed from 2019-2021and backtest from 01/01/21 to 01/04/21
    
    100148.41235
    Average Drawdown
    0.8803418298344439
    Average Std Dev
    0.0021904436046547423

    Average Portfolio Value - Sector Wise - clusters formed from 2019-2021 and backtest from 01/01/21 to 01/04/21
    99924.40644136231
    Average Drawdown
    0.9987093498211609
    Average Std Dev
    0.0021588766218318027"""



    pairs_file = pd.read_csv(f"../data/{CHOICE}wise_pairs_{START}_{END}.csv")
    
    #pairs_file = pd.read_csv(f"../data/{CHOICE}wise_winners.txt", delimiter=" ")    
    #pairs_file = pairs_file.sort_values('PORTFOLIO_VALUE', ascending=False).iloc[:5, :2]
    
    pair_val = 0
    dd_val = 0
    sharpe_val = 0
    stddev_val = 0
    j = 0
    
    for pair in pairs_file.values[:1]:
        print(pair)
        try:
            curr_val, drawdown, sharpe, returns = runstrategy(args, pair[0], pair[1])
            if write_to_file == True:
                if curr_val > args.cash:
                    with open(f"../data/{CHOICE}wise_winners.txt", "w") as f:
                        f.write(f"{pair[0]} {pair[1]} {curr_val}\n")

            
            pair_val = pair_val + curr_val
            dd_val = dd_val + drawdown
            stddev_val = np.std(returns.values) + stddev_val
            sharpe_val = sharpe_val + sharpe

            j = j + 1

        except: 
            pass
        
    print("Average Portfolio Value")
    print(pair_val / j )
    print("Average Drawdown")
    print(dd_val / j)
    print("Average Std Dev")
    print(stddev_val / j)
    print("Average Sharpe")
    print(sharpe_val / j)

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
    cerebro.addstrategy(PairsTradingStrategy)

    # Add the commission - only stocks like a for each operation
    cerebro.broker.setcash(args.cash)

    # Add the commission - only stocks like a for each operation
    cerebro.broker.setcommission(commission=args.commperc)

    cerebro.addanalyzer(btanalyzers.SharpeRatio, _name='mysharpe')
    cerebro.addanalyzer(btanalyzers.PyFolio, _name='pyfolio')
    cerebro.addanalyzer(btanalyzers.DrawDown, _name='drawdown' )
    cerebro.addanalyzer(btanalyzers.Returns, _name='returns')

    # And run it
    val = cerebro.run()
    
    final_portfolio_value = val[0].broker.getvalue()
    drawdown_value = val[0].analyzers.getbyname('drawdown')
    sharpe_value = val[0].analyzers.getbyname('mysharpe').get_analysis()['sharperatio']    
    drawdown = drawdown_value.get_analysis()['drawdown']
    pyfoliozer = val[0].analyzers.getbyname('pyfolio')
    returns = val[0].analyzers.getbyname('returns')

    returns, positions, transactions, gross_lev = pyfoliozer.get_pf_items()
    print(returns)
    print(positions)
    print(transactions)
    
    #pf.create_full_tear_sheet( returns, positions=positions, transactions=transactions, live_start_date="2019-01-05",round_trips=True)
    if args.plot:
        cerebro.plot(numfigs=args.numfigs, volume=False, zdown=False)

    return final_portfolio_value, drawdown, sharpe_value, returns


def parse_args():
    parser = argparse.ArgumentParser(description='MultiData Strategy')

    parser.add_argument('--path', type=str, 
                        default="../../data/nse/NSE_1920/",
                        help="Path to folder containing csv files of security")


    parser.add_argument('--fromdate', '-f',
                        default='2019-01-01',
                        help='Starting date in YYYY-MM-DD format')

    parser.add_argument('--todate', '-t',
                        default='2021-01-01',
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

    parser.add_argument('--plot', '-p', default=True, action='store_true',
                        help='Plot the read data')

    parser.add_argument('--numfigs', '-n', default=1,
                        help='Plot using numfigs figures')

    return parser.parse_args()


if __name__ == "__main__":

    strat_PairsTrading(write_to_file=True)