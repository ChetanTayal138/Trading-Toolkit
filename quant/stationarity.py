import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats
from statsmodels.tsa.stattools import coint, adfuller
from utils import read_df, filter_df, pct_change


def generate_datapoint(mean, var):
    return np.random.normal(mean, var)

def stationarity_test(X, cutoff=0.05):
    """Carry out augmented dicky-fuller test on X"""
    p_value= adfuller(X)[1]

    if(p_value) < cutoff:
        print("Series is likely stationary")
    else:
        print("Series is unlikely stationary")
    print("Stationarity P_value is " + str(p_value))
    return p_value

if __name__ == "__main__":
    
    

    df = read_df("../data/nse/NSE_1920/KOTAKBANK.csv")
    
    START_DATE = "2015-01-01"
    END_DATE = "2020-01-01"
    
    temp = filter_df(START_DATE, END_DATE, df)
    actual_price = temp['Close'].values
    actual_price = actual_price[~np.isnan(actual_price)]
    actual_returns = pct_change(actual_price)
    
    print(actual_price.shape)
    A = []
    print("Stationarity Test for Closing Prices")
    stationarity_test(actual_price)
    print("Stationarity Test for Returns")
    stationarity_test(actual_returns)
    for i in range(1000):
        A.append(generate_datapoint(0,1))
    
    A_0 = np.array(A)
    A_1 = np.cumsum(A_0)
    A_2 = np.cumsum(A_1)
    print("Stationarity Test for Order 0 series")
    stationarity_test(A_0)
    print("Stationarity Test for Order 1 series")
    stationarity_test(A_1)
    print("Stationarity Test for Order 2 series")
    stationarity_test(A_2)
     
    
    #plt.title("Closing prices of KOTAK over past 5 years")
    #plt.plot(actual_price)
    plt.title("Returns of KOTAK over past 5 years")
    plt.plot(actual_returns)
    plt.show()

    #plt.plot(A_0)
    #plt.show()
    #plt.plot(A_1)
    #plt.show()
    #plt.plot(A_2)
    #plt.show()
