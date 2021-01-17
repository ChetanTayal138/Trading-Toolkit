import numpy as np
import pandas as pd
import matplotlib.pyplot as plt






def read_df(filename):
    df = pd.read_csv(filename, parse_dates=["Date"])
    return df

def filter_df(START_DATE, END_DATE, df):    
    temp_df = df.loc[(df["Date"] > START_DATE) & (df["Date"] < END_DATE)]
    return temp_df

def simple_moving_average(df, day_range=10, view=False):
    j=0
    means = {}
    for i in range(0,len(df)):
        
        temp_df = df.iloc[i:i+day_range, :]
        if view:
            print(len(temp_df))
            print(f"First day of window ---> {temp_df.iloc[0, 0]}")
            print(f"Last day of window ---> {temp_df.iloc[len(temp_df)-1, 0]}")
        
        means[j] = {"Mean":temp_df['Close'].mean(), "First":temp_df.iloc[0,0], "Last":temp_df.iloc[len(temp_df)-1, 0]}

        j=j+1
        
    return means



def exponential_moving_average(df, day_range=10, view=False, smoothing_factor=2):
    #Giving more weight to recent prices using smoothing factor = (s/(selected_time_period+1))
    j = 0
    means = {}
    print(smoothing_factor/(day_range+1))
    for i in range(0, len(df)):
        
        temp_df = df.iloc[i:i+day_range, :]

        curr_mean = temp_df['Close'].mean()

        if i > 1:
            prev_mean = means[j-1]['Mean']

            curr_mean = curr_mean * (smoothing_factor / (day_range+1)) +  prev_mean * (1- (smoothing_factor/(day_range+1))) #Giving more weight to current means

        means[j] = {"Mean":curr_mean, "First":temp_df.iloc[0,0], "Last":temp_df.iloc[len(temp_df)-1, 0]}

        j = j + 1

    return means

if __name__ == "__main__":

    df = read_df("./tsla.csv")
    START_DATE = "2020-01-01"
    END_DATE = "2021-01-01"

    temp = filter_df(START_DATE, END_DATE, df)
    print(len(temp))
    sma = simple_moving_average(temp, day_range=2)
    print(len(sma))
    ema = exponential_moving_average(temp, day_range=2)
    print(len(ema))

    
    sma_means = []
    ema_means = []
    for k in sma:
        sma_means.append(sma[k]['Mean'])

    for k in ema:
        ema_means.append(ema[k]['Mean'])

    #print(sma_means)
    #print(ema_means)

    sma_means = np.array(sma_means)
    ema_means = np.array(ema_means)
    
    
    actual_price = np.array(temp['Close'])

    print(np.square(actual_price-sma_means).mean(axis=0))
    print(np.square(actual_price-ema_means).mean(axis=0))

    #fig, axs = plt.subplots(2)
    #fig.suptitle('Simple Moving Average vs Exponential Moving Average')
    plt.plot(sma_means, 'r')
    plt.plot(np.array(temp['Close']), 'black')
    plt.plot(ema_means, 'g')
    

    #temp['Close'].plot(x="Open")
    plt.show()


