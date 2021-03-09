import pandas as pd
import numpy as np
from utils import *


def compute_rsi_one(average_gain, average_loss, lookback_period=14):

    rsi_term = average_gain / average_loss
    return 100 - (100 / (1+rsi_term))

def compute_rsi_two(prev_average_gain, prev_average_loss, current_average_gain, current_average_loss, lookback_period=14):
    rsi_term  = (prev_average_gain * (lookback_period-1) + current_average_gain) / (prev_average_loss * (lookback_period-1) + current_average_loss) 
    return 100 - (100 / (1+rsi_term))


def calculate_gain_loss(close_values, lookback_period=14):

    print(len(close_values))
    j = 0
    gains = []
    losses = []
    for i in range(lookback_period):

        if i >= 1:
            prev_value = close_values[i-1]
            curr_value = close_values[i]
            print(f"Current value is {curr_value}")

            #change = curr_value/prev_value #positive ratio indicates a gain, negative ratio indicates a loss from the previous day
            if curr_value - prev_value >= 0:
                gains.append((curr_value - prev_value)/prev_value )
            else:
                losses.append((prev_value - curr_value)/prev_value)

        else:
            print(f"Starting value is {close_values[i]}")

    ag = np.array(gains).mean()
    al = np.array(losses).mean()
    print(f"AVERAGE GAIN = {ag}")
    print(f"AVERAGE LOSS = {al}")
    
    return ag, al

if __name__ == "__main__":

    df = read_df("./tsla.csv")
    START_DATE = "2020-01-01"
    END_DATE = "2021-01-01"

    temp = filter_df(START_DATE, END_DATE, df)
    close_values = temp['Close'].values
    rsi_values = []
    gain_averages = []
    loss_averages = []
    
    
    
    ag, al = calculate_gain_loss(close_values[0:14])
    rsi_values.append(compute_rsi_one(ag, al))
    gain_averages.append(ag)
    loss_averages.append(al)
    
    for j in range(1, len(close_values)-13):

        try:
            new_ag, new_al = calculate_gain_loss(close_values[j:j+14])
            rsi_values.append(compute_rsi_two(gain_averages[-1], loss_averages[-1], new_ag, new_al))
            gain_averages.append(new_ag)
            loss_averages.append(new_al)            

        except: 
            print("Encountered non divisible scenario")


    #print(len(rsi_values))
    #print(min(rsi_values))
    #print(max(rsi_values))
    #plt.plot(rsi_values)

    fig, axs = plt.subplots(2)
    axs[0].title.set_text("Closing price values")
    axs[0].plot(close_values[:-13])
    
    axs[1].title.set_text("RSI indicator")
    axs[1].plot(rsi_values, "r")
    axs[1].axhline(30, c="black")
    axs[1].axhline(70, c="black")
    plt.show()












