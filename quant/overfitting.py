import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats
from utils import pct_change, read_df, filter_df
from alphabeta_regression import normal_equation

def calculate_r_squared(predictions, actual):
    unexplained_variance = np.sum(np.square(actual - predictions))
    average_actual_value = np.mean(actual)
    total_variance = np.sum(np.square(actual - average_actual_value))
    r_squared = 1 - (unexplained_variance / total_variance)

    return r_squared


if __name__ == "__main__":

    x1 = read_df("../data/nse/MARUTI.NS.csv").dropna()
    x2 = read_df("../data/nse/TATASTEEL.NS.csv").dropna()
    x3 = read_df("../data/nse/JUBLFOOD.NS.csv").dropna()
    x4 = read_df("../data/nse/MINDTREE.NS.csv").dropna()
    y =  read_df("../data/nse/HEROMOTOCO.NS.csv").dropna()

    #We expect highest correlation between Heromotocorp and maruti since they belong in the same sector. Here we try to model the price of Hero Motocorp by regressing it first against only Maruti and then regressig it against all other stocks
    
    START_DATE = "2019-01-01"
    END_DATE = "2020-01-01"
    
    x1 = filter_df(START_DATE, END_DATE, x1)['Close'].values.reshape(-1,1)
    x2 = filter_df(START_DATE, END_DATE, x2)['Close'].values.reshape(-1,1)
    x3 = filter_df(START_DATE, END_DATE, x3)['Close'].values.reshape(-1,1)
    x4 = filter_df(START_DATE, END_DATE, x4)['Close'].values.reshape(-1,1)
    y = filter_df(START_DATE, END_DATE, y)['Close'].values.reshape(-1,1)
    
    m_x = np.hstack((x1,x2,x3,x4))
    
    # Single Linear Regression

    alpha, beta = normal_equation(x1, y)
    
    slr_predictions = alpha + beta * x1

    r_squared = calculate_r_squared(slr_predictions, y)
    print("Single Linear Regression R squared - " + str(r_squared)) 
    m_alpha, beta1, beta2, beta3, beta4 = normal_equation(m_x, y)

    mlr_predictions = m_alpha + beta1 * x1 + beta2 * x2 + beta3 * x3 + beta4 * x4

    r_squared = calculate_r_squared(mlr_predictions, y)
    print("Multiple Linear Regression R squared - " + str(r_squared))

    

    plt.plot(y, color='black')
    plt.plot(slr_predictions, color='blue')
    plt.plot(mlr_predictions, color='red')
    plt.show()

    

    ## MAKING FUTURE PREDICTIONS

    x1 = read_df("../data/nse/MARUTI.NS.csv").dropna()
    x2 = read_df("../data/nse/TATASTEEL.NS.csv").dropna()
    x3 = read_df("../data/nse/JUBLFOOD.NS.csv").dropna()
    x4 = read_df("../data/nse/MINDTREE.NS.csv").dropna()
    y =  read_df("../data/nse/HEROMOTOCO.NS.csv").dropna()

    
    START_DATE = "2020-01-01"
    END_DATE = "2021-01-01"
    
    x1 = filter_df(START_DATE, END_DATE, x1)['Close'].values.reshape(-1,1)
    x2 = filter_df(START_DATE, END_DATE, x2)['Close'].values.reshape(-1,1)
    x3 = filter_df(START_DATE, END_DATE, x3)['Close'].values.reshape(-1,1)
    x4 = filter_df(START_DATE, END_DATE, x4)['Close'].values.reshape(-1,1)
    y = filter_df(START_DATE, END_DATE, y)['Close'].values.reshape(-1,1)


    slr_predictions = alpha + beta * x1
    mlr_predictions = m_alpha + beta1 * x1 + beta1 * x2 + beta3 * x3 + beta4 * x4


    r_squared = calculate_r_squared(slr_predictions, y)
    print("New Single Linear Regression R squared - " + str(r_squared))
    

    r_squared = calculate_r_squared(mlr_predictions, y)
    print("New Multiple Linear Regression R squared - " + str(r_squared))


    plt.plot(y, color='black')
    plt.plot(slr_predictions, color='blue')
    plt.plot(mlr_predictions, color='red')
    plt.show()


