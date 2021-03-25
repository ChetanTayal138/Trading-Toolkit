import pandas as pd
import numpy as np
import datetime

def bhavcopy_downloader():
    MONTHS = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
    year = 2021
    for month in MONTHS[:3]:
        for date in range(1,31):
            BASE_LINK = f"https://www1.nseindia.com/content/historical/EQUITIES/{year}/{month}/cm{date}{month}{year}bhav.csv.zip"
            print(BASE_LINK)

def get_equities(PATH, equities):
    curr_df = pd.read_csv(PATH)    
    curr_df = curr_df[curr_df['SYMBOL'].isin(equities)]
    curr_df = curr_df[curr_df['SERIES']=='EQ']

    return curr_df





if __name__ == "__main__":

   

    NSE_500 = pd.read_csv("../data/bhavcopies/ind_nifty500list.csv")
    NSE_500_SYMBOLS = list(NSE_500['Symbol'])
    dates = [1,2,3,4,5,8,9,10,12,15,16,17,18,19,22,23,24]

    starting_df = get_equities("../data/bhavcopies/cm01MAR2021bhav.csv", NSE_500_SYMBOLS)
    starting_df['DATE'] = [datetime.datetime.strptime(x, '%d-%b-%Y') for x in starting_df['TIMESTAMP']]
    starting_df['NAME'] = [x for x in starting_df['SYMBOL']]
    starting_df['CONSECUTIVE'] = [0 for i in range(len(starting_df))]
    starting_df['TYPE'] = ['None' for i in range(len(starting_df))]

    starting_df = starting_df[['SYMBOL', 'NAME', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'DATE', 'TYPE', 'CONSECUTIVE']]
    
    highs = starting_df.set_index('SYMBOL').T.to_dict()
    lows = starting_df.set_index('SYMBOL').T.to_dict()
    


     
    for i in range(1,len(dates)):
        curr_date = dates[i]
        prev_date = dates[i-1]
        todays_date = datetime.datetime.strptime(f"{curr_date}-MAR-2021", '%d-%b-%Y')       
        yesterdays_date = datetime.datetime.strptime(f"{prev_date}-MAR-2021", '%d-%b-%Y')

        if curr_date < 10:
            curr_date = f"0{curr_date}"
        if prev_date < 10:
            prev_date = f"0{prev_date}"
        
        print("Checking for date - " + str(curr_date))
        
        prev_df = get_equities(f"../data/bhavcopies/cm{prev_date}MAR2021bhav.csv", list(NSE_500_SYMBOLS))
        curr_df = get_equities(f"../data/bhavcopies/cm{curr_date}MAR2021bhav.csv", list(NSE_500_SYMBOLS))

        prev_highs = prev_df.set_index('SYMBOL')['HIGH'].to_dict()
        curr_highs = curr_df.set_index('SYMBOL')['HIGH'].to_dict()
        
        prev_lows = prev_df.set_index('SYMBOL')['LOW'].to_dict()
        curr_lows = curr_df.set_index('SYMBOL')['LOW'].to_dict()
        

        for symbol in curr_highs:
            
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

            
                

        high_df = pd.DataFrame(columns = ['NAME', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'DATE', 'TYPE', 'CONSECUTIVE'])
        low_df = pd.DataFrame(columns = ['NAME', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'DATE', 'TYPE', 'CONSECUTIVE'])

        for symbol in highs:

                high_df = high_df.append(highs[symbol], ignore_index = True)
                low_df = low_df.append(lows[symbol], ignore_index = True)



        high_df.to_csv(f"../data/higher_highs/{todays_date}.csv")
        low_df.to_csv(f"../data/lower_lows/{todays_date}.csv")

        



