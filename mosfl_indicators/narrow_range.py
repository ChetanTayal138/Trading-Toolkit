import os
import pandas as pd
import numpy as np
import datetime
import argparse

def get_equities(PATH, equities, daily=True):
    curr_df = pd.read_csv(PATH)    
    curr_df = curr_df[curr_df['SYMBOL'].isin(equities)]
    if daily:
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

def get_week_dates(months):
    week_dates = []
    for month in months :
        files = [x for x in os.listdir("./data/input/weekly_nse_200/") if f"{month}" in x]        
        dates = sorted([int(f[0:2]) for f in files])
        for d in dates:
            if d < 10:
                d = f"0{d}"
            week_dates.append(f"{d}-{month}")
    return week_dates


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--exists', type=str, help='Pass as false if running for the first time.')
    parser.add_argument('--type', type=str, default='daily', help='Pass "weekly" to calculate indicators on weekly data')
    args = parser.parse_args()

    
    MONTHS = ["JAN","FEB","MAR", "APR", "MAY"]
    NSE_200 = pd.read_csv("./data/input/bhavcopies/ind_nifty200list.csv")    
    NSE_200_SYMBOLS = list(NSE_200['Symbol'])

    DAILY_PATH = "./data/input/bhavcopies"
    WEEKLY_PATH = "./data/input/weekly_nse_200"



    if args.type == 'weekly':
        PATH = WEEKLY_PATH
        dates = get_week_dates(MONTHS)
    else:
        PATH = DAILY_PATH
        dates = get_month_dates(MONTHS)


    if args.exists != 'false':
        dates = dates[-3:]
    

    print("Checking for dates")
    print(dates)
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


        if args.type == 'weekly':
            third_df = get_equities(f"./data/input/weekly_nse_200/{third_day_date}-{third_day_month}-2021.csv", list(NSE_200_SYMBOLS), daily=False)
            second_df = get_equities(f"./data/input/weekly_nse_200/{second_day_date}-{second_day_month}-2021.csv", list(NSE_200_SYMBOLS), daily=False)
            first_df = get_equities(f"./data/input/weekly_nse_200/{first_day_date}-{first_day_month}-2021.csv", list(NSE_200_SYMBOLS), daily=False)


        else:
            third_df = get_equities(f"./data/input/bhavcopies/cm{third_day_date}{third_day_month}2021bhav.csv", list(NSE_200_SYMBOLS))
            second_df = get_equities(f"./data/input/bhavcopies/cm{second_day_date}{second_day_month}2021bhav.csv", list(NSE_200_SYMBOLS))
            first_df = get_equities(f"./data/input/bhavcopies/cm{first_day_date}{first_day_month}2021bhav.csv", list(NSE_200_SYMBOLS))


        for symbol in NSE_200_SYMBOLS:
            third_high = third_df[third_df['SYMBOL']==symbol].HIGH.values
            second_high = second_df[second_df['SYMBOL']==symbol].HIGH.values
            first_high = first_df[first_df['SYMBOL']==symbol].HIGH.values

            third_low = third_df[third_df['SYMBOL']==symbol].LOW.values
            second_low = second_df[second_df['SYMBOL']==symbol].LOW.values
            first_low = first_df[first_df['SYMBOL']==symbol].LOW.values

            if third_high < second_high and second_high < first_high and third_low > second_low and second_low > first_low:
                print(f"{symbol} {third_day_date}-{third_day_month}-2021 {third_high[0]} {third_low[0]}")
