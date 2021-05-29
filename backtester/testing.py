from data import apply_PCA
import pandas as pd
import numpy as np
from utils.clustering import apply_OPTICS
import unittest

class TestPairsFormation(unittest.TestCase):

    def test_Optics(self):
        
        NSE_500_SYMBOLS = list(pd.read_csv("../data/nse/NSE_1920/ind_nifty500list.csv")['Symbol'].values)
        stock_final = pd.read_csv("./data/stock_final.csv", index_col = 'Date')
        stock_final_columns = list(stock_final.columns)
        INTERSECTING_NSE_500 = [x for x in NSE_500_SYMBOLS if x in stock_final_columns]

        stock_final = stock_final[INTERSECTING_NSE_500]
        
        X, explained_variance = apply_PCA(stock_final, 3)
        clustered_series_all, clustered_series, counts, clf = apply_OPTICS(X, stock_final, min_samples=3,cluster_method='xi')
        
        stock_info = pd.read_csv("./data/stock_info.csv", usecols=['Symbol', 'Sector'])
        stock_info = stock_info[stock_info['Symbol'].isin(INTERSECTING_NSE_500)]
        stock_info_dict = dict(stock_info.values)
        count = 0
        j = 0
        for label_n in range(len(counts)):
            j = j + 1

            elements_cluster_n = list(clustered_series[clustered_series == label_n].index)
        
            sector_list = []
            for el in elements_cluster_n:
                if stock_info_dict[el] not in sector_list:
                    sector_list.append(stock_info_dict[el])
            if len(sector_list) > 1:
                count = count + 1
        
        self.assertGreaterEqual(count, j/2)
                    
        


