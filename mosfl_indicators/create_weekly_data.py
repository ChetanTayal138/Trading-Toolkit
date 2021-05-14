import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import datetime

def get_equities(PATH, equities):
    curr_df = pd.read_csv(PATH)    
    curr_df = curr_df[curr_df['SYMBOL'].isin(equities)]
    curr_df = curr_df[curr_df['SERIES']=='EQ']

    return curr_df

def get_month_dates(months):

    month_dates = []
    for month in months:
        files = [x for x in os.listdir("./data/input/bhavcopies/") if f"{month}" in x]
        dates = sorted([int(f[2:4]) for f in files])
        
        for d in dates:
            if d < 10:
                d = f"0{d}"
            month_dates.append(f"{d}-{month}")

    return month_dates

def get_weeks(dates):
    weeks = {}
    for i in range(1,17):
        weeks[i] = []
    print(weeks)
    for date in dates:
        day, month = date.split('-')
        date = datetime.datetime.strptime(f"{date}-2021", '%d-%b-%Y') 
        week_num = date.isocalendar()[1]
        weeks[week_num].append([date,day,month])
    
    return weeks



if __name__ == "__main__":

    MONTHS = ["JAN","FEB","MAR","APR"]

    NSE_200 = pd.read_csv("./data/input/bhavcopies/ind_nifty200list.csv")
    NSE_200_SYMBOLS = list(NSE_200['Symbol'])
    dates = get_month_dates(MONTHS)
    weeks = get_weeks(dates[1:])

    starting_df = get_equities(f"./data/input/bhavcopies/cm01{MONTHS[0]}2021bhav.csv", NSE_200_SYMBOLS)
    starting_df['DATE'] = [datetime.datetime.strptime(x, '%d-%b-%Y') for x in starting_df['TIMESTAMP']]
    starting_df['NAME'] = [x for x in starting_df['SYMBOL']]
    starting_df['CONSECUTIVE'] = [0 for i in range(len(starting_df))]
    starting_df['TYPE'] = ['None' for i in range(len(starting_df))]

    starting_df = starting_df[['SYMBOL', 'NAME', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'DATE', 'TYPE', 'CONSECUTIVE']]

    highs = starting_df.set_index('SYMBOL').T.to_dict()
    lows = starting_df.set_index('SYMBOL').T.to_dict()


    for i in weeks:

        current_week = weeks[i]

        dataframes = []

        for single_day in current_week:
            dataframes.append(get_equities(f"./data/input/bhavcopies/cm{single_day[1]}{single_day[2]}2021bhav.csv", list(NSE_200_SYMBOLS)))

        new_df = pd.concat(dataframes)

        df_data = []
        for symbol in NSE_200_SYMBOLS:
            try:
                symbol_df = new_df[new_df['SYMBOL']==symbol]
                
                weekly_open = symbol_df['OPEN'].values[0]
                weekly_close = symbol_df['CLOSE'].values[-1]
                weekly_high = np.max(symbol_df['HIGH'].values)
                weekly_low = np.min(symbol_df['LOW'].values)
                weekly_date = symbol_df['TIMESTAMP'].values[-1]

                weekly_data = [symbol, weekly_open, weekly_high, weekly_low, weekly_close, weekly_date]

                df_data.append(weekly_data)
            except:
                print(f"{symbol} not present in nifty 200 list")

        df = pd.DataFrame.from_records(df_data, columns=['SYMBOL', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'TIMESTAMP'])
        print("Wrote for week " + str(weekly_date))
        df.to_csv(f"./data/input/weekly_nse_200/{str(weekly_date)[:11]}.csv", index=False)




