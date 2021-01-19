# Introduction

The purpose of this ever-growing repository is to serve as an introduction to basic market indicators that serve as the basis of a multitude of trading decisions. All implementations are done using barebones numpy and pandas and can probably be done using a more efficient vectorized approach (which will also be explored) but for now the goal is to gain an understanding of the working of the indicators. 



## Indicators currently implemented


### SMA & EMA 

Perhaps the most basic indicators to gain an understanding of the underlying security. Each data point's SMA is calculated by taking the N-Period window's mean closing price and marked for the next day. EMA, built on top of SMA aims to give more weight to recent trends of the security and reacts and adapts to sudden changes in the asset's movement.


![Comparison of SMA and EMA for TSLA](https://github.com/ChetanTayal138/Trading-Toolkit/blob/main/images/sma_ema.png)
