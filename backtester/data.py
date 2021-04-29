import numpy as np
import pandas as pd
import yfinance as yf
import datetime
import time
import requests
import io
from sklearn.decomposition import PCA
from sklearn import preprocessing
import os

def download_yahoo_data(start, end, download=True):

    
    NSE_df = pd.read_csv("../data/nse/NSE_1920/ind_nifty500list.csv").dropna()
    NSE_SYMBOLS = list(NSE_df['Symbol'].values)
    
    if download is False:
        return NSE_SYMBOLS

    for i in NSE_SYMBOLS:
        
        print("Fetching " + str(i) + "..." )
     
        try:
            stock = yf.download(f"{i}.NS",start=start, end=end, progress=False)
            stock_info = yf.Ticker(f"{i}.NS").info['sector']
            if len(stock) == 0:
                None
            else:
                stock['Name']=i
                stock['Sector'] = stock_info
                stock.to_csv(f"../data/nse/NSE_1920/{i}.csv")
                
        except Exception:
            None

    return NSE_SYMBOLS

def generate_returns(x):
    curr = x[:-1]
    future = x[1:]
    pcts = (future-curr) / curr 

    pcts = np.insert(pcts, 0, 0)

    return pcts


def read_df(filename, column_names = None):
    if column_names is None :
        df = pd.read_csv(filename, usecols=['Date','Sector'], header=0, parse_dates=['Date'])
    else:
        df = pd.read_csv(filename, usecols=column_names, header=0, parse_dates=['Date'])
    df.dropna(inplace=True)
    return df

def filter_df(START_DATE, END_DATE, df):    
    temp_df = df.loc[(df["Date"] > START_DATE) & (df["Date"] < END_DATE)]
    return temp_df


def apply_PCA(x, components, svd_solver='auto', random_state=0):
    print(x.shape)
    
    pca = PCA(n_components = components, svd_solver = svd_solver ,random_state = random_state)
    pca.fit(x)
    explained_variance = pca.explained_variance_
    X = preprocessing.StandardScaler().fit_transform(pca.components_.T)

    return X, explained_variance







if __name__ == "__main__":
    l = os.listdir("../data/nse/NSE_1920")
    print(len(l))
    
    SYMBOLS = download_yahoo_data(start="2016-01-01", end="2021-04-01", download=False)
    print(SYMBOLS)
    exit()

    from tiingo import TiingoClient

    config = {}

# To reuse the same HTTP Session across API calls (and have better performance), include a session key.
    config['session'] = True

# If you don't have your API key as an environment variable,
# pass it in via a configuration dictionary.
    config['api_key'] = "fd7689ea0019b4292b78d3efd6f7bb9c896083ff"

# Initialize
    client = TiingoClient(config)

    
    df = client.get_dataframe(['AAPL'], frequency='daily', metric_name='adjClose', startDate='2000-01-01', endDate='2019-01-01')
    print(df)
    