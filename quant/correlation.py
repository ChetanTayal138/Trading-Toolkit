import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats
from statsmodels.stats.stattools import jarque_bera
from utils import read_df, filter_df, pct_change




if __name__ == "__main__":

    benchmark = read_df("../data/nse/nifty.csv")
    a1 = read_df("../data/nse/INFY.NS.csv")
    a2 = read_df("../data/nse/TATACONSUM.NS.csv")
    a3 = read_df("../data/nse/MARUTI.NS.csv")
    
    START_DATE = "2019-01-01"
    END_DATE = "2021-01-01"
    
    t1 = filter_df(START_DATE, END_DATE, a1)
    t2 = filter_df(START_DATE, END_DATE, a2)
    t3 = filter_df(START_DATE, END_DATE, a3)
    b1 = filter_df(START_DATE, END_DATE, benchmark)

    p1 = t1['Close'].values
    p1 = p1[~np.isnan(p1)]

    p2 = t2['Close'].values
    p2 = p2[~np.isnan(p2)]


    p3 = t3['Close'].values
    p3 = p3[~np.isnan(p3)]
    
    nifty = b1['Close'].values
    nifty = nifty[~np.isnan(nifty)]
    
    print("Correlation Coefficients")
    print("INFOSYS and TATA Consumer : ", np.corrcoef(p1,p2)[0,1])
    print("TATA Consumer and Maruti : ", np.corrcoef(p2,p3)[0,1])
    print("Maruti and Infosys : ", np.corrcoef(p3, p1)[0,1])

    rolling_correlation = pd.Series(p1).rolling(60).corr(pd.Series(nifty))
    plt.title("Rolling Correlation of Nifty and Infosys")
    plt.plot(rolling_correlation)
    plt.xlabel('Day')
    plt.ylabel('60-day Rolling Correlation')
    plt.show()
        
    plt.scatter(p1,nifty)
    plt.xlabel('INFOSYS')
    plt.ylabel('Nifty')
    plt.title('Stock prices from ' + START_DATE + ' to ' + END_DATE)
    plt.show()


