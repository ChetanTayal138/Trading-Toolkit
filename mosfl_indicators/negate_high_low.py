import os
import pandas as pd
import numpy as np
import datetime
import argparse



    

def get_month_dates(months):

    files = [x.replace(".csv","") for x in os.listdir("./data/output/daily/")]
    return sorted(files)
    

def get_week_dates(months):
    
    files = [x.replace(".csv","") for x in os.listdir("./data/output/weekly/")]
    return sorted(files)
    



def generate_LH_negate(today_HH, yesterday_LH):
    new_HH_entries = today_HH[today_HH['HH'] == 1]    
    old_LH = yesterday_LH[yesterday_LH['NAME'].isin(new_HH_entries['NAME'])]

    return old_LH[old_LH['LH'] >= 4]

def generate_HH_negate(today_LH, yesterday_HH):
    new_LH_entries = today_LH[today_LH['LH'] == 1]
    
    old_HH = yesterday_HH[yesterday_HH['NAME'].isin(new_LH_entries['NAME'])]
    

    return old_HH[old_HH['HH'] >= 4]


def generate_LL_negate(today_HL, yesterday_LL):
    new_HL_entries = today_HL[today_HL['HL'] == 1]
    old_LL = yesterday_LL[yesterday_LL['NAME'].isin(new_HL_entries['NAME'])]
    
    return old_LL[old_LL['LL'] >= 4]


def generate_HL_negate(today_LL, yesterday_HL):
    new_LL_entries = today_LL[today_LL['LL'] == 1]
    old_HL = yesterday_HL[yesterday_HL['NAME'].isin(new_LL_entries['NAME'])]

    return old_HL[old_HL['HL'] >= 4]


def generate_LHL_negate(today_HHL, yesterday_LHL):
    new_HHL_entries = today_HHL[today_HHL['HHL'] == 1]
    old_LHL = yesterday_LHL[yesterday_LHL['NAME'].isin(new_HHL_entries['NAME'])]

    return old_LHL[old_LHL['LHL'] >= 1]


def generate_HHL_negate(today_LHL, yesterday_HHL):
    new_LHL_entries = today_LHL[today_LHL['LHL'] == 1]
    old_HHL = yesterday_HHL[yesterday_HHL['NAME'].isin(new_LHL_entries['NAME'])]

    return old_HHL[old_HHL['HHL'] >= 1]


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--exists', type=str, help='Pass as false if running for the first time.')
    parser.add_argument('--type', type=str, default='daily', help='Pass "weekly" to calculate indicators on weekly data')
    args = parser.parse_args()
        
    
    NSE_200 = pd.read_csv("./data/input/bhavcopies/ind_nifty200list.csv")
    NSE_200_SYMBOLS = list(NSE_200['Symbol'])

    
    MONTH_DICT = {1:"JAN", 2:"FEB", 3:"MAR", 4:"APR", 5:"MAY", 6:"JUN", 7:"JUL", 8:"AUG", 9:"SEP", 10:"OCT", 11:"NOV", 12:"DEC"}

    DAILY_PATH = "./data/input/bhavcopies"
    WEEKLY_PATH = "./data/input/weekly_nse_200"
    
    today = datetime.datetime.today()
    
    
    MONTHS = []
    for i in range(1,today.month+1):
        MONTHS.append(MONTH_DICT[i])    


    if args.type == 'daily':
        dates = get_month_dates(MONTHS)
    else:
        dates = get_week_dates(MONTHS)
    

    
    today_df = pd.read_csv(f"./data/output/{args.type}/{dates[-1]}.csv")
    print("Generating Data For")
    print(dates[-1])
    yesterday_df = pd.read_csv(f"./data/output/{args.type}/{dates[-2]}.csv")
 
    today_HH = today_df.sort_values(['HH','CLOSE'], ascending=False)[['NAME','HH','CLOSE']]
    yesterday_LH = yesterday_df.sort_values(['LH','CLOSE'], ascending=False)[['NAME', 'LH','CLOSE']]
    
    today_LH = today_df.sort_values(['LH','CLOSE'], ascending=False)[['NAME', 'LH','CLOSE']]
    yesterday_HH = yesterday_df.sort_values(['HH','CLOSE'], ascending=False)[['NAME', 'HH','CLOSE']]
    

    today_HL = today_df.sort_values(['HL','CLOSE'], ascending=False)[['NAME', 'HL','CLOSE']]
    yesterday_LL = yesterday_df.sort_values(['LL','CLOSE'], ascending=False)[['NAME', 'LL','CLOSE']]


    today_LL = today_df.sort_values(['LL','CLOSE'], ascending=False)[['NAME', 'LL','CLOSE']]
    yesterday_HL = yesterday_df.sort_values(['HL','CLOSE'], ascending=False)[['NAME', 'HL','CLOSE']]

    today_HHL = today_df.sort_values(['HHL', 'CLOSE'], ascending=False)[['NAME', 'HHL','CLOSE']] 
    yesterday_LHL = yesterday_df.sort_values(['LHL', 'CLOSE'], ascending=False)[['NAME', 'LHL','CLOSE']]

    today_LHL = today_df.sort_values(['LHL', 'CLOSE'], ascending=False)[['NAME', 'LHL','CLOSE']] 
    yesterday_HHL = yesterday_df.sort_values(['HHL', 'CLOSE'], ascending=False)[['NAME', 'HHL','CLOSE']]
    

    LH = generate_LH_negate(today_HH, yesterday_LH).head(10)
    
    HH = generate_HH_negate(today_LH, yesterday_HH).head(10)
    
    LL = generate_LL_negate(today_HL, yesterday_LL).head(10)
    
    HL = generate_HL_negate(today_LL, yesterday_HL).head(10)
    
    LHL = generate_LHL_negate(today_HHL, yesterday_LHL).head(10) 
    
    HHL = generate_HHL_negate(today_LHL, yesterday_HHL).head(10)

    print("Saving Data Type " + str(args.type))
    LH.to_csv(f"./data/output/negate/{args.type}/LH.csv", index=False)
    HH.to_csv(f"./data/output/negate/{args.type}/HH.csv", index=False)
    LL.to_csv(f"./data/output/negate/{args.type}/LL.csv", index=False)
    HL.to_csv(f"./data/output/negate/{args.type}/HL.csv", index=False)
    LHL.to_csv(f"./data/output/negate/{args.type}/LHL.csv", index=False)
    HHL.to_csv(f"./data/output/negate/{args.type}/HHL.csv", index=False)


