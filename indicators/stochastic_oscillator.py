import pandas as pd
import numpy as np
from utils import *









def compute_oscillation(low_values, high_values, close_values, current_index, K_values, day_range=14, slow=False):
    #current_window = closing_price_history[current_index:current_index+day_range-1] * 5
    curr_low = low_values[current_index : current_index + day_range]
    curr_high = high_values[current_index : current_index + day_range]
    curr_close = close_values[current_index : current_index + day_range]

    
    L_day_range = np.min(curr_low)
    H_day_range = np.max(curr_high)
    
    
    K = ((curr_close[-1] - L_day_range) / (H_day_range - L_day_range )) * 100
    if slow:
        if current_index > 3:
            K = (K_values[current_index-1] + K_values[current_index-2] + K)/3
    
    return K

def compute_stochastic_oscillator(low_values, high_values, close_values):

    K_values = []

    j = 0
    for i in range(len(close_values)-13):
        curr_k = compute_oscillation(low_values, high_values, close_values, i, K_values)
        K_values.append(curr_k)

    return K_values


if __name__ == "__main__":
    
    
    df = read_df("./data/tsla.csv")
    START_DATE = "2020-01-01"
    END_DATE = "2021-01-01"

    temp = filter_df(START_DATE, END_DATE, df)

    
    
    low_values = temp['Low'].values
    high_values = temp['High'].values
    close_values = temp['Close'].values

    
    K_values = compute_stochastic_oscillator(low_values, high_values, close_values)
    print(K_values)

    fig, axs = plt.subplots(2)
    axs[0].plot(close_values)
    axs[1].plot(K_values)
    plt.show()












        
        
















