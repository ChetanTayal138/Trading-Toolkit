import pandas as pd
from bs4 import BeautifulSoup 
import requests
from difflib import SequenceMatcher

fo_df = pd.read_csv("../fo_mktlots.csv")
underlying = fo_df.iloc[4:]['UNDERLYING                          '].values
for i in range(len(underlying)):
	underlying[i] = underlying[i].rstrip()


results_df = pd.read_csv("../Results.csv")
#print(results_df['Security Name'].values)
#exit()

fo_symbols = list(fo_df.iloc[4:,:]['SYMBOL    '].values)

names = []
lol = []
for f in fo_symbols:
	f = f.split(" ")[0]
	x = results_df[results_df['Security Name'] == f][['Security Name', 'Result Date']]
	if x.size > 0:
		lol.append(x)

print(lol)

#print(names)
#print(len(results_df[results_df['Security Name'].isin(names)]))





"""res = requests.get('https://www.moneycontrol.com/markets/earnings/results-calendar/')
soup = BeautifulSoup(res.content, 'html.parser')
table = soup.find('tbody')
rows = table.find_all('tr')
data_dict = []
for r in rows:
	
	STOCK = r.find('a').text
	DATE = r.find_all('td')[1].text
	data_dict.append({"Name" : STOCK, "Date" : DATE})

for d in data_dict:
	

	stock_name = d['Name']
	print("Checking For " + stock_name)
	ratios = {}
	for k in underlying:
		val = SequenceMatcher(None, stock_name, k).ratio()
		if val > 0.3:
			ratios[k] = val

	print(ratios)"""