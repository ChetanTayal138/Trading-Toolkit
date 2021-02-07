from utils import *
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression


def read_spaced():
    df = pd.read_csv("./regression_example.csv", sep="\t")
    print(df.head())
    return df


if __name__ == "__main__":

    #df = read_spaced()
    

    
    df_1 = read_df("./tsla.csv")
    df_2 = read_df("./snp.csv")

    START_DATE = "2016-01-01"
    END_DATE = "2021-01-01"
    

    temp_1 = filter_df(START_DATE, END_DATE, df_1)
    temp_2 = filter_df(START_DATE, END_DATE, df_2)

    
    temp_1 = temp_1.groupby(pd.Grouper(key='Date', freq='1W')).nth(0)
    temp_2 = temp_2.groupby(pd.Grouper(key='Date', freq='1W')).nth(0)


    
    pct_1 = temp_1['Close'].pct_change().values[1:].reshape(-1,1)
    pct_2 = temp_2['Close'].pct_change().values[1:].reshape(-1,1)
    """pct_1 = list(df['PortReturn'].values)
    pct_2 = list(df['S&P500Return'].values)
    
    pct_1_vals = []
    pct_2_vals = []

    for i in pct_1:
        i = i.replace('%', '')
        pct_1_vals.append(float(i))

    for i in pct_2:
        i = i.replace('%', '')
        pct_2_vals.append(float(i))
    pct_1 = np.array(pct_1_vals).reshape(-1,1)
    pct_2 = np.array(pct_2_vals).reshape(-1,1)"""

    reg = LinearRegression().fit(pct_2, pct_1)

    print(f"Alpha is {reg.intercept_/100}")
    print(f"Beta is {reg.coef_}")

    plt.scatter(pct_2, pct_1)
    plt.plot(pct_2, reg.predict(pct_2), color='k')
   
    plt.show()
    
