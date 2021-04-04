import pandas as pd
import scipy.stats as stats
import numpy as np

def rank_correlation(df_1, df_2):
    s1 = df_1['Date']
    s2 = df_2['Date']
    common_dates = pd.Series(np.intersect1d(s1.values,s2.values))

    x = df_1[df_1['Date'].isin(common_dates)]['InterMonth Change']
    y = df_2[df_2['Date'].isin(common_dates)]['InterMonth Change']

    plt.scatter(x, y)
    spearman(x, y)


def year_vs_month_intermonth(dataframe):

    data = {}
    YEARS = [i for i in range(2010, 2022)]
    MONTHS = {1:"JAN", 2:"FEB", 3:"MAR", 4:"APR", 5:"MAY", 6:"JUN", 7:"JUL", 8:"AUG", 9:"SEP", 10:"OCT", 11:"NOV", 12:"DEC"}

    for m in MONTHS:
        data[MONTHS[m]] = []


    for y in YEARS:
        mask = dataframe['Date'].map(lambda x: x.year) == y
        df = dataframe[mask]

        df['Month'] = df['Date'].map(lambda x: MONTHS[x.month]) 
        df = df[['Date', 'IntraMonth Diff', 'InterMonth Change', 'Month']]

        for m in MONTHS:
            if MONTHS[m] not in list(df['Month']):

                append_data = {'Date':f'{y}-{m}-01','InterMonth Change':None, 'IntraMonth Diff':None, 'Month':MONTHS[m]}        
                df = df.append(append_data, ignore_index=True)

        df['Date'] = pd.to_datetime(df['Date'], format="%Y-%m-%d")
        df = df.sort_values('Date', ascending=True)
        df = df[['Month', 'InterMonth Change', 'Date']].values

        curr = []
        for i in df:    
            data[i[0]].append(i[1])

    df_data = []
    for k in data:
        df_data.append(data[k])

    df = pd.DataFrame(df_data, columns=YEARS, index=[MONTHS[i] for i in MONTHS])
    print(df)

def generate_bar_data(df, view=False):
    intra_month = []
    inter_month = []
    for i in range(1,13):
        mask = df['Date'].map(lambda x: x.month) == i
        if view:
            print(df[mask])
        intra_month.append(df[mask]['IntraMonth Diff'].mean())
        inter_month.append(df[mask]['InterMonth Change'].mean())
        
    return intra_month, inter_month    


def convert_to_datetime(df):
    df['Date'] = pd.to_datetime(df['Date'], format="%Y-%m-%d")
    return df

def convert_column_to_datetime(df):
    dates = df['Date']
    temp_dates = []
    for d in dates:
        d = d.split(" ")
        curr = ['1']
        curr.append(d[0])
        curr.append(d[1])
        temp_dates.append("-".join(curr))

    df['Date'] = temp_dates

    return df

def sorter(df, frequency, column, asc=False):
    return df.groupby(pd.Grouper(key='Date',freq=frequency)).mean().sort_values(column, ascending=asc)

def spearman(x,y,cutoff=0.05):
    corr_coeff, p_value = stats.spearmanr(x,y)
    print('Correlation Coefficient: ' + str(corr_coeff))
    if p_value < cutoff:
        print("Significant relation is present")
    else:
        print("Significant relation is not present")
    print('p-value: ' + str(p_value))

    return corr_coeff, p_value
