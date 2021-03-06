import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats

def read_df(filename):
    df = pd.read_csv(filename, usecols=['Date', 'Open', 'High', 'Low', 'Close'], header=0, parse_dates=['Date'])
    return df

def filter_df(START_DATE, END_DATE, df):    
    temp_df = df.loc[(df["Date"] > START_DATE) & (df["Date"] < END_DATE)]
    return temp_df

def pct_change(values):
    
    curr = values[:-1]
    future = values[1:]
    pcts = (future-curr) / curr 

    return pcts

if __name__ == "__main__":

    df = read_df("data/nifty.csv")
    
    START_DATE = "2015-01-01"
    END_DATE = "2020-01-01"
    
    temp = filter_df(START_DATE, END_DATE, df)
    actual_price = temp['Close'].values





