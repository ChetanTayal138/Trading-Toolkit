import numpy as np
import pandas as pd
import matplotlib.pyplot as plt




def read_df(filename):
    df = pd.read_csv(filename, usecols=['Date', 'Open', 'High', 'Low', 'Close'], header=0, parse_dates=['Date'])
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



def exponential_moving_average(df, day_range=200, view=False, smoothing_factor=2):
    #Giving more weight to recent prices using smoothing factor = (s/(selected_time_period+1))
    j = 0
    means = {}
    multiplier = (smoothing_factor/(day_range+1))
    

    for i in range(0, len(df)):
        
        temp_df = df.iloc[i:i+day_range, :]
    
        
        
        if(i == 0):
            curr_mean = temp_df['Close'].mean()

        else:
            prev_mean = means[j-1]['Mean']
            close = temp_df.tail()['Close'].values[-1]
            
            curr_mean = (close - prev_mean) * multiplier + prev_mean
            
            #curr_mean = curr_mean * (smoothing_factor / (day_range+1)) +  prev_mean * (1- (smoothing_factor/(day_range+1))) #Giving more weight to current means
            


        means[j] = {"Mean":curr_mean, "First":temp_df.iloc[0,0], "Last":temp_df.iloc[len(temp_df)-1, 0]}

        j = j + 1

    return means



if __name__ == "__main__":

    df = read_df("../data/nse/NSE_1920/JSWSTEEL.csv")
        
    START_DATE = "2015-01-01"
    END_DATE = "2021-01-01"
    DAY_RANGE = 200
     
    temp = filter_df(START_DATE, END_DATE, df)
    
    temp = temp.dropna()
    
    sma = simple_moving_average(temp, day_range=DAY_RANGE)
    
    ema = exponential_moving_average(temp, day_range=DAY_RANGE)

    sma_means = []
    ema_means = []
    
    for k in sma:
        sma_means.append(sma[k]['Mean'])

    for k in ema:
        ema_means.append(ema[k]['Mean'])

    sma_means = np.array(sma_means)
    ema_means = np.array(ema_means)

    temp = temp.iloc[DAY_RANGE:, :]
    ema_means = ema_means[:-DAY_RANGE]
    sma_means = sma_means[:-DAY_RANGE]
    
    temp[f'{DAY_RANGE}-EMA'] = ema_means
    temp[f'{DAY_RANGE}-SMA'] = sma_means

    actual_price = np.array(temp['Close'])[DAY_RANGE:]

    print(temp.head())
    print(temp.tail())
    plt.title(f'Closing (Black) vs {DAY_RANGE}-Day EMA (Red) vs {DAY_RANGE}-Day SMA (Green)')
    plt.plot(sma_means, 'green')
    plt.plot(np.array(temp['Close']), 'black')
    plt.plot(ema_means, 'red')
    plt.show()


