from statsmodels.tsa.stattools import coint
import sys
sys.path.append("../quant")
from alphabeta_regression import normal_equation
import numpy as np
import matplotlib.pyplot as plt

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
                        print(hurst_value)
                        if hurst_value < hurst_threshold:
                            halflife_value = self.check_half_life(spread)
                            print(halflife_value)
                            if halflife_value > 1 and halflife_value < 365:
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



