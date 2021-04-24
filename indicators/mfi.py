import pandas as pd
import numpy as np
from utils import *



def typical_prices(high, low, close):
    return (high + low + close)/3

def compute_mfi(typical_values, volume):
    
    mfis = []
    for j in range(0, len(typical_values)-13):

        curr_window = typical_values[j:j+15]
        
        curr_volumes = volume[j:j+15]

        positive_flows = []
        negative_flows = []

        
        for v in range(1,15) :
            try:
                if(curr_window[v] >= curr_window[v-1]):
                    positive_flows.append(curr_window[v] * curr_volumes[v])
                else:
                    negative_flows.append(curr_window[v] * curr_volumes[v])
            except:
                break
        
        positive_flows_sum = sum(positive_flows) #+ (curr_window[0] * curr_volumes[0])
        negative_flows_sum = sum(negative_flows)
        print(positive_flows_sum)
        print(negative_flows_sum)

        mfi_ratio = positive_flows_sum / negative_flows_sum
        mfi_index = 100 - (100/(1+mfi_ratio))
        mfis.append(mfi_index)        


    return mfis

            
        

if __name__ == "__main__":

    df = read_df("../data/tsla.csv")

    START_DATE = "2020-01-01"
    END_DATE = "2021-01-01"

    temp = filter_df(START_DATE, END_DATE, df)
    
    high_values = temp['High'].values
    low_values = temp['Low'].values
    close_values = temp['Close'].values
    volume_values = temp['Volume'].values

    typical_values = typical_prices(high_values, low_values, close_values)
    
    mfi_index_values = compute_mfi(typical_values, volume_values)
    print(mfi_index_values)
        
    fig, axs = plt.subplots(2)
    axs[0].title.set_text("Closing price values")
    axs[0].plot(close_values)
    
    axs[1].title.set_text("Money Flow Index")
    axs[1].plot(mfi_index_values, "r")
    axs[1].axhline(20, c="black")
    axs[1].axhline(80, c="black")

    plt.show()



