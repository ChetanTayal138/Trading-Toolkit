from data import download_yahoo_data, generate_returns, read_df, filter_df, apply_PCA
import pandas as pd
import numpy as np
from clustering import apply_DBSCAN, plot_TSNE

if __name__ == "__main__":

	"""SYMBOLS = download_yahoo_data(download=False)
	stock_final = pd.DataFrame()

	
	for s in SYMBOLS:

		try:
			print("Reading data for " + s)
			asset_df = filter_df("2016-01-01", "2021-01	-01", read_df(f"../data/nse/NSE_500/{s}.csv"))
			if len(asset_df)==1231:
				asset_prices = asset_df['Close'].values
				asset_returns = generate_returns(asset_prices)
				asset_df['Returns'] = asset_returns
				stock_final[s] = asset_df['Returns']
				stock_final['Date'] = asset_df['Date']

			

		except Exception as e:
			print(e)
			print("Error reading...")

	stock_final = stock_final.set_index('Date').dropna()
	stock_final.to_csv("./stock_final.csv")"""
	stock_final = pd.read_csv("./stock_final.csv", index_col = 'Date')
	X, explained_variance = apply_PCA(stock_final, 10)
	
	
	clustered_series_all, clustered_series, counts, clf = apply_DBSCAN(0.15, 4, X, stock_final)
	plot_TSNE(X,clf, clustered_series_all)

	
		