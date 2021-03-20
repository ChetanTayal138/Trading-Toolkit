import numpy as np
from statsmodels import regression
from alphabeta_regression import normal_equation
import statsmodels.api as sm
import matplotlib.pyplot as plt
import math
from utils import read_df, filter_df, pct_change



if __name__ == "__main__":
    
    
    benchmark = read_df("../data/nse/nifty.csv")
    portfolio = read_df("../data/nse/KOTAKBANK.NS.csv")

    START_DATE = "2018-01-01"
    END_DATE = "2019-01-01"
    
    benchmark= filter_df(START_DATE, END_DATE, benchmark)
    benchmark_prices = benchmark['Close'].values
    benchmark_returns = pct_change(benchmark_prices).reshape(-1,1)


    portfolio = filter_df(START_DATE, END_DATE, portfolio)
    portfolio_prices = portfolio['Close'].values
    portfolio_returns = pct_change(portfolio_prices).reshape(-1,1)

    print(benchmark_returns.shape)
    print(portfolio_returns.shape)

    alpha, beta = normal_equation(benchmark_returns, portfolio_returns)

    """X2 = np.linspace(benchmark_returns.min(), benchmark_returns.max(), 100)

    predictions = alpha + beta * X2

    plt.scatter(benchmark_returns, portfolio_returns)
    plt.plot(X2, predictions, 'r')
    plt.show()"""

    hedged_portfolio = portfolio_returns + beta * benchmark_returns * -1

    print(f"Mean Returns --- Market = {np.mean(benchmark_returns)} -- Normal Portfolio = {np.mean(portfolio_returns)} -- Hedged Portfolio = {np.mean(hedged_portfolio)}")
    print(f"Volatility   --- Market = {np.std(benchmark_returns)} -- Normal Portfolio = {np.std(portfolio_returns)} -- Hedged Portfolio = {np.std(hedged_portfolio)}") 

    new_alpha, new_beta = normal_equation(benchmark_returns, hedged_portfolio)
    print(f"Old Alpha = {alpha} New Alpha = {new_alpha}")
    print(f"Old Beta = {beta} New Beta = {new_beta}")

    plt.plot(benchmark_returns)
    plt.plot(portfolio_returns)
    plt.plot(hedged_portfolio)
    plt.show()
