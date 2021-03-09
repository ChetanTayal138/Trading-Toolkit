from utils import exponential_moving_average, read_df, filter_df
import matplotlib.pyplot as plt
import numpy as np





if __name__ == "__main__":
    
    
    df = read_df("data/tsla.csv")
    
    START_DATE = "2020-01-01"
    END_DATE = "2021-01-01"

    temp = filter_df(START_DATE, END_DATE, df)
    print(temp.head())    

    ema = exponential_moving_average(temp, day_range=15)
        

    ema_means = []
    
    for k in ema:
        ema_means.append(ema[k]['Mean'])
    
    ema_means = np.array(ema_means)
    temp['Close'] = ema_means
    
    ema_ema = exponential_moving_average(temp, day_range=15)
    ema_ema_means = []
    for k in ema:
        ema_ema_means.append(ema_ema[k]['Mean'])
    
    ema_ema_means = np.array(ema_ema_means)

    dema = 2 * ema_means - ema_ema_means


    #plt.plot(ema_means, 'r')
    #plt.plot(ema_ema_means, 'g')
    plt.title('Actual Price (Black) vs Double Exponential Moving Average (Blue)')
    plt.plot(np.array(temp['Close']), 'black')
    plt.plot(dema, 'blue')
    plt.show()







