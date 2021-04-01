import os
import pandas as pd
import numpy as np
import datetime


def get_equities(PATH, equities):
    curr_df = pd.read_csv(PATH)    
    curr_df = curr_df[curr_df['SYMBOL'].isin(equities)]
    curr_df = curr_df[curr_df['SERIES']=='EQ']

    return curr_df


def get_month_dates(months):

    month_dates = []
    for month in months:
        files = [x for x in os.listdir("../data/bhavcopies/") if f"{month}" in x]
        dates = sorted([int(f[2:4]) for f in files])
        
        for d in dates:
            if d < 10:
                d = f"0{d}"
            month_dates.append(f"{d}-{month}")

    return month_dates


if __name__ == "__main__":
    
    MONTHS = ["JAN","FEB","MAR", "APR"]
    NSE_200 = pd.read_csv("../data/bhavcopies/ind_nifty200list.csv")
    NSE_200_SYMBOLS = list(NSE_200['Symbol'])
    dates = get_month_dates(MONTHS)
    
    starting_df = get_equities(f"../data/bhavcopies/cm01{MONTHS[0]}2021bhav.csv", NSE_200_SYMBOLS)
    starting_df['DATE'] = [datetime.datetime.strptime(x, '%d-%b-%Y') for x in starting_df['TIMESTAMP']]
    starting_df['NAME'] = [x for x in starting_df['SYMBOL']]
    starting_df['CONSECUTIVE'] = [0 for i in range(len(starting_df))]
    starting_df['TYPE'] = ['None' for i in range(len(starting_df))]

    starting_df = starting_df[['SYMBOL', 'NAME', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'DATE', 'TYPE', 'CONSECUTIVE']]

    highs = starting_df.set_index('SYMBOL').T.to_dict()
    lows = starting_df.set_index('SYMBOL').T.to_dict()

    for i in range(2,len(dates)):
        third_day = dates[i]
        second_day = dates[i-1]
        first_day = dates[i-2]

        third_day_date, third_day_month = third_day.split('-')
        second_day_date, second_day_month = second_day.split('-')
        first_day_date, first_day_month = first_day.split('-')

        third_date = datetime.datetime.strptime(f"{third_day}-2021", '%d-%b-%Y')
        second_date = datetime.datetime.strptime(f"{second_day}-2021", '%d-%b-%Y')
        first_date = datetime.datetime.strptime(f"{first_day}-2021", '%d-%b-%Y')



        third_df = get_equities(f"../data/bhavcopies/cm{third_day_date}{third_day_month}2021bhav.csv", list(NSE_200_SYMBOLS))
        second_df = get_equities(f"../data/bhavcopies/cm{second_day_date}{second_day_month}2021bhav.csv", list(NSE_200_SYMBOLS))
        first_df = get_equities(f"../data/bhavcopies/cm{first_day_date}{first_day_month}2021bhav.csv", list(NSE_200_SYMBOLS))


        for symbol in NSE_200_SYMBOLS:
            third_high = third_df[third_df['SYMBOL']==symbol].HIGH.values
            second_high = second_df[second_df['SYMBOL']==symbol].HIGH.values
            first_high = first_df[first_df['SYMBOL']==symbol].HIGH.values

            third_low = third_df[third_df['SYMBOL']==symbol].LOW.values
            second_low = second_df[second_df['SYMBOL']==symbol].LOW.values
            first_low = first_df[first_df['SYMBOL']==symbol].LOW.values

            if third_high < second_high and second_high < first_high and third_low > second_low and second_low > first_low:
                print(f"{symbol} {third_day_date}-{third_day_month}-2021 {third_high[0]} {third_low[0]}")
