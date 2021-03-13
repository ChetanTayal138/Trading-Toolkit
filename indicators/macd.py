import pandas as pd
import numpy as np
from utils import *


def generate_macd(temp):

    ema_26 = exponential_moving_average(temp, day_range=26)
    
    ema_12 = exponential_moving_average(temp, day_range=12)
    
    # MACD is calculated by subtracting the 26-period EMA from the 12-period EMA
    
    # We then generate a signal line by calculating a 9-period EMA of the MACD
    sma = simple_moving_average(temp, day_range=9)

    ema_26_means = [ema_26[k]['Mean'] for k in ema_26]
    
    ema_12_means = [ema_12[k]['Mean'] for k in ema_12]

    sma_means = [sma[k]['Mean'] for k in sma]

    macd_line = np.array(ema_12_means) - np.array(ema_26_means)

    return macd_line

def compute_macd(temp, signal_period=9, smoothing_factor=2):
    macd = generate_macd(temp)
    j = 0
    signal_values = []
    for i in range(len(macd)):
        curr_values = macd[i:i+signal_period]
        curr_mean = curr_values.mean()
        if i > 1:
            prev_mean = signal_values[j-1]
            curr_mean = curr_mean * (smoothing_factor / (signal_period+1)) + prev_mean * (1-(smoothing_factor/(signal_period+1)))
        signal_values.append(curr_mean)

        j = j+1

    return macd, np.array(signal_values)




if __name__ == "__main__":
    df = read_df("data/tsla.csv")
    START_DATE = "2020-01-01"
    END_DATE = "2021-01-01"

    temp = filter_df(START_DATE, END_DATE, df)
    macd_line, signal_line = compute_macd(temp)
    print(len(macd_line))
    print(len(signal_line))
    
       
    fig, axs = plt.subplots(2)

    """axs[0].title.set_text("26-period ema (red) vs 12-period ema (black)")
    axs[0].plot(np.array(temp['close']), 'black')
    axs[0].plot(np.array(ema_26_means), 'r')
    axs[0].plot(np.array(ema_12_means), 'b')"""
    axs[1].title.set_text("Corresponding MACD line (Red) and Signal Line (Black)")
    axs[1].plot(macd_line, 'r')
    axs[1].bar([i for i in range(253)], macd_line/2)
    axs[1].plot(signal_line, 'black')
    axs[1].hlines(0, 0, 253)
    plt.show()

