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

def get_weeks(dates):
    weeks = {}
    for i in range(1,14):
        weeks[i] = []
    
    for date in dates:
        day, month = date.split('-')
        date = datetime.datetime.strptime(f"{date}-2021", '%d-%b-%Y') 
        week_num = date.isocalendar()[1]
        weeks[week_num].append([date,day,month])
    
    return weeks

def get_month_dates(months):

    files = [x.replace(".csv","") for x in os.listdir("./data/daily/")]
    return sorted(files)
    

def get_week_dates(months):
    
    files = [x.replace(".csv","") for x in os.listdir("./data/weekly/")]
    return sorted(files)
    



def generate_LH_negate(today_HH, yesterday_LH):

    new_HH_entries = today_HH[today_HH['HH'] == 1]    
    old_LH = yesterday_LH[yesterday_LH['NAME'].isin(new_HH_entries['NAME'])]

    return old_LH[old_LH['LH'] >= 4]

def generate_HH_negate(today_LH, yesterday_HH):

    new_LH_entries = today_LH[today_LH['LH'] == 1]    
    old_HH = yesterday_HH[yesterday_HH['NAME'].isin(new_LH_entries['NAME'])]

    return old_HH[old_HH['HH'] >= 4]


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--exists', type=str, help='Pass as false if running for the first time.')
    parser.add_argument('--type', type=str, default='daily', help='Pass "weekly" to calculate indicators on weekly data')
    args = parser.parse_args()
        
    
    NSE_200 = pd.read_csv("../data/bhavcopies/ind_nifty200list.csv")
    NSE_200_SYMBOLS = list(NSE_200['Symbol'])

    
    MONTH_DICT = {1:"JAN", 2:"FEB", 3:"MAR", 4:"APR", 5:"MAY", 6:"JUN", 7:"JUL", 8:"AUG", 9:"SEP", 10:"OCT", 11:"NOV", 12:"DEC"}

    DAILY_PATH = "../data/bhavcopies"
    WEEKLY_PATH = "../data/weekly_nse_200"
    
    today = datetime.datetime.today()
    MONTHS = []
    for i in range(1,today.month+1):
        MONTHS.append(MONTH_DICT[i])    


    if args.type == 'daily':
        dates = get_month_dates(MONTHS)
    else:
        dates = get_week_dates(MONTHS)
        
    
    today_df = pd.read_csv(f"./data/{args.type}/{dates[-1]}.csv")
    yesterday_df = pd.read_csv(f"./data/{args.type}/{dates[-2]}.csv")

    
    
    today_HH = today_df.sort_values(['HH','CLOSE'], ascending=False)[['NAME','HH']]
    yesterday_LH = yesterday_df.sort_values(['LH','CLOSE'], ascending=False)[['NAME', 'LH']]
    
    today_LH = today_df.sort_values(['LH','CLOSE'], ascending=False)[['NAME', 'LH']]
    yesterday_HH = yesterday_df.sort_values(['HH','CLOSE'], ascending=False)[['NAME', 'HH']]
    


    print(generate_LH_negate(today_HH, yesterday_LH))
    print(generate_HH_negate(today_LH, yesterday_HH))
    
    
