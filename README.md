# Introduction

The purpose of this ever-growing repository is to serve as an introduction to basic market indicators that serve as the basis of a multitude of trading decisions. All implementations are done using barebones numpy and pandas and can probably be done using a more efficient vectorized approach (which will also be explored) but for now the goal is to gain an understanding of the working of the indicators. 



# Indicators currently implemented


### SMA & EMA 

Perhaps the most basic indicators to gain an understanding of the underlying security. Each data point's SMA is calculated by taking the N-Period window's mean closing price and marked for the next day. EMA, built on top of SMA aims to give more weight to recent trends of the security and reacts and adapts to sudden changes in the asset's movement.


![Comparison of SMA and EMA for TSLA](https://github.com/ChetanTayal138/Trading-Toolkit/blob/main/images/sma_ema.png)


### Bollinger Bands

Bollinger bands aim to model an upper and lower limit on the underlying security's sell value i.e oversold or underbought by plotting trendlines N-standard deviations away from the SMA or EMA of the security. Typically this N is equal to 2 standard deviations which covers almost 95% of variance of the data from the mean (68-95-99.7 rule). If the SMA/EMA moves closer to the Upper Bollinger Band it is considered to be an overbought asset and if the SMA/EMA moves closer to the Lower Bollinger Band it is considered to be an undersold asset. 


![Bollinger bands for TSLA](https://github.com/ChetanTayal138/Trading-Toolkit/blob/main/images/bollinger.png)



### MACD 

MACD stands for Moving Average Convergence Divergence which is a momentum based trend and aims to model the relationship between two moving averages of a security (typically used are 26-period and 12-period SMAs or EMAs). A EMA of M-Period is then calculated over the MACD line to generate a signal line which can be used to signal buying or selling positions for the underlying asset.


![MACD Line for TSLA](https://github.com/ChetanTayal138/Trading-Toolkit/blob/main/images/macd.png)


### RSI 

Relative Strength Index is another momentum based indicator that tries to model the change of an asset's recent price changes and can be used as a good indication wether the asset is overbought (and likely to fall off in the future) or if the asset is undersold (and likely to rise in the near future). The value of the RSI indicator always falls below 0 and 100 where values greater than 70 indicate a time of overbought and values less than 30 indicating a perioid of underselling of the asset.




![RSI for TSLA](https://github.com/ChetanTayal138/Trading-Toolkit/blob/main/images/rsi.png)
