import os
import pandas as pd
import numpy as np
import datetime
import argparse


def get_equities(PATH, equities):
    curr_df = pd.read_csv(PATH)    
    curr_df = curr_df[curr_df['SYMBOL'].isin(equities)]
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

    parser = argparse.ArgumentParser()
    parser.add_argument('--exists', type=str, help='Pass as false if running for the first time.')

    args = parser.parse_args()

    MONTH_DICT = {1:"JAN", 2:"FEB", 3:"MAR", 4:"APR", 5:"MAY", 6:"JUN", 7:"JUL", 8:"AUG", 9:"SEP", 10:"OCT", 11:"NOV", 12:"DEC"}
    today = datetime.datetime.today()
    MONTHS = []
    for i in range(1,today.month+1):
        MONTHS.append(MONTH_DICT[i])    
    dates = get_month_dates(MONTHS)
    if args.exists != 'false':
        dates = dates[-2:]
    
    NSE_200 = pd.read_csv("../data/bhavcopies/ind_nifty200list.csv")
    NSE_200_SYMBOLS = list(NSE_200['Symbol'])


    starting_df = get_equities(f"../data/bhavcopies/cm01{MONTHS[0]}2021bhav.csv", NSE_200_SYMBOLS)
    starting_df['DATE'] = [datetime.datetime.strptime(x, '%d-%b-%Y') for x in starting_df['TIMESTAMP']]
    starting_df['NAME'] = starting_df['SYMBOL']
    starting_df['CONSECUTIVE'] = [0 for i in range(len(starting_df))]
    starting_df['TYPE'] = ['None' for i in range(len(starting_df))]

    """starting_df['HH'] = ['None' for i in range(len(starting_df))]
    starting_df['HL'] = ['None' for i in range(len(starting_df))]
    starting_df['LH'] = ['None' for i in range(len(starting_df))]
    starting_df['LL'] = ['None' for i in range(len(starting_df))]

    starting_df['HHL'] = ['None' for i in range(len(starting_df))]
    starting_df['LHL'] = ['None' for i in range(len(starting_df))]"""


    starting_df = starting_df[['SYMBOL', 'NAME', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'DATE', 'TYPE', 'CONSECUTIVE']]
    
    highs = starting_df.set_index('SYMBOL').T.to_dict()
    lows = starting_df.set_index('SYMBOL').T.to_dict()
    higher_high_low = starting_df.set_index('SYMBOL').T.to_dict()
    lower_high_low = starting_df.set_index('SYMBOL').T.to_dict()

    for i in range(1,len(dates)):
        curr_date = dates[i]
        prev_date = dates[i-1]

        date_prev,month_prev = prev_date.split('-')
        date_curr,month_curr = curr_date.split('-')

        todays_date = datetime.datetime.strptime(f"{curr_date}-2021", '%d-%b-%Y')       
        yesterdays_date = datetime.datetime.strptime(f"{prev_date}-2021", '%d-%b-%Y')
        
        print("Checking for date - " + str(curr_date))
        
        prev_df = get_equities(f"../data/bhavcopies/cm{date_prev}{month_prev}2021bhav.csv", list(NSE_200_SYMBOLS))
        curr_df = get_equities(f"../data/bhavcopies/cm{date_curr}{month_curr}2021bhav.csv", list(NSE_200_SYMBOLS))

        prev_highs = prev_df.set_index('SYMBOL')['HIGH'].to_dict()
        curr_highs = curr_df.set_index('SYMBOL')['HIGH'].to_dict()
        
        prev_lows = prev_df.set_index('SYMBOL')['LOW'].to_dict()
        curr_lows = curr_df.set_index('SYMBOL')['LOW'].to_dict()
        

        for symbol in curr_highs:

            try:

                if curr_highs[symbol] > prev_highs[symbol] and curr_lows[symbol] > prev_lows[symbol]:
                    if(higher_high_low[symbol]["TYPE"] == "HHL"):
                        higher_high_low[symbol]['CONSECUTIVE'] = higher_high_low[symbol]['CONSECUTIVE'] + 1
                    else:
                        higher_high_low[symbol]["TYPE"] = "HHL"
                        higher_high_low[symbol]['CONSECUTIVE'] = 1


                    higher_high_low[symbol]['HIGH'] = curr_highs[symbol]
                    higher_high_low[symbol]['LOW'] = curr_lows[symbol]
                    higher_high_low[symbol]['DATE'] = todays_date

                else:

                    higher_high_low[symbol]["TYPE"] = 'None'
                    higher_high_low[symbol]['CONSECUTIVE'] = 0
                    higher_high_low[symbol]['HIGH'] = curr_highs[symbol]
                    higher_high_low[symbol]['LOW'] = curr_lows[symbol]
                    higher_high_low[symbol]['DATE'] = todays_date


                if curr_highs[symbol] < prev_highs[symbol] and curr_lows[symbol] < prev_lows[symbol]:

                    if(lower_high_low[symbol]["TYPE"] == "LHL"):
                        lower_high_low[symbol]['CONSECUTIVE'] = lower_high_low[symbol]['CONSECUTIVE'] + 1
                    else:
                        lower_high_low[symbol]["TYPE"] = "LHL"
                        lower_high_low[symbol]['CONSECUTIVE'] = 1


                    
                    lower_high_low[symbol]['HIGH'] = curr_highs[symbol]
                    lower_high_low[symbol]['LOW'] = curr_lows[symbol]
                    lower_high_low[symbol]['DATE'] = todays_date

                    lower_high_low[symbol]['HIGH'] = curr_highs[symbol]
                    lower_high_low[symbol]['LOW'] = curr_lows[symbol]
                    lower_high_low[symbol]['DATE'] = todays_date

                else:
                    
                    lower_high_low[symbol]["TYPE"] = 'None'
                    lower_high_low[symbol]['CONSECUTIVE'] = 0

            
                if curr_highs[symbol] > prev_highs[symbol]:

                    if(highs[symbol]["TYPE"] == "HH"):
                        highs[symbol]['CONSECUTIVE'] = highs[symbol]['CONSECUTIVE'] + 1
                    else:
                        highs[symbol]["TYPE"] = "HH"
                        highs[symbol]['CONSECUTIVE'] = 1
                    
                    highs[symbol]['HIGH'] = curr_highs[symbol]
                    highs[symbol]['DATE'] = todays_date
                
                elif curr_highs[symbol] < prev_highs[symbol]:
                    if(highs[symbol]["TYPE"] == "LH"):
                        highs[symbol]['CONSECUTIVE'] = highs[symbol]['CONSECUTIVE'] + 1

                    else:
                        highs[symbol]["TYPE"] = "LH"
                        highs[symbol]['CONSECUTIVE'] = 1

                    highs[symbol]['HIGH'] = curr_highs[symbol]
                    highs[symbol]['DATE'] = todays_date

                
                if curr_lows[symbol] < prev_lows[symbol]:
                    if(lows[symbol]["TYPE"] == "LL"):
                        lows[symbol]['CONSECUTIVE'] = lows[symbol]['CONSECUTIVE'] + 1
                    else:
                        lows[symbol]["TYPE"] = "LL"
                        lows[symbol]['CONSECUTIVE'] = 1
                    
                    lows[symbol]['LOW'] = curr_lows[symbol]
                    lows[symbol]['DATE'] = todays_date
                

                elif curr_lows[symbol] > prev_lows[symbol]:
                    if(lows[symbol]["TYPE"] == "HL"):
                        lows[symbol]['CONSECUTIVE'] = lows[symbol]['CONSECUTIVE'] + 1

                    else:
                        lows[symbol]["TYPE"] = "HL"
                        lows[symbol]['CONSECUTIVE'] = 1

                    lows[symbol]['LOW'] = curr_lows[symbol]
                    lows[symbol]['DATE'] = todays_date
            
            except:
                
                print(f"SYMBOL -- {symbol} NOT PRESENT IN CURRENT NIFTY 200")
                

        high_df = pd.DataFrame(columns = ['NAME', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'DATE', 'TYPE', 'CONSECUTIVE'])
        low_df = pd.DataFrame(columns = ['NAME', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'DATE', 'TYPE', 'CONSECUTIVE'])
        hhl_df = pd.DataFrame(columns = ['NAME', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'DATE', 'TYPE', 'CONSECUTIVE'])
        lhl_df = pd.DataFrame(columns = ['NAME', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'DATE', 'TYPE', 'CONSECUTIVE'])

        for symbol in highs:

                high_df = high_df.append(highs[symbol], ignore_index = True)
                low_df = low_df.append(lows[symbol], ignore_index = True)
                hhl_df = hhl_df.append(higher_high_low[symbol], ignore_index = True)
                lhl_df = lhl_df.append(lower_high_low[symbol], ignore_index = True)


        print(high_df)
        exit()
        high_df.to_csv(f"../data/higher_highs/{todays_date}.csv") #Stores stocks with either higher high or higher low
        low_df.to_csv(f"../data/lower_lows/{todays_date}.csv") #Stores stocks with either lower high or lower low
        hhl_df.to_csv(f"../data/higher_high_lows/{todays_date}.csv") #Stores stocks with both higher high and higher low
        lhl_df.to_csv(f"../data/lower_high_lows/{todays_date}.csv") #Stores stocks with both lower high and lower low
        
