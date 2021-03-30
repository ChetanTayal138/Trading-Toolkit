import numpy as np
from statsmodels import regression
from alphabeta_regression import normal_equation
import statsmodels.stats.diagnostic as smd
import scipy.stats as stats
import matplotlib.pyplot as plt
import math
from utils import read_df, filter_df, pct_change

def calculate_residuals(predictions,observed):
    return observed - predictions

if __name__ == "__main__":
    
    

    n = 50 
    X = np.linspace(0,n,n)
    Y_autocorrelated = np.zeros(n)
    Y_autocorrelated[0] = 50

    for i in range(1,n):
        Y_autocorrelated[i] = Y_autocorrelated[i-1] + np.random.normal(0,1)

    X = X.reshape(-1,1)
    Y_autocorrelated_diff = np.diff(Y_autocorrelated).reshape(-1,1)
    Y_autocorrelated = Y_autocorrelated.reshape(-1,1)
    
     
    
    alpha, beta = normal_equation(X,  Y_autocorrelated)
    alpha_diff, beta_diff = normal_equation(X[1:, :], Y_autocorrelated_diff)

    predictions = alpha[0] + (beta[0] * X)
    predictions_diff = alpha_diff[0] + (beta_diff[0] * X[1:, :])

    residuals = calculate_residuals(predictions, Y_autocorrelated)

    
    residuals_diff = calculate_residuals(predictions_diff, Y_autocorrelated_diff)

    
    plt.scatter(predictions_diff, residuals_diff)
    

    plt.axhline(0, color='red')
    plt.xlabel('Predicted Values')
    plt.ylabel('Residual Values')
    
    plt.show()



    
    ljung_box = smd.acorr_ljungbox(residuals_diff, lags = 10)
    print("Lagrange Multiplier Statistics:", ljung_box[0])
    print("\nP-values:", ljung_box[1], "\n")

    if any(ljung_box[1] < 0.05):
        print("The residuals are autocorrelated.")
    else:
        print("The residuals are not autocorrelated.")



















    
