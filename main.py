import sys
sys.path.append("./indicators")

from utils import *

from bollinger import compute_bollinger
from macd import compute_macd
from mfi import compute_mfi, typical_prices
from roc import compute_roc
from rsi import compute_rsi
from stochastic_oscillator import compute_stochastic_oscillator

class IndicatorEngine:

    def __init__(self, filename, start, end):
        self.df = read_df(filename)
        self.START_DATE = start
        self.END_DATE = end
        self.temp = filter_df(start, end, self.df)
        self.high = self.temp['High'].values
        self.low = self.temp['Low'].values
        self.close = self.temp['Close'].values
        self.typical = typical_prices(self.high, self.low, self.close)
        self.volume = self.temp['Volume'].values



        self.bollinger = None
        self.macd = None

    def signalBollinger(self):
        sma_values, bolu_values, bold_values = compute_bollinger(self.temp)
        if (bolu_values[-1] - sma_values[-1]) <= (bold_values[-1] - sma_values[-1]):
            self.bollinger = "BUY"
        else:
            self.bollinger = "SELL"

    def signalMacd(self):
        macd_line, signal_line = compute_macd(self.temp)
        if(signal_line[-1] >= macd_line[-1]):
            self.macd = "BUY"
        else:
            self.macd = "SELL"

    def signalMfi(self):
        mfi_index_values = compute_mfi(self.typical, self.volume)
        if(mfi_index_values[-1] > 70):
            self.mfi = "SELL" #Overbought 
        elif(mfi_index_values[-1] < 30):
            self.mfi = "BUY" #Oversold
        else:
            self.mfi = "NEUTRAL"


    def signalRoc(self):
        roc_values = compute_roc(self.close, 12)
        if(roc_values[-1] > 0):
            self.roc = "BUY"
        else:
            self.roc = "SELL"

    def signalRsi(self):
        rsi_values = compute_rsi(self.close)
        if(rsi_values[-1] > 70):
            self.rsi = "SELL" #Overbought
        elif(rsi_values[-1] < 30):
            self.rsi = "BUY" #Oversold
        else:
            self.rsi = "NEUTRAL"

    def signalStochastic(self):
        k_values = compute_stochastic_oscillator(self.low, self.high, self.close)
        if(k_values[-1] > 80):
            self.stochastic = "SELL" 
        elif(k_values[-1] < 20):
            self.stochastic = "BUY"
        else:
            self.stochastic = "NEUTRAL"


    def generateSignals(self):

        self.signalBollinger()
        self.signalMacd()
        self.signalMfi()
        self.signalRoc()
        self.signalRsi()
        self.signalStochastic()

        return {
        "Bollinger" : self.bollinger, 
        "Macd" : self.macd, 
        "Mfi" : self.mfi,
        "Roc" : self.roc,
        "Rsi": self.rsi,
        "Stochastic Osscilator" : self.stochastic
        }





def main():
    
    START_DATE = "2019-01-01"
    END_DATE = "2021-01-01"
    

    IE = IndicatorEngine("data/tsla.csv", START_DATE, END_DATE)
    print(IE.generateSignals())





if __name__ == "__main__":
    main()
