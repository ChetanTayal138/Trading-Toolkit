import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from utils import read_df, filter_df


def simple_moving_average(df, day_range=10, view=False):
    
    sma_means = []
    for i in range(0,len(df)):        

        temp_df = df.iloc[i:i+day_range, :]
        curr_mean = temp_df['Close'].mean()
        sma_means.append(curr_mean)
        
    sma_means = sma_means[:-day_range]
    
    sma_means = np.pad(sma_means, (day_range,0), 'constant')
    
    df[f'{DAY_RANGE}-SMA'] = sma_means
        
    return df


def simple_moving_std(df, day_range=10):

    stds = []
    for i in range(0,len(df)):        

        temp_df = df.iloc[i:i+day_range, :]
        curr_std = temp_df['Close'].std()
        stds.append(curr_std)
        
    stds = stds[:-day_range]
    
    stds = np.pad(stds, (day_range,0), 'constant')
    
    df[f'{DAY_RANGE}-STD'] = stds
        
    return df

def exponential_moving_average(df, day_range=10, view=False, smoothing_factor=2):
    
    ema_means = []
    multiplier = (smoothing_factor/(day_range+1))

    for i in range(0, len(df)):
        
        temp_df = df.iloc[i:i+day_range, :]        
        
        if(i == 0):
            curr_mean = temp_df['Close'].mean()
        else:
            prev_mean = ema_means[i-1]
            close = temp_df.tail()['Close'].values[-1]
            curr_mean = (close - prev_mean) * multiplier + prev_mean
        
        ema_means.append(curr_mean)

    
    ema_means = ema_means[:-day_range]
    
    ema_means = np.pad(ema_means, (day_range,0), 'constant')
    
    df[f'{DAY_RANGE}-EMA'] = ema_means
    
    return df



if __name__ == "__main__":

    df = read_df("../data/nasdaq/tsla.csv")
        
    START_DATE = "2015-01-01"
    END_DATE = "2020-01-01"
    DAY_RANGE = 90
     
    temp = filter_df(START_DATE, END_DATE, df)
    
    temp = temp.dropna()
    
    temp = simple_moving_average(temp, day_range=DAY_RANGE)
    temp = simple_moving_std(temp, day_range=DAY_RANGE)

    mu = temp[f'{DAY_RANGE}-SMA'].values[DAY_RANGE:]
    std = temp[f'{DAY_RANGE}-STD'].values[DAY_RANGE:]
    
    mean_of_rolling_std = np.mean(std)
    std_of_rolling_std = np.std(std)

    mean_of_rolling_mean = np.mean(mu)
    std_of_rolling_mean = np.std(mu)

    xtic = [str(x).split('T')[0] for x in temp['Date'].values]
    x_labels = []
    for i in range(0,len(xtic),100):
        x_labels.append(xtic[i])

    
    plt.plot(mu)
    plt.plot(mu + std, color="green")
    plt.plot(mu - std, color="red")

    plt.axhline(mean_of_rolling_std)
    plt.axhline(mean_of_rolling_std + std_of_rolling_std)
    plt.axhline(mean_of_rolling_std - std_of_rolling_std)
    plt.show()
    

    
    plt.title(f'Closing (Black) vs {DAY_RANGE}-Day EMA (Red) vs {DAY_RANGE}-Day SMA (Green)')
    
    plt.plot(np.array(temp['Close'])[DAY_RANGE:], 'black')
    #plt.plot(temp[f'{DAY_RANGE}-EMA'].values[DAY_RANGE:], 'red')
    plt.plot(temp[f'{DAY_RANGE}-SMA'].values[DAY_RANGE:], 'green')
    plt.axhline(mean_of_rolling_mean)
    plt.axhline(mean_of_rolling_mean + std_of_rolling_mean)
    plt.axhline(mean_of_rolling_mean - std_of_rolling_mean)
    plt.xticks(ticks=range(0,len(temp), 100), labels=x_labels)
    plt.show()


