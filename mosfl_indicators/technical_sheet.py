import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from openpyxl import Workbook
from openpyxl import load_workbook
import yfinance as yf


if __name__ == "__main__":


	DRAGONFLY_LIST = ["Sundaram Finance Limited"]
	DRAGONFLY_PRICE_LIST = []

	BULLHC_LIST = ["Tata Elxsi Limited"]
	BULLHC_PRICE_LIST = []

	BM_LIST = ["Birla Corporation Limited"]

	BM_PRICE_LIST = []


	BEARHC_LIST = ["Angel Broking Limited"]
	BEARHC_PRICE_LIST = []

	ENGULFING_LIST = ["Linde India Limited"]
	ENGULFING_PRICE_LIST = []

	BEARM_LIST = ["Bharat Dynamics Limited"]
	BEARM_PRICE_LIST = []

	HIGH_LIST = sorted(["Birla Corporation Limited", "Adani Transmission Limited", "UPL Limited", "Dalmia Bharat Limited"])
	HIGH_PRICE_LIST = []
	FIFTY_HIGH_LIST = []

	LOW_LIST = sorted(["Godfrey Phillips India Limited", "Sanofi India Limited", "Bata India Limited", "RITES Limited"])
	LOW_PRICE_LIST = []
	FIFTY_LOW_LIST = []

	
	OVERSOLD_LIST = sorted(["Procter & Gamble Health Limited", "CEAT Limited", "Navneet Education Limited"])
	OVERSOLD_PRICE_LIST = []
	
	OVERBOUGHT_LIST = sorted(["NMDC Limited", "NLC India Limited", "Angel Broking Limited"])
	OVERBOUGHT_PRICE_LIST = []



	nifty_df = pd.read_excel("./nifty_all.xlsx")

	oversold_symbols = nifty_df[nifty_df['Company Name'].isin(OVERSOLD_LIST)]['Symbol'].sort_values()
	overbought_symbols = nifty_df[nifty_df['Company Name'].isin(OVERBOUGHT_LIST)]['Symbol'].sort_values()


	
	
	dragonfly_smybols = nifty_df[nifty_df['Company Name'].isin(DRAGONFLY_LIST)]['Symbol']
	bullhc_symbols = nifty_df[nifty_df['Company Name'].isin(BULLHC_LIST)]['Symbol']
	bm_symbols = nifty_df[nifty_df['Company Name'].isin(BM_LIST)]['Symbol']

	bearhc_symbols = nifty_df[nifty_df['Company Name'].isin(BEARHC_LIST)]['Symbol']
	engulfing_symbols = nifty_df[nifty_df['Company Name'].isin(ENGULFING_LIST)]['Symbol']
	bearm_symbols = nifty_df[nifty_df['Company Name'].isin(BEARM_LIST)]['Symbol']

	high_symbols = nifty_df[nifty_df['Company Name'].isin(HIGH_LIST)]['Symbol'].sort_values()
	low_symbols = nifty_df[nifty_df['Company Name'].isin(LOW_LIST)]['Symbol'].sort_values()



	for symbol in oversold_symbols:
		symbol_name = symbol + ".NS"
		print("Fetching : " + symbol_name)
		stock_data = round(yf.download(symbol_name, period="1d", progress=False)['Close'].values[0],2)
		OVERSOLD_PRICE_LIST.append(stock_data)



	for symbol in overbought_symbols:
		symbol_name = symbol + ".NS"
		print("Fetching : " + symbol_name)
		stock_data = round(yf.download(symbol_name, period="1d", progress=False)['Close'].values[0], 2)
		OVERBOUGHT_PRICE_LIST.append(stock_data)

	
	for symbol in dragonfly_smybols:
		symbol_name = symbol + ".NS"
		print("Fetching : " + symbol_name)
		stock_data = round(yf.download(symbol_name, period="1d", progress=False)['Close'].values[0],2)
		DRAGONFLY_PRICE_LIST.append(stock_data)


	for symbol in bullhc_symbols:
		symbol_name = symbol + ".NS"
		print("Fetching : " + symbol_name)
		stock_data = round(yf.download(symbol_name, period="1d", progress=False)['Close'].values[0],2)
		BULLHC_PRICE_LIST.append(stock_data)


	for symbol in bm_symbols:
		symbol_name = symbol + ".NS"
		print("Fetching : " + symbol_name)
		stock_data = round(yf.download(symbol_name, period="1d", progress=False)['Close'].values[0],2)
		BM_PRICE_LIST.append(stock_data)








	for symbol in bearhc_symbols:
		symbol_name = symbol + ".NS"
		print("Fetching : " + symbol_name)
		stock_data = round(yf.download(symbol_name, period="1d", progress=False)['Close'].values[0],2)
		BEARHC_PRICE_LIST.append(stock_data)


	for symbol in engulfing_symbols:
		symbol_name = symbol + ".NS"
		print("Fetching : " + symbol_name)
		stock_data = round(yf.download(symbol_name, period="1d", progress=False)['Close'].values[0],2)
		ENGULFING_PRICE_LIST.append(stock_data)


	for symbol in bearm_symbols:
		symbol_name = symbol + ".NS"
		print("Fetching : " + symbol_name)
		stock_data = round(yf.download(symbol_name, period="1d", progress=False)['Close'].values[0],2)
		BEARM_PRICE_LIST.append(stock_data)




	for symbol in high_symbols:
		symbol_name = symbol + ".NS"
		print("Fetching : " + symbol_name)
		#stock_data = round(yf.download(symbol_name, period="1d", progress=False)['Close'].values[0],2)
		
		stock_info = yf.Ticker(symbol_name).info
		
		stock_data = stock_info['regularMarketPrice']
		fifty_two_week_high = stock_info['fiftyTwoWeekHigh']
		
		HIGH_PRICE_LIST.append(stock_data)
		FIFTY_HIGH_LIST.append(fifty_two_week_high)


	for symbol in low_symbols:
		symbol_name = symbol + ".NS"
		print("Fetching : " + symbol_name)
		#stock_data = round(yf.download(symbol_name, period="1d", progress=False)['Close'].values[0], 2)
		
		stock_info = yf.Ticker(symbol_name).info
		stock_data = stock_info['regularMarketPrice']
		fifty_two_week_low = stock_info['fiftyTwoWeekLow']
		
		LOW_PRICE_LIST.append(stock_data)
		FIFTY_LOW_LIST.append(fifty_two_week_low)

	

	workbook = load_workbook(filename="./Tech Deri Set Up_07-05-21.xlsx")
	sheet = workbook.active
	

	EXCEL_MAPPING = {
    "OVERSOLD_NAME" : "A3:A5",
    "OVERSOLD_PRICE":  "B3:B5",
    "OVERSOLD_RSI" : "C3:C5",

    "OVERBOUGHT_NAME" : "E3:E5",
    "OVERBOUGHT_PRICE":  "F3:F5",
    "OVERBOUGHT_RSI" : "G3:G5",
    
    "DRAGONFLY_NAME" : "A10:A10",
    "DRAGONFLY_PRICE" : "C10:C10",
    
    "BULLHC_NAME" : "A11:A11",
    "BULLHC_PRICE" : "C11:C11",

    "BM_NAME" : "A12:A12",
    "BM_PRICE" : "C12:C12",

    "BEARHC_NAME" : "E10:E10",
    "BEARHC_PRICE" : "G10:G10",

    "ENGULFING_NAME" : "E11:E11",
    "ENGULFING_PRICE" : "G11:G11",

    "BEARM_NAME" : "E12:E12",
    "BEARM_PRICE" : "G12:G12",

    "HIGH_NAME" : "A41:A44",
    "HIGH_PRICE": "B41:B44",
    "FIFTY_HIGH_PRICE" : "C41:C44",

	"LOW_NAME" : "G41:G44",
    "LOW_PRICE": "H41:H44",
    "FIFTY_LOW_PRICE" : "I41:I44",

 
    }

	for index,i in enumerate(sheet[EXCEL_MAPPING["OVERSOLD_NAME"]]):
		print(f"{index} {OVERSOLD_LIST[index]}")
		i[0].value = OVERSOLD_LIST[index]

	for index,i in enumerate(sheet[EXCEL_MAPPING["OVERSOLD_PRICE"]]):
		print(f"{index} {OVERSOLD_PRICE_LIST[index]}")
		i[0].value = OVERSOLD_PRICE_LIST[index]

	
	for index,i in enumerate(sheet[EXCEL_MAPPING["OVERBOUGHT_NAME"]]):
		print(f"{index} {OVERBOUGHT_LIST[index]}")
		i[0].value = OVERBOUGHT_LIST[index]

	for index,i in enumerate(sheet[EXCEL_MAPPING["OVERBOUGHT_PRICE"]]):
		print(f"{index} {OVERBOUGHT_PRICE_LIST[index]}")
		i[0].value = OVERBOUGHT_PRICE_LIST[index]


	for index,i in enumerate(sheet[EXCEL_MAPPING["DRAGONFLY_NAME"]]):
		i[0].value = DRAGONFLY_LIST[index]
	for index,i in enumerate(sheet[EXCEL_MAPPING["DRAGONFLY_PRICE"]]):
		i[0].value = DRAGONFLY_PRICE_LIST[index]

	
	for index,i in enumerate(sheet[EXCEL_MAPPING["BULLHC_NAME"]]):
		i[0].value = BULLHC_LIST[index]

	for index,i in enumerate(sheet[EXCEL_MAPPING["BULLHC_PRICE"]]):
		i[0].value = BULLHC_PRICE_LIST[index]

	try:
	
		for index,i in enumerate(sheet[EXCEL_MAPPING["BM_NAME"]]):
			i[0].value = BM_LIST[index]

		for index,i in enumerate(sheet[EXCEL_MAPPING["BM_PRICE"]]):
			i[0].value = BM_PRICE_LIST[index]

	except Exception as e:

		for index,i in enumerate(sheet[EXCEL_MAPPING["BM_NAME"]]):
			i[0].value = ""

		for index,i in enumerate(sheet[EXCEL_MAPPING["BM_PRICE"]]):
			i[0].value = ""





	try:
		for index,i in enumerate(sheet[EXCEL_MAPPING["BEARHC_NAME"]]):
			i[0].value = BEARHC_LIST[index]
		for index,i in enumerate(sheet[EXCEL_MAPPING["BEARHC_PRICE"]]):
			i[0].value = BEARHC_PRICE_LIST[index]
	except Exception as e:
		for index,i in enumerate(sheet[EXCEL_MAPPING["BEARHC_NAME"]]):
			i[0].value = ""
		for index,i in enumerate(sheet[EXCEL_MAPPING["BEARHC_PRICE"]]):
			i[0].value = ""



	try:
		for index,i in enumerate(sheet[EXCEL_MAPPING["ENGULFING_NAME"]]):
			i[0].value = ENGULFING_LIST[index]

		for index,i in enumerate(sheet[EXCEL_MAPPING["ENGULFING_PRICE"]]):
			i[0].value = ENGULFING_PRICE_LIST[index]

	except Exception as e:
		for index,i in enumerate(sheet[EXCEL_MAPPING["ENGULFING_NAME"]]):
			i[0].value = ""

		for index,i in enumerate(sheet[EXCEL_MAPPING["ENGULFING_PRICE"]]):
			i[0].value = ""

	try:
		for index,i in enumerate(sheet[EXCEL_MAPPING["BEARM_NAME"]]):
			i[0].value = BEARM_LIST[index]

		for index,i in enumerate(sheet[EXCEL_MAPPING["BEARM_PRICE"]]):
			i[0].value = BEARM_PRICE_LIST[index]

	except Exception as e:
		for index,i in enumerate(sheet[EXCEL_MAPPING["BEARM_NAME"]]):
			i[0].value = ""

		for index,i in enumerate(sheet[EXCEL_MAPPING["BEARM_PRICE"]]):
			i[0].value = ""



	for index,i in enumerate(sheet[EXCEL_MAPPING["HIGH_NAME"]]):
		i[0].value = HIGH_LIST[index]
	for index,i in enumerate(sheet[EXCEL_MAPPING["HIGH_PRICE"]]):
		i[0].value = HIGH_PRICE_LIST[index]
	for index,i in enumerate(sheet[EXCEL_MAPPING["FIFTY_HIGH_PRICE"]]):
		i[0].value = FIFTY_HIGH_LIST[index]

	
	for index,i in enumerate(sheet[EXCEL_MAPPING["LOW_NAME"]]):
		i[0].value = LOW_LIST[index]
	for index,i in enumerate(sheet[EXCEL_MAPPING["LOW_PRICE"]]):
		i[0].value = LOW_PRICE_LIST[index]
	for index,i in enumerate(sheet[EXCEL_MAPPING["FIFTY_LOW_PRICE"]]):
		i[0].value = FIFTY_LOW_LIST[index]


	workbook.save(filename=f"./test.xlsx")