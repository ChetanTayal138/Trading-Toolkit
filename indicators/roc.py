import pandas as pd
import numpy as np
from utils import *



def compute_roc(closing_prices,n):
    curr_prices = closing_prices
    prev_prices = np.pad(closing_prices[:len(closing_prices)-n], (n,0), 'constant')
    
    return ((curr_prices[n:] - prev_prices[n:]) / (prev_prices[n:])) * 100


if __name__ == "__main__":

    df = read_df("data/tsla.csv")

    START_DATE = "2020-01-01"
    END_DATE = "2021-01-01"

    temp = filter_df(START_DATE, END_DATE, df)
    close_values = temp['Close'].values
    
    roc_values = compute_roc(close_values, 12)
    
    print(roc_values)
    fig, axs = plt.subplots(2)
    axs[0].title.set_text("Closing price values")
    axs[0].plot(close_values)
    
    axs[1].title.set_text("ROC indicator")
    axs[1].plot(roc_values, "r")
    axs[1].axhline(0, c="black")
    plt.show()



