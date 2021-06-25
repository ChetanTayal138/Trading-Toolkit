import os
import time
import argparse
import datetime
import backtrader as bt
import backtrader.feeds as btfeeds
import backtrader.indicators as btind
import backtrader.analyzers as btanalyzers
import json
import sys
import pandas as pd
import argparse
sys.path.append("../strategies")
from averagecrossover import AverageCrossOverStrategy 
import multiprocessing
from ctypes import Structure, c_double
from multiprocessing.sharedctypes import Array

class Result(Structure):
    _fields_ = [('value', c_double), ('sharpe', c_double), ('drawdown', c_double)]

class StrategyExperiment :

    def __init__(self, strategy, pairs):
        self.strategy = strategy
        self.pairs =  pairs
        self.args = parse_args()
        self.multiprocess = self.args.multiprocess
        self.json_data = {}
    
    def start_experiment(self):
        self.processes = [] 

        for ticker in sorted(os.listdir(self.args.path))[:10]:
            self.ticker = ticker
            ticker_metrics = {} 
            print(f"Running experiment for {ticker}")
            try:
                if self.multiprocess == "True" :
                    self.results = []
                    for i in self.pairs :

                        curr_res = Array(Result, [(-1.0,-1.0, -1.0)])
                        self.results.append(curr_res)
                        fast = self.pairs[i]["fast"]
                        slow = self.pairs[i]["slow"]
                        p = multiprocessing.Process(target = self.strategy, args=(self.args, ticker, fast, slow, self.results[-1])) 
                        self.processes.append(p)
                        p.start()

                    self.end_experiment()

                else:
                    for i in self.pairs:
                        fast = self.pairs[i]["fast"]
                        slow = self.pairs[i]["slow"]

                        val,sharpe,dd = self.strategy(self.args,ticker,fast,slow)
                        ticker_metrics[f"{fast}-{slow}"] = {"value" :val,"sharpe" : sharpe,"drawdown" : dd}
                        self.json_data[ticker] = ticker_metrics        
            except Exception as e:
                    if self.multiprocess == "False":

                        for i in self.pairs:
                            fast = self.pairs[i]["fast"]
                            slow = self.pairs[i]["slow"] 
                            ticker_metrics[f"{fast}-{slow}"] = {"value" :-1,"sharpe" : -1,"drawdown" : -1}
                            self.json_data[ticker] = ticker_metrics        
                
                    else:
                        pass
       
        if self.multiprocess == "True":  
            with open("./metrics_multiprocess.json", "w") as outfile:
                json.dump(self.json_data, outfile)
        else:

            with open("./metrics_singleprocess.json", "w") as outfile:
                json.dump(self.json_data, outfile)

    def end_experiment(self):
        for process in self.processes:
            process.join()

        self.log_experiment()

    def log_experiment(self):
        """
        Expected json to be created should have the following structure

        {
            "ticker1" : {
                            "30-50" : {
                                        "value" : 1000,
                                        "sharpe" : 1,
                                        "drawdown": 0.5,
                            },

                            "50-100" : {
                                        .
                                        .
                                        .
                            },
                            .
                            .
                            .
                            .
            },

            "ticker2" : {
                            .
                            .
                            .

            },
        
        }
        """

        self.json_data[self.ticker] = {}
        for idx, res in enumerate(self.results):
            curr_data = {}
            word = f"{self.pairs[idx+1]['fast']}-{self.pairs[idx+1]['slow']}"
            pair_results = res[0]

            curr_data[word] = {
                    "value" : pair_results.value,
                    "sharpe" : pair_results.sharpe,
                    "drawdown" : pair_results.drawdown
                    }
            self.json_data[self.ticker][word] = curr_data[word]

def runstrategy(args, TICKER, FAST, SLOW, results=None):


    cerebro = bt.Cerebro()
    fromdate = datetime.datetime.strptime(args.fromdate, '%Y-%m-%d')
    todate = datetime.datetime.strptime(args.todate, '%Y-%m-%d')
    

    data = btfeeds.YahooFinanceCSVData(
        dataname= args.path + TICKER, 
        fromdate=fromdate, 
        todate=todate) 
    
    cerebro.adddata(data)

    # Add the strategy
    cerebro.addstrategy(AverageCrossOverStrategy, p1=FAST, p2=SLOW, level=3)

    # Add the commission - only stocks like a for each operation
    cerebro.broker.setcash(args.cash)

    # Add the commission - only stocks like a for each operation
    cerebro.broker.setcommission(commission=args.commperc) 

    cerebro.addanalyzer(btanalyzers.SharpeRatio, _name='mysharpe', convertrate=True, timeframe=bt.TimeFrame.Days)
    cerebro.addanalyzer(btanalyzers.DrawDown, _name='drawdown' )
    cerebro.addanalyzer(btanalyzers.Returns, _name='returns')
    # And run it
    try :
        val = cerebro.run()
        
        final_portfolio_value = val[0].broker.getvalue()
        sharpe_value = val[0].analyzers.getbyname('mysharpe').get_analysis()['sharperatio']    
        drawdown_value = val[0].analyzers.getbyname('drawdown').get_analysis()['drawdown']
        returns = val[0].analyzers.getbyname('returns').get_analysis()
        # And run it
        # Plot if requested
        if args.plot:
            cerebro.plot(numfigs=args.numfigs, volume=True, zdown=False)

        if results is not None:
            for x in results : 
                x.value = final_portfolio_value
                x.sharpe = sharpe_value
                x.drawdown = drawdown_value
                return 

        #print([(a.value, a.sharpe, a.drawdown) for a in results])
        return final_portfolio_value,sharpe_value,drawdown_value
    except Exception as e:
        return e

def parse_args():
    parser = argparse.ArgumentParser(description='CrossoverStrategy')

    parser.add_argument('--path', type=str, 
                        default="../../data/nse/NSE_1920/",
                        help="Path to folder containing csv files of security")


    parser.add_argument('--fromdate', '-f',
                        default='2016-01-01',
                        help='Starting date in YYYY-MM-DD format')

    parser.add_argument('--todate', '-t',
                        default='2021-04-01',
                        help='Starting date in YYYY-MM-DD format')

    parser.add_argument('--multiprocess', default="False", type=str,
                        help='Indicate wether to make use of multiple cores for different pairs')

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
    periods = {
        1 : {"fast" : 30, "slow" : 50},
        2 : {"fast" : 30, "slow" : 100},        
        3 : {"fast" : 30, "slow" : 150},
        4 : {"fast" : 30, "slow" : 200},
        5 : {"fast" : 50, "slow" : 100},
        6 : {"fast" : 50, "slow" : 150},
        7 : {"fast" : 50 ,"slow" : 200},
        8 : {"fast" : 100, "slow" : 150},
        9 : {"fast" : 100, "slow" : 200},
        10 : {"fast" : 150, "slow" : 200},
        }


    #strat_AverageCrossover()
    c = StrategyExperiment(runstrategy, periods)
    starttime = time.time()
    c.start_experiment()
    print('That took {} seconds'.format(time.time() - starttime))

