import pandas as pd
import numpy as np
from utils import *









def compute_oscillation(closing_price_history, current_index, K_values, day_range=14, slow=False):
    print(current_index)
    print(current_index + day_range)
    current_window = closing_price_history[current_index:current_index+day_range-1] * 5
    print(current_window)
    L_day_range = np.min(current_window)
    H_day_range = np.max(current_window)
    print(f"LOW IS {L_day_range}")
    print(f"HIGH IS {H_day_range}")
    
    print(current_window[-1]-L_day_range)
    print(H_day_range - L_day_range)
    
    K = ((current_window[-1] - L_day_range) / (H_day_range - L_day_range )) * 100
    if slow:
        if current_index > 3:
            K = (K_values[current_index-1] + K_values[current_index-2] + K)/3
    #print("K")
    print(K)
    return K


if __name__ == "__main__":
    
    
    df = read_df("./data/tsla.csv")
    START_DATE = "2017-01-01"
    END_DATE = "2017-01-24"

    temp = filter_df(START_DATE, END_DATE, df)
    
    closing_price_history = np.array(temp['Close'])
    
    K_values = []

    j = 0
    for i in range(len(closing_price_history)-13):
        curr_k = compute_oscillation(closing_price_history, i, K_values, slow=True)
        K_values.append(curr_k)


    fig, axs = plt.subplots(2)
    axs[0].plot(closing_price_history)
    axs[1].plot(K_values)
    plt.show()












        
        
















