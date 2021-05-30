from statsmodels.tsa.stattools import coint
import sys
sys.path.append("../quant")
from alphabeta_regression import normal_equation
import numpy as np
import matplotlib.pyplot as plt
import backtrader as bt
from backtrader.indicators import PeriodN
import json

class PairChecker:


    def __init__(self, cluster, cluster_dataframe):

        self.cluster = cluster
        self.cluster_size = len(cluster)
        self.data = cluster_dataframe
        self.pairs = []

    def check_cointegration(self, cutoff=0.05, hurst_threshold=0.5):
        """Carry out augmented dicky-fuller test on X"""
        number_of_checks = 0
        for i in range(self.cluster_size):
            for j in range(i+1, self.cluster_size):
                number_of_checks = number_of_checks + 1

                try:
                    print(f"Checking for cointegration between {self.cluster[i]}--{self.cluster[j]}")

                    S1 = self.data.iloc[:, i]
                    S2 = self.data.iloc[:, j]
                    
                    alpha, beta = normal_equation(S2.values.reshape(-1,1), S1.values.reshape(-1,1))
                    spread = S2 - beta * S1

                    p_value = coint(S1,S2)[1]

                    if(p_value) > cutoff:
                        pass
                        #print("Series is unlikely cointegrated")
                    else:
                        hurst_value = self.check_hurst(spread)
                        
                        if hurst_value < hurst_threshold:
                            halflife_value = self.check_half_life(spread)
                            print(halflife_value)
                            if halflife_value > 1 and halflife_value < 100:
                        #print("Series is likely cointegrated")
                                self.pairs.append( [self.cluster[i], self.cluster[j]])

                except Exception as e:
                    print(e)
                    #print("Error...")
            
        return self.pairs, number_of_checks

    def check_hurst(self, spread):
        spread = spread.values

        lags = range(2,100)
        #tau = [np.sqrt(np.std(np.subtract(spread[lag:], spread[:-lag]))) for lag in lags]
        
        #poly = np.polyfit(np.log(lags), np.log(tau), 1)

        variancetau = []; tau = []

        for lag in lags: 
            tau.append(lag)

            pp = np.subtract(spread[lag:], spread[:-lag])   
            variancetau.append(np.var(pp))
    
        m = np.polyfit(np.log(tau),np.log(variancetau),1)


        hurst = m[0] / 2


        return hurst

        return poly[0] * 2.0

    def check_half_life(self, spread):
        spread = spread.values
        spread_lag = np.roll(spread, 1)
        spread_lag[0] = 0
        spread_ret = spread - spread_lag
        spread_ret[0] = 0

        alpha, beta = normal_equation(spread_ret[1:].reshape(-1,1), spread_lag[1:].reshape(-1,1))
        halflife = -np.log(2) / beta

        return halflife



class OLS_Slope_InterceptN(PeriodN):
    '''
    Calculates a linear regression using ``statsmodel.OLS`` (Ordinary least
    squares) of data1 on data0
    Uses ``pandas`` and ``statsmodels``
    '''
    _mindatas = 2  # ensure at least 2 data feeds are passed

    packages = (
        ('pandas', 'pd'),
        ('statsmodels.api', 'sm'),
    )
    lines = ('slope', 'intercept',)
    params = (
        ('period', 10),
    )

    def next(self):
        p0 = pd.Series(self.data0.get(size=len(self.data0))).values
        p1 = pd.Series(self.data1.get(size=len(self.data1))).values

        #alpha, beta = normal_equation(p1.reshape(-1,1), p0.reshape(-1,1))
        p1 = sm.add_constant(p1)
        intercept, slope = sm.OLS(p0, p1).fit().params
        

        self.lines.slope[0] = intercept
        self.lines.intercept[0] = slope


class OLS_TransformationN(PeriodN):
    '''
    Calculates the ``zscore`` for data0 and data1. Although it doesn't directly
    uses any external package it relies on ``OLS_SlopeInterceptN`` which uses
    ``pandas`` and ``statsmodels``
    '''
    _mindatas = 2  # ensure at least 2 data feeds are passed
    lines = ('spread', 'spread_mean', 'spread_std', 'zscore',)
    params = (('period', 10),)

    def __init__(self):
        slint = OLS_Slope_InterceptN(*self.datas)

        spread = self.data0 - (slint.slope * self.data1 + slint.intercept)
        self.l.spread = spread

        self.l.spread_mean = bt.ind.SMA(spread, period=self.p.period)
        self.l.spread_std = bt.ind.StdDev(spread, period=self.p.period)
        self.l.zscore = (spread - self.l.spread_mean) / self.l.spread_std


class TradeAnalyzer:

    def __init__(self, analyzer_list):
        self.summary_dict = dict(analyzer_list.get_analysis().lvalues()[0])
        self.win_loss_dict = dict(analyzer_list.get_analysis().lvalues()[1])
        self.win_trades = dict(analyzer_list.get_analysis().lvalues()[3])
        self.loss_trades = dict(analyzer_list.get_analysis().lvalues()[4])


    def get_summary(self):
        return self.summary_dict

    def get_streak(self):
        x = [{i:dict(self.win_loss_dict[i])} for i in self.win_loss_dict]
        return x[0],x[1]

    def get_wins(self):
        win_trades_info = dict(self.win_trades['pnl'])
        win_trades_info['number'] = self.win_trades['total']
        win_trades_info['type'] = 'wins'

        return win_trades_info

    def get_losses(self):
        loss_trades_info = dict(self.loss_trades['pnl'])
        loss_trades_info['number'] = self.loss_trades['total']
        loss_trades_info['type'] = 'losses'
        return loss_trades_info



