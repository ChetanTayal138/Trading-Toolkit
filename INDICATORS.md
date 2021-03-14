# Indicators Currently Implemented


### SMA & EMA 

Perhaps the most basic indicators to gain an understanding of the underlying security. Each data point's SMA is calculated by taking the N-Period window's mean closing price and marked for the next day. EMA, built on top of SMA aims to give more weight to recent trends of the security and reacts and adapts to sudden changes in the asset's movement.


![Comparison of SMA and EMA for TSLA](https://github.com/ChetanTayal138/Trading-Toolkit/blob/main/images/sma_ema.png)


### DEMA

React quicker to traditional MAs helping traders exit their positions at an earlier stage, allowing them to minimize losses altho susceptible to overtrading. Based on the formula => DEMA = 2 * Ema(n) - Ema(Ema(n)), it utilizes the EMA of an n-period EMA to reduce noise. If the security's actual price is above the DEMA line and the DEMA is on an upward trend, it helps reinforce or confirm an upward trend (and vice versa for downward trend).

![DEMA for TSLA](https://github.com/ChetanTayal138/Trading-Toolkit/blob/main/images/double_exponential_ma.png)


### Bollinger Bands

Bollinger bands aim to model an upper and lower limit on the underlying security's sell value i.e oversold or underbought by plotting trendlines N-standard deviations away from the SMA or EMA of the security. Typically this N is equal to 2 standard deviations which covers almost 95% of variance of the data from the mean (68-95-99.7 rule). If the SMA/EMA moves closer to the Upper Bollinger Band it is considered to be an overbought asset and if the SMA/EMA moves closer to the Lower Bollinger Band it is considered to be an undersold asset. 


![Bollinger bands for TSLA](https://github.com/ChetanTayal138/Trading-Toolkit/blob/main/images/bollinger.png)



### MACD 

MACD stands for Moving Average Convergence Divergence which is a momentum based trend and aims to model the relationship between two moving averages of a security (typically used are 26-period and 12-period SMAs or EMAs). A EMA of M-Period is then calculated over the MACD line to generate a signal line which can be used to signal buying or selling positions for the underlying asset.


![MACD Line for TSLA](https://github.com/ChetanTayal138/Trading-Toolkit/blob/main/images/macd.png)


### RSI 

Relative Strength Index is another momentum based indicator that tries to model the change of an asset's recent price changes and can be used as a good indication wether the asset is overbought (and likely to fall off in the future) or if the asset is undersold (and likely to rise in the near future). The value of the RSI indicator always falls below 0 and 100 where values greater than 70 indicate a time of overbought and values less than 30 indicating a perioid of underselling of the asset.




![RSI for TSLA](https://github.com/ChetanTayal138/Trading-Toolkit/blob/main/images/rsi.png)


### Alpha and Beta

Alpha and Beta are indirectly derived from the Capital Asset Pricing Model (CAPM), a way to determine a security's risk by comparing its volatility against a standard benchmark, typically an index fund like the S&P 500. Alpha and Beta can be easily calculated by employing regression analysis on two variables- Returns of the portfolio (in this case, these are weekly returns of TSLA) and the returns of the standard benchmark( in this case, these are the weekly returns of S&P 500). Using return of portfolio = alpha + beta * return of benchmark, we can obtain the regression parameters. The intercept corresponds to the Alpha and the coefficient corresponds to the Beta of the security.

![AlphaBeta for TSLA](https://github.com/ChetanTayal138/Trading-Toolkit/blob/main/images/alphabeta.png)


### MFI

MFI stands for Money Flow Index is an oscillator based indicator that takes into account the securities volume as well as price. Hence also called volume-weighted RSI and is calculated using the formula MFI = 100 - (100/ 1 + Money Flow Ratio), where the Money Flow Ratio is calculated by taking the ratio between 14 period positive money flow and 14 period negative money flow. Money Flow in this scenario corresponds to the product of Typical Price and Volume of the asset. The value of MFI falls between 0 and 100 and values over 80 indicate an overbought asset and values under 20 indicate an oversold asset.

![MFI for TSLA]((https://github.com/ChetanTayal138/Trading-Toolkit/blob/main/images/mfi.png)



### ROC

Rate of Change is another momentum based oscillator that measures the percentage change in price between the current price and the price n periods ago. It gives a positive value if price changes are trending positively and a negative value if price changes are trending negatively. A rising ROC will be indicative of an uptrend and vice versa.

![MFI for TSLA]((https://github.com/ChetanTayal138/Trading-Toolkit/blob/main/images/roc.png)
