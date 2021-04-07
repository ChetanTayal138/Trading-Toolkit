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
    X = np.random.randint(0,100,n)
    e = np.random.normal(0,1,n)
    Y = 10 + 0.5 * X + e
    Y_nonlinear = 10 - (X ** 1.2) + e
    Y_heteroscedastic = 100 + (2 * X)+ (e * X)

    


    X = X.reshape(-1,1)
    Y = Y.reshape(-1,1)
    Y_nonlinear = Y_nonlinear.reshape(-1,1)
 
    Y_heteroscedastic_diff = np.diff(Y_heteroscedastic).reshape(-1,1)
    Y_heteroscedastic_log = np.log(Y_heteroscedastic).reshape(-1,1)
    Y_heteroscedastic_box_cox = stats.boxcox(Y_heteroscedastic)[0].reshape(-1,1)

    Y_heteroscedastic = Y_heteroscedastic.reshape(-1,1)
    
    
    alpha, beta = normal_equation(X,  Y_heteroscedastic)
    alpha_new, beta_new = normal_equation(X[1:, :], Y_heteroscedastic_diff)
    alpha_log, beta_log = normal_equation(X, Y_heteroscedastic_log)
    alpha_box, beta_box = normal_equation(X, Y_heteroscedastic_box_cox)
        
    predictions = alpha[0] + (beta[0] * X)
    predictions_new = (alpha_new + (beta_new * X))[1:,:]
    predictions_log = alpha_log[0] + (beta_log[0] * X)
    predictions_box = alpha_box + (beta_box * X)

    print(predictions_box.shape)
    
    residuals = calculate_residuals(predictions, Y_heteroscedastic)
    
    residuals_new = calculate_residuals(predictions_new, Y_heteroscedastic_diff)
    
    residuals_log = calculate_residuals(predictions_log, Y_heteroscedastic_log)
    residuals_box = calculate_residuals(predictions_box, Y_heteroscedastic_box_cox)
    print(residuals_box.shape)

    #breusch_pagan_p = smd.het_breuschpagan(residuals_new, X[1:])[1]
    """print(breusch_pagan_p)
    if breusch_pagan_p > 0.05:
        print("Relationship is not heteroscedastic")
    elif breusch_pagan_p < 0.05:
        print("Relationship is heteroscedastic")"""

    plt.scatter(predictions, residuals)
    

    plt.axhline(0, color='red')
    plt.xlabel('Predicted Values')
    plt.ylabel('Residual Values')
    
    plt.show()
    #plt.scatter(X,Y_heteroscedastic)
    #plt.plot(X, predictions, 'r')
    
    #plt.show()


    plt.scatter(predictions_box, residuals_box)

    plt.axhline(0, color='red')
    plt.xlabel('Predicted Values')
    plt.ylabel('Residual Values')
    plt.show()
