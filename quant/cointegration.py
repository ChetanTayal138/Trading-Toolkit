import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats
from statsmodels.tsa.stattools import coint
from utils import read_df, filter_df, pct_change
from alphabeta_regression import normal_equation
from stationarity import stationarity_test


def cointegration_test(X1, X2, cutoff=0.05):
    """Carry out augmented dicky-fuller test on X"""
    #Significant p-value would indicate that we accept the null hypothesis test that the two series are cointegrated
    #Significant meaning the p-value is above our cutoff level
    p_value= coint(X1,X2)[1]
    print("P-value of cointegration test " + str(p_value))

    if(p_value) > cutoff:
        print("Series is unlikely cointegrated")
    else:
        print("Series is likely cointegrated")
    return p_value
if __name__ == "__main__":

    df1 = read_df("../data/nse/Basket/BAJAJ-AUTO.NS.csv")
    df2 = read_df("../data/nse/Basket/MINDTREE.NS.csv")
    
    START_DATE = "2018-01-01"
    END_DATE = "2019-01-01"
    
    temp1 = filter_df(START_DATE, END_DATE, df1)
    temp2 = filter_df(START_DATE, END_DATE, df2)

    actual_price1 = temp1['Close'].values
    actual_price1 = actual_price1[~np.isnan(actual_price1)]

    actual_price2 = temp2['Close'].values
    actual_price2 = actual_price2[~np.isnan(actual_price2)]

    
    print("Stationarity Test for Bajaj Auto Closing Prices")
    stationarity_test(actual_price1)
    print("Stationarity Test for Mindtree Closing Prices")
    stationarity_test(actual_price2)
    
    
    plt.title("Closing prices of BAJAJAUTO and Mindtree over past 5 years")
    plt.plot(actual_price1)
    plt.plot(actual_price2)
    
    plt.show()

    actual_price1 = actual_price1.reshape(-1,1)
    actual_price2 = actual_price2.reshape(-1,1)

    print("Running Linear Regression")

    alpha, beta = normal_equation(actual_price2, actual_price1)
    print(alpha)
    print(beta)
    Z = actual_price2 - beta * actual_price1
    

    plt.plot(Z)
    plt.show()
    print("Checking for stationarity of Z")
    stationarity_test(Z)
    print("Calibrating cointegration test")
    X = np.random.normal(0,1,len(actual_price1))

    cointegration_test(actual_price1, actual_price2)

    #cointegration_test(actual_price2, actual_price1)


















