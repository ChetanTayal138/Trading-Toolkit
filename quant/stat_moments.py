import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats
from statsmodels.stats.stattools import jarque_bera
from utils import read_df, filter_df


def pct_change(values):
    
    curr = values[:-1]
    future = values[1:]
    pcts = (future-curr) / curr 

    return pcts

def normality_callibration():
    N = 1000
    M = 1000

    pvalues = np.ndarray((N))
    for i in range(N):
        # Draw M samples from a normal distribution
        X = np.random.normal(0, 1, M);
        _, pvalue, _, _ = jarque_bera(X)
        pvalues[i] = pvalue

    # count number of pvalues below our default 0.05 cutoff
    num_significant = len(pvalues[pvalues < 0.05])

    print(float(num_significant) / N)

def normality_test(returns):
    _,p_value,_,_ = jarque_bera(returns)
    if(p_value) > 0.05:
        print("Returns likely follow a normal distribution")
    else:
        print("Returns likely do not follow a normal distribution")
    return

if __name__ == "__main__":

    df = read_df("data/nifty.csv")
    
    START_DATE = "2015-01-01"
    END_DATE = "2020-01-01"
    
    temp = filter_df(START_DATE, END_DATE, df)
    actual_price = temp['Close'].values
    actual_price = actual_price[~np.isnan(actual_price)]
    returns = pct_change(actual_price)

    
    skew = stats.skew(returns)
    mean = np.mean(returns)
    median = np.median(returns)
    kurtosis = stats.kurtosis(returns)

    # Uncomment below line to test wether our null hypothesis function (jarque_bera test) is running correctly. Expect value of around 0.05 or less 
    #normality_callibration()

    normality_test(returns)
    print(f"Skew : {skew}, Mean : {mean}, Median : {median}, Kurtosis : {kurtosis}")

    plt.hist(returns, 30)
    plt.show()


