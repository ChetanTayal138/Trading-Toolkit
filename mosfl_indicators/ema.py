import pandas as pd
import numpy as np
import yfinance as yf
import sys
sys.path.append("../indicators")
from utils import exponential_moving_average

def download_nifty_500(symbols, PATH):
    i = 0

    for symbol in symbols:
        print("Fetching " + str(i) + "..." )
        try:
            stock = yf.download(f"{symbol}.NS",start="2019-05-12", end="2021-05-12", interval="1d", progress=False)
            stock['Name']= symbol
            stock.to_csv(PATH + f"{symbol}.csv")
            i = i + 1
        except Exception as e:
            print(e)

    return symbols, i

def compare(df):
    if df['Close'] > df['200-EMA']:
        return 'Higher'
    else:
        return 'Lower'




if __name__ == '__main__':

    """NSE_500 = pd.read_csv("./data/input/bhavcopies/ind_nifty500list.csv")
    NSE_500_SYMBOLS = list(NSE_500['Symbol'])
    print(NSE_500_SYMBOLS)
    res_df = pd.DataFrame(columns=['Symbol', 'Close','200-EMA'])

    PATH = "./data/input/nse_500/"
    #symbols, i = download_nifty_500(NSE_500_SYMBOLS, PATH)
    i = 0
    for symbol in NSE_500_SYMBOLS:
        df = pd.read_csv(PATH + f"{symbol}.csv")
        close_price = list(df['Close'])[-1]
        print(f"{i} {symbol} {close_price}")
        
        means = exponential_moving_average(df, day_range=200, smoothing_factor=2.0)
        

        ema_means = []

        for k in means:
            ema_means.append(means[k]['Mean'])

        ema_means = np.array(ema_means)[:-200]
        
        try:
            res_df.loc[i] = [symbol, close_price, ema_means[-1]]
            i = i + 1
        except Exception as e:
            print(f"Error occured with {symbol}")

    print(res_df)
    res_df.to_csv("./ema_outlook.csv", index=True)"""


    df = pd.read_csv("./ema_outlook.csv", usecols=['Symbol', 'Close', '200-EMA'])
    print(df)
    
    
    df['Condition'] = df.apply(compare,axis=1)
    print(df['Condition'].value_counts())

    df.to_csv("./ema_outlook.csv", index=False)


    

    



    