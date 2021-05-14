import pandas as pd
import numpy as np
import os
import yfinance as yf
import datetime


def download_fo_mothly(symbols, PATH, append=False):
    i = 0

    for symbol in symbols[:1]:

        print("Fetching " + str(i) + "..." )
     
        try:
            stock = yf.download(f"{symbol}.NS",start="2021-05-01", end="2021-05-10", interval="1mo", progress=False)
            stock['Name']= symbol
            stock.reset_index(level=0,inplace=True)
            
            #pd.to_datetime(stock['Date'], format='%Y-%m-%d')
            
            existing_frame = pd.read_csv(PATH + f"{symbol}.csv")
            existing_frame = existing_frame.append(stock, ignore_index=True)
            #stock.to_csv(PATH + f"{symbol}.csv")
            i = i + 1
                
        except Exception as e:
            print(e)
    

    return i




def mark_positive_negative(value):
    if value > 0:
        return 'Positive'
    elif value < 0:
        return 'Negative'


if __name__ == "__main__":


    PATH = "./data/input/fo_monthly/"
    FO_SYMBOLS_PATH = PATH + "fo_list.csv"

    fo_df = pd.read_csv(FO_SYMBOLS_PATH)
    fo_symbols = list(fo_df['SYMBOL'])
    MONTHS = {1:"JAN", 2:"FEB", 3:"MAR", 4:"APR", 5:"MAY", 6:"JUN", 7:"JUL", 8:"AUG", 9:"SEP", 10:"OCT", 11:"NOV", 12:"DEC"}
    #i = download_fo_mothly(fo_symbols, PATH)
    #print(f"Successful download for {i} tickers")
    
    MONTHS_COLS = [MONTHS[i] for i in MONTHS]
    heatmap_dataframe = pd.DataFrame(columns=MONTHS_COLS)
    #heatmap_dataframe = pd.DataFrame(columns=['Symbol', 'May 10 Year Trailing Average'])
    z = 0
    for symbol in fo_symbols:
        print(f"Symbol is {symbol}")
        df = pd.read_csv(PATH + f"{symbol}.csv", usecols=['Date','Close'])        
        
        df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')
        df['Difference'] = df['Close'].diff()
        df['Division'] =  ((df['Close'] / df.Close.shift()) - 1) * 100
        df['Change'] = df['Difference'].apply(mark_positive_negative)

        curr = df.loc[df['Date'].dt.month == 5].iloc[1:11, :]
        print(curr)
        exit()
        
        z = z + 1

        vals = []
        for i in range(1,13):

            try:
                curr_df = df.loc[df['Date'].dt.month == i]
                curr_df = curr_df['Change'].value_counts()

                print(f"Month Number : {i}")
                #print(curr_df)

                available = {'Positive':0, 'Negative':0}
                if len(curr_df) >= 2:
                    available['Positive'] = curr_df['Positive']
                    available['Negative'] = curr_df['Negative']
                    if curr_df['Positive'] >= curr_df['Negative']:
                        
                        #heatmap_dataframe[symbol][MONTHS[i]] = 'Positive'
                        vals.append(f"{available['Positive']} {available['Negative']}")

                    else:
                            
                        #heatmap_dataframe[symbol][MONTHS[i]] = 'Negative'
                        vals.append(f"{available['Positive']} {available['Negative']}")                        
                        #vals.append('Negative')

                else:
                    
                    key = curr_df.keys()[0]
                    available[key] = curr_df[key]
                    vals.append(f"{available['Positive']} {available['Negative']}")

            except Exception as e:
    
                print(f"Error occured in month {MONTHS[i]}")
                vals.append("0 0")

        heatmap_dataframe.loc[symbol] = vals
        
    
    #heatmap_dataframe.to_csv("./someresults.csv")
    print(heatmap_dataframe)