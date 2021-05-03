import matplotlib.pyplot as plt
from tqdm import tqdm
from data import download_yahoo_data, generate_returns, read_df, filter_df, apply_PCA
import pandas as pd
import numpy as np
from utils.clustering import apply_DBSCAN, apply_OPTICS, plot_TSNE, plot_cluster
from utils.pairs import PairChecker
import matplotlib.pyplot as plt
import datetime



def generate_returns_dataframe(start, end, download=False):


    SYMBOLS = download_yahoo_data(start, end, download=download) # Will return all symbols of Nifty
    stock_final = pd.DataFrame()
    
    for s in SYMBOLS:

        try:
            print("Reading data for " + s)
            asset_df = filter_df(start, end, read_df(f"../data/nse/NSE_1920/{s}.csv", column_names=['Date', 'Sector', 'Close']))

            if len(asset_df)==1292:


                asset_prices = asset_df['Close'].values
                asset_returns = generate_returns(asset_prices)
                asset_df['Returns'] = asset_returns
                stock_final[s] = asset_df['Returns']
                stock_final['Date'] = asset_df['Date']

        except Exception as e:
            print(e)
            print("Error reading...")

    print(len(stock_final))
    print(stock_final.head())
    stock_final = stock_final.set_index('Date').dropna()
    stock_final.to_csv("./data/stock_final.csv")
    return stock_final

def generate_info_dataframe(stock_final):

    SYMBOLS = stock_final.columns

    symbols_info = {}
    for s in SYMBOLS:

        asset_df = filter_df("2016-01-01", "2021-01 -01", read_df(f"../data/nse/NSE_1920/{s}.csv"))
        symbols_info[s] = asset_df['Sector'].iloc[0]

    
    symbol_info_df = pd.DataFrame(list(symbols_info.items()), columns = ['Symbol', 'Sector'])
    symbol_info_df.to_csv("./data/stock_info.csv")
    return True


def generate_clusterwise_pairs(counts, clustered_series, label_n, start, end):
    all_pairs = []
    total_checks = 0
    total_pairs = 0

    for label_n in range(len(counts)):

        elements_cluster_n = list(clustered_series[clustered_series == label_n].index)
        n = len(elements_cluster_n)
        
        cluster_dataframe = pd.DataFrame()
        print("Cluster " + str(label_n))
        possible_pairs_in_cluster = (n * (n-1)) / 2
        total_pairs = total_pairs + possible_pairs_in_cluster

        for el in elements_cluster_n:
            #print(f"Name : {el} Sector : {stock_info_dict[el]}")
            asset_df = filter_df(start, end, read_df(f"../data/nse/NSE_1920/{el}.csv", column_names=['Close','Date']))
            cluster_dataframe[el] = asset_df['Close']


        PC = PairChecker(elements_cluster_n, cluster_dataframe)
        current_pairs, num_checks = PC.check_cointegration()
        total_checks = total_checks + num_checks

        for pair in current_pairs:

            all_pairs.append(pair)

    return all_pairs, total_pairs


def generate_sectorwise_pairs(sectorwise_clusters, start, end):
    all_pairs = []
    total_checks = 0
    total_pairs = 0

    for sector in tqdm(sectorwise_clusters):

        elements_cluster_n = sectorwise_clusters[sector]
        n = len(elements_cluster_n)
        
        cluster_dataframe = pd.DataFrame()
        print("Cluster " + str(sector))
        possible_pairs_in_cluster = (n * (n-1)) / 2
        total_pairs = total_pairs + possible_pairs_in_cluster

        for el in elements_cluster_n:
            #print(f"Name : {el} Sector : {stock_info_dict[el]}")
            asset_df = filter_df(start, end, read_df(f"../data/nse/NSE_1920/{el}.csv", column_names=['Close','Date']))
            cluster_dataframe[el] = asset_df['Close']


        PC = PairChecker(elements_cluster_n, cluster_dataframe)
        current_pairs, num_checks = PC.check_cointegration()
        total_checks = total_checks + num_checks

        for pair in current_pairs:
            all_pairs.append(pair)

    return all_pairs, total_pairs

    


if __name__ == "__main__":

    #START = datetime.datetime(2016,1,1)
    #END = datetime.datetime(2021,4,1)
    #stock_final = generate_returns_dataframe(START, END, download=False)
    #generate_info_dataframe(stock_final)
    
    NSE_500_SYMBOLS = list(pd.read_csv("../data/nse/NSE_1920/ind_nifty500list.csv")['Symbol'].values)
    
    stock_final = pd.read_csv("./data/stock_final.csv", index_col = 'Date')
    stock_final_columns = list(stock_final.columns)

    INTERSECTING_NSE_500 = [x for x in NSE_500_SYMBOLS if x in stock_final_columns]


    stock_final = stock_final[INTERSECTING_NSE_500]
    print(len(stock_final.columns))
    
    
    stock_info = pd.read_csv("./data/stock_info.csv", usecols=['Symbol', 'Sector'])
    stock_info = stock_info[stock_info['Symbol'].isin(INTERSECTING_NSE_500)]
    
    stock_info_dict = dict(stock_info.values)



    sectors = stock_info['Sector'].unique()
    sectorwise_clusters = {}

    for s in sectors:
        s_cluster = list(stock_info[stock_info['Sector'] == s]['Symbol'].values)
        sectorwise_clusters[s] = s_cluster
        print(f"Number of assets in {s} are {len(s_cluster)}")

    
    n = len(stock_final.columns)
    total_pairs = (n * (n-1))/2
    print("Total Number of Tickers")
    print(n)
    print("Total Number of Possible Pairs")
    print(total_pairs)


    X, explained_variance = apply_PCA(stock_final, 2)
    

    
    clustered_series_all, clustered_series, counts, clf = apply_OPTICS(X, stock_final, min_samples=3,cluster_method='xi')
    #clustered_series_all, clustered_series, counts, clf = apply_DBSCAN(0.15, 4, X, stock_final)

    plot_TSNE(X,clf, clustered_series_all)

    for label_n in range(len(counts)):

        elements_cluster_n = list(clustered_series[clustered_series == label_n].index)
        n = len(elements_cluster_n)
        
        print("Cluster " + str(label_n))

        for el in elements_cluster_n:
            print(f"Name : {el} Sector : {stock_info_dict[el]}")
    
  
    

    all_pairs, total_pairs = generate_sectorwise_pairs(sectorwise_clusters, "2019-01-01", "2020-01-01")
    
    df = pd.DataFrame(all_pairs, columns = ['Asset 1', 'Asset 2'])
    df.to_csv("./data/sectorwise_pairs.csv", index=False)
    print(f"Total Number of Pairs Found are - {len(all_pairs)}")
    print(f"Total Possible Pairs - {total_pairs}" )

    
    all_pairs, total_pairs = generate_clusterwise_pairs(counts, clustered_series, label_n, "2019-01-01", "2020-01-01")

    df = pd.DataFrame(all_pairs, columns = ['Asset 1', 'Asset 2'])
    df.to_csv("./data/clusterwise_pairs.csv", index=False)
    print(f"Total Number of Pairs Found are - {len(all_pairs)}")
    print(f"Total Possible Pairs - {total_pairs}" )
