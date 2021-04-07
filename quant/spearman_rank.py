import scipy.stats as stats
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from utils import read_df, filter_df, pct_change



def rankmodel_scores(symbol_list, start, end):

    historical_returns = []
    for symbol in symbol_list:
        df = read_df(os.path.join("../data/nse", symbol))

        START_DATE = start
        END_DATE = end
        
        temp = filter_df(START_DATE, END_DATE, df)
        
        actual_price = temp['Close'].values
        actual_price = actual_price[~np.isnan(actual_price)]
        returns = pct_change(actual_price)
        historical_returns.append(returns)

    scores = np.mean(historical_returns, axis=1) * 100

    return scores

if __name__ == "__main__":
    
    
    START_DATE = "2019-02-01"
    END_DATE = "2019-03-01"
    symbol_list = [x for x in os.listdir("../data/nse") if ".csv" in x]
    print(symbol_list)
    exit()
    
    scores = rankmodel_scores(symbol_list, START_DATE, END_DATE)

    print(scores)
    
    START_DATE = "2019-03-01"
    END_DATE = "2019-04-01"
    
    walk_forward_returns = rankmodel_scores(symbol_list, START_DATE, END_DATE)

    print(walk_forward_returns)

    plt.scatter(scores, walk_forward_returns)
    plt.title("Scores vs Walk Forward Returns")
    plt.xlabel('Scores')
    plt.ylabel('Walk Forward Returns')
    plt.show()

    r_s = stats.spearmanr(scores, walk_forward_returns)
    print('Correlation Coefficient: ' + str(r_s[0]))
    print('p-value: ' + str(r_s[1]))




