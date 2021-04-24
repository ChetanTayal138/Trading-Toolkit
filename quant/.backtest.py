import pandas as pd
import numpy as np
from utils import *


class BackTester():


    """ticker_data should be an array of values which were actually observed for the particular stock"""
    def __init__(self, ticker_name, ticker_data, portfolio_value):
        
        self.ticker_name = ticker_name
        self.ticker_open = list(np.array(ticker_data['Open']))
        self.ticker_close = list(np.array(ticker_data['Close']))
        self.share_price = self.ticker_close[0]
        self.portfolio_value = portfolio_value if portfolio_value > 0 else 1000
        self.number_of_shares = self.portfolio_value / self.share_price

    def simple_strategy(self):
        """Defines a simple hold strategy"""

        #for day in range(len(self.ticker_open)):
            
        #print(self.ticker_open[day])
        print(f"Initial Portfolio = {self.portfolio_value}")
        final_portfolio = self.number_of_shares * self.ticker_close[-1]
    
        print(f"Final Portfolio = {final_portfolio}")

        print("Profit")
        print(final_portfolio - self.portfolio_value)
        #plt.plot(self.ticker_open)
        #plt.show()






    

if __name__ == "__main__":
    df = read_df("./tsla.csv")
    START_DATE = "2020-01-01"
    END_DATE = "2021-01-01"

    ticker_data = filter_df(START_DATE, END_DATE, df)
    
    print(ticker_data.head())
    print(ticker_data.tail())
    BT = BackTester("TSLA", ticker_data, 10000)
    BT.simple_strategy()
















