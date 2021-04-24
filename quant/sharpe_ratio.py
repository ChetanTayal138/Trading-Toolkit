from utils import *
import matplotlib.pyplot as plt





def sharpe_ratio(asset_returns, riskfree_returns):
    return np.mean(asset_returns - riskfree_returns) / np.std(asset_returns - riskfree_returns)



if __name__ == "__main__":

        
    df_1 = read_df("../data/nasdaq/snp.csv")
    df_2 = read_df("../data/nasdaq/irx.csv")

    START_DATE = "2018-01-01"
    END_DATE = "2021-01-01"

        

    temp_1 = filter_df(START_DATE, END_DATE, df_1).dropna()
    temp_2 = filter_df(START_DATE, END_DATE, df_2).dropna()
    

        
    riskfree_returns = pct_change(temp_1['Close'].values)
    asset_returns = pct_change(temp_2['Close'].values)

    running_sharpe = [sharpe_ratio(asset_returns[i-90:i], riskfree_returns[i-90:i]) for i in range(90, len(asset_returns))]
    mean_rs = np.mean(running_sharpe[:-100])
    std_rs = np.std(running_sharpe[:-100])


    print("Mean Sharpe Ratio : " + str(mean_rs))
    print("Std Dev of Sharpe Ratio : " + str(std_rs))
    _, ax1 = plt.subplots()
    ax1.plot(range(90, len(asset_returns)), running_sharpe);
    ax1.axhline(mean_rs)
    ax1.axhline(mean_rs + std_rs, linestyle='--')
    ax1.axhline(mean_rs - std_rs, linestyle='--')

    ax1.axvline(len(asset_returns)-100, color="red")

    
    plt.xlabel('Date')
    plt.ylabel('Sharpe Ratio')
    plt.show()
    

    # 
