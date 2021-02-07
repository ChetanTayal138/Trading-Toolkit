from utils import *
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

def normal_equation(x, y):
    x = np.hstack((np.ones((x.shape[0], 1), dtype=float), x))    
    A1 = np.linalg.inv(x.T.dot(x))
    A2 = A1.dot(x.T)
    A3 = A2.dot(y)
    return A3


if __name__ == "__main__":

        
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

    alpha, beta = normal_equation(pct_2, pct_1)

    print(f"Alpha is {alpha/100}")
    print(f"Beta is {beta}")

    predictions = alpha + pct_2 * beta

    plt.scatter(pct_2, pct_1)
    plt.plot(pct_2, predictions, color='k')
    plt.xlabel("Benchmark Return")
    plt.ylabel("Security Returns")
   
    plt.show()
    
