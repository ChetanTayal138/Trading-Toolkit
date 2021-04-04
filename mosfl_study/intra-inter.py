import numpy as np
import pandas as pd
import matplotlib.pyplot as plt




def read_df(filename):
    """Read in csv file"""
    df = pd.read_csv(filename, parse_dates=["Date"])
    return df

def filter_df(START_DATE, END_DATE, df):    
    """Filter dataframe based on start and end dates"""
    temp_df = df.loc[(df["Date"] > START_DATE) & (df["Date"] < END_DATE)]
    return temp_df


def intramonth_difference(df):
    """Calcualtes the difference between the High and Low prices within a month"""
    df['IntraMonth Diff'] = (df['High'] - df['Low']) / df['Open'] * 100
    df['IntraMonth Diff'] = np.around(df['IntraMonth Diff'].astype('float32'), decimals=2)
    return df


def intermonth_difference(df):
    """Calculates the difference between two consecutive monthly closing prices"""
    close_prices = df['Close']
    curr = close_prices[1:]
    nex  = close_prices[:-1]
    
    difference = list((abs(curr.values - nex.values)) / curr.values * 100)
    difference.insert(0,0)
    
    df['InterMonth Change'] = np.around(np.array(difference), decimals=2)

    return df


def create_frequency_chart(title, dataframe, heading, bins='auto', view=False):
    plt.title(title)
    heads = []
    frequency_table = {}
    freq, values, _ = plt.hist(dataframe[heading].values, bins=bins)
    if view:
        plt.show()

    for f in range(len(values)-1):
        heads.append(f'{values[f]}-{values[f+1]}')

    
    for i in range(len(heads)):
       frequency_table[heads[i]] = freq[i]
    
    #Sanity check for sum being 73.
    s = 0
    ranges = []
    vals = []
    pcts = []

    for j in frequency_table:
        ranges.append(j)
        vals.append(frequency_table[j])
        pcts.append( round((frequency_table[j] / len(dataframe)) * 100, 2))
        s = s + frequency_table[j]    
    print(s) 
    table = {'Ranges' : ranges, 'Values' : vals, 'Percentage' : pcts}


    return table

if __name__ == "__main__":

    #TYPE = "Nifty"
    #TYPE = "BankNifty"
    #TYPE = "Gold"
    TYPE = "Vix"
    df = read_df(f"./data/{TYPE}_Monthly.csv")
    df = df.dropna()
    print(df.tail())
    df = df.iloc[len(df) : 0 : -1, :]
    
    
    df['Close'] = df['Close'].map(lambda x: float(str(x).replace(',', '')))
    df['Open'] = df['Open'].map(lambda x: float(str(x).replace(',', '')))
    df['High'] = df['High'].map(lambda x: float(str(x).replace(',', '')))
    df['Low'] = df['Low'].map(lambda x: float(str(x).replace(',', '')))
    
    df['Close'] = df['Close'].astype('float32')
    df['Low'] = df['Low'].astype('float32')
    df['High'] = df['High'].astype('float32')
    df['Open'] = df['Open'].astype('float32')
    
    df = intramonth_difference(df)
    df = intermonth_difference(df)
    df.to_csv(f"./output/IntraInter/{TYPE}_Monthly_IntraInter.csv", index=False)
    print(df.head())
 
    intermonth_table = create_frequency_chart("Intermonth change with suggested bins", df, "InterMonth Change", bins=[0,3,6,9,12,100], view=False)
    intermonth_df = pd.DataFrame.from_dict(intermonth_table)
    
    intramonth_table = create_frequency_chart("Intramonth change with suggested bins", df, "IntraMonth Diff", bins=[0,3,6,9,12,100], view=False)
    intramonth_df = pd.DataFrame.from_dict(intramonth_table)

    intramonth_df.to_csv(f"./output/Percentages/{TYPE}_intramonth_suggested.csv", index=False)
    intermonth_df.to_csv(f"./output/Percentages/{TYPE}_intermonth_suggested.csv", index=False)
    
    #df.index = pd.to_datetime(df['Date'], format="%y-%m-%d")
    
    #print(df.groupby(by=[df.Date.month, df.Date.year])
    #df = df.groupby(pd.Grouper(freq='1M')).max()
    #print(df.head(30))
