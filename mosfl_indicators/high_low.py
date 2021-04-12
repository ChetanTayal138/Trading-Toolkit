import os
import pandas as pd
import numpy as np
import datetime
import argparse


def get_equities(PATH, equities):
    curr_df = pd.read_csv(PATH)    
    curr_df = curr_df[curr_df['SYMBOL'].isin(equities)]
    #curr_df = curr_df[curr_df['SERIES']=='EQ']

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

    month_dates = []
    for month in months:
        files = [x for x in os.listdir("../data/bhavcopies/") if f"{month}" in x]
        dates = sorted([int(f[2:4]) for f in files])
        
        for d in dates:
            if d < 10:
                d = f"0{d}"
            month_dates.append(f"{d}-{month}")

    return month_dates

def get_week_dates(months):
    week_dates = []
    for month in months :
        files = [x for x in os.listdir("../data/weekly_nse_200/") if f"{month}" in x]        
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
    
    
    NSE_200 = pd.read_csv("../data/bhavcopies/ind_nifty200list.csv")
    NSE_200_SYMBOLS = list(NSE_200['Symbol'])

    MONTH_DICT = {1:"JAN", 2:"FEB", 3:"MAR", 4:"APR", 5:"MAY", 6:"JUN", 7:"JUL", 8:"AUG", 9:"SEP", 10:"OCT", 11:"NOV", 12:"DEC"}

    DAILY_PATH = "../data/bhavcopies"
    WEEKLY_PATH = "../data/weekly_nse_200"

    today = datetime.datetime.today()
    
    MONTHS = []
    for i in range(1,today.month+1):
        MONTHS.append(MONTH_DICT[i])    

    if args.type == 'weekly':
        PATH = WEEKLY_PATH
        dates = get_week_dates(MONTHS)
        
    else:
        PATH = DAILY_PATH
        dates = get_month_dates(MONTHS)

        
    if args.exists != 'false':
        dates = dates[-2:]
        prev_date = dates[0]
        date_prev,month_prev = prev_date.split('-')
        yesterdays_date = datetime.datetime.strptime(f"{prev_date}-2021", '%d-%b-%Y')
        
        data = pd.read_csv(f"./data/{args.type}/{yesterdays_date}.csv")
        data['SYMBOL'] = data['NAME']
        data = data.set_index('SYMBOL').T.to_dict()
    else:
        if args.type == 'daily':
            starting_df = get_equities(f"{PATH}/cm01{MONTHS[0]}2021bhav.csv", NSE_200_SYMBOLS)
        else:
            starting_df = get_equities(f"{PATH}/{dates[0]}-2021.csv", NSE_200_SYMBOLS)
        starting_df['DATE'] = [datetime.datetime.strptime(x, '%d-%b-%Y') for x in starting_df['TIMESTAMP']]
        starting_df['NAME'] = starting_df['SYMBOL']
        

        starting_df['HH'] = [0 for i in range(len(starting_df))]
        starting_df['HL'] = [0 for i in range(len(starting_df))]
        starting_df['LH'] = [0 for i in range(len(starting_df))]
        starting_df['LL'] = [0 for i in range(len(starting_df))]
        starting_df['HHL'] = [0 for i in range(len(starting_df))]
        starting_df['LHL'] = [0 for i in range(len(starting_df))]
        starting_df = starting_df[['SYMBOL', 'DATE', 'NAME', 'HH', 'HL', 'LH', 'LL', 'HHL', 'LHL', 'CLOSE']]

        data = starting_df.set_index('SYMBOL').T.to_dict()
        
   
    

    for i in range(1,len(dates)):
        curr_date = dates[i]
        prev_date = dates[i-1]

        date_prev,month_prev = prev_date.split('-')
        date_curr,month_curr = curr_date.split('-')

        todays_date = datetime.datetime.strptime(f"{curr_date}-2021", '%d-%b-%Y')       
        yesterdays_date = datetime.datetime.strptime(f"{prev_date}-2021", '%d-%b-%Y')
        
        print("Last date - " + str(yesterdays_date))
        print("Checking for date - " + str(curr_date))
        if args.type == 'daily':    
            prev_df = get_equities(f"../data/bhavcopies/cm{date_prev}{month_prev}2021bhav.csv", list(NSE_200_SYMBOLS))
            curr_df = get_equities(f"../data/bhavcopies/cm{date_curr}{month_curr}2021bhav.csv", list(NSE_200_SYMBOLS))
        else:
            prev_df = get_equities(f"../data/weekly_nse_200/{date_prev}-{month_prev}-2021.csv", list(NSE_200_SYMBOLS))
            curr_df = get_equities(f"../data/weekly_nse_200/{date_curr}-{month_curr}-2021.csv", list(NSE_200_SYMBOLS))


        prev_highs = prev_df.set_index('SYMBOL')['HIGH'].to_dict()
        curr_highs = curr_df.set_index('SYMBOL')['HIGH'].to_dict()
        
        prev_lows = prev_df.set_index('SYMBOL')['LOW'].to_dict()
        curr_lows = curr_df.set_index('SYMBOL')['LOW'].to_dict()
        
        
        for symbol in curr_highs:
            
            
            
            try:

                data[symbol]['CLOSE'] = curr_df[curr_df['SYMBOL']==symbol]['CLOSE'].values[0]
                if curr_highs[symbol] > prev_highs[symbol] and curr_lows[symbol] > prev_lows[symbol]:
                    if(data[symbol]["HHL"] != 0):
                        data[symbol]["HHL"] = data[symbol]["HHL"] + 1
                        
                    else:
                        data[symbol]["HHL"] = 1

                    data[symbol]['DATE'] = todays_date
                    data[symbol]["LHL"] = 0

                else:

                    data[symbol]["HHL"] = 0                    
                    data[symbol]['DATE'] = todays_date


                if curr_highs[symbol] < prev_highs[symbol] and curr_lows[symbol] < prev_lows[symbol]:

                    
                    if(data[symbol]["LHL"] != 0):
                        data[symbol]["LHL"] = data[symbol]["LHL"] + 1
                    else:
                        data[symbol]["LHL"] = 1

                    data[symbol]['DATE'] = todays_date
                    data[symbol]["HHL"] = 0

                else:

                    data[symbol]["LHL"] = 0                    
                    data[symbol]['DATE'] = todays_date



            
                if curr_highs[symbol] > prev_highs[symbol]:

                    if(data[symbol]["HH"] != 0):
                        data[symbol]['HH'] = data[symbol]['HH'] + 1
                    else:
                        data[symbol]["HH"] = 1
                    
                    
                    data[symbol]['DATE'] = todays_date
                    data[symbol]['LH'] = 0 #Higher High means we reset the count of Lower High
                
                elif curr_highs[symbol] < prev_highs[symbol]:
                    if(data[symbol]["LH"] != 0):
                        data[symbol]["LH"] = data[symbol]["LH"] + 1
                    else:
                        data[symbol]["LH"] = 1
                        
                    data[symbol]['DATE'] = todays_date
                    data[symbol]['HH'] = 0

                
                if curr_lows[symbol] < prev_lows[symbol]:
                    if(data[symbol]["LL"] != 0):
                        data[symbol]["LL"] = data[symbol]["LL"] + 1
                    else:
                        data[symbol]["LL"] = 1
                        
                    data[symbol]['DATE'] = todays_date
                    data[symbol]['HL'] = 0
                

                elif curr_lows[symbol] > prev_lows[symbol]:
                    if(data[symbol]["HL"] != 0):
                        data[symbol]["HL"] = data[symbol]["HL"] + 1

                    else:
                        data[symbol]["HL"] = 1

                    data[symbol]['DATE'] = todays_date
                    data[symbol]['LL'] = 0
            
            except Exception as e:
                
                print(f"SYMBOL -- {symbol} NOT PRESENT IN CURRENT NIFTY 200")
                
        data_df = pd.DataFrame(columns = ['SYMBOL', 'DATE', 'NAME', 'HH', 'HL', 'LH', 'LL', 'HHL', 'LHL', 'CLOSE'])

        for symbol in data:
                data_df = data_df.append(data[symbol], ignore_index = True)

        
        print(data_df[['NAME','HHL','CLOSE']].sort_values(['HHL','CLOSE'],ascending=False).head(10))
        data_df.to_csv(f"data/{args.type}/{todays_date}.csv", index=False)
        
        
