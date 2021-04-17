import numpy as np
import pandas as pd
import yfinance as yf
import datetime
import time
import requests
import io
from sklearn.decomposition import PCA
from sklearn import preprocessing


def download_yahoo_data(download=True):

    start = datetime.datetime(2016,1,1)
    end = datetime.datetime(2021,4,1)

    NSE_500_df = pd.read_csv("../data/bhavcopies/ind_nifty500list.csv")
    NSE_500_SYMBOLS = list(NSE_500_df[NSE_500_df['Series']=='EQ']['Symbol'].values)
    if download is False:
        return NSE_500_SYMBOLS

    for i in NSE_500_SYMBOLS:  
       
        print(i)
     
        try:
            stock = yf.download(f"{i}.NS",start=start, end=end, progress=False)
            if len(stock) == 0:
                None
            else:
                stock['Name']=i
                stock.to_csv(f"../data/nse/NSE_500/{i}.csv")
                
        except Exception:
            None

    return NSE_500_SYMBOLS

def generate_returns(x):
    curr = x[:-1]
    future = x[1:]
    pcts = (future-curr) / curr 

    pcts = np.insert(pcts, 0, 0)

    return pcts


def read_df(filename):
    df = pd.read_csv(filename, usecols=['Date', 'Open', 'High', 'Low', 'Close'], header=0, parse_dates=['Date'])
    df.dropna(inplace=True)
    return df

def filter_df(START_DATE, END_DATE, df):    
    temp_df = df.loc[(df["Date"] > START_DATE) & (df["Date"] < END_DATE)]
    return temp_df


def apply_PCA(x, components, svd_solver='auto', random_state=0):
    pca = PCA(n_components = components, svd_solver = svd_solver ,random_state = random_state)
    pca.fit(x)

    explained_variance = pca.explained_variance_
    X = preprocessing.StandardScaler().fit_transform(pca.components_.T)

    return X, explained_variance