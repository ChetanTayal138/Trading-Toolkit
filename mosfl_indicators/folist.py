import pandas as pd

df1 = pd.read_csv("./data/input/bhavcopies/ind_nifty50list.csv")
df2 = pd.read_csv("./data/input/bhavcopies/ind_niftymidcap100list.csv")
df3 = pd.read_csv("./data/input/bhavcopies/ind_niftysmallcap100list.csv")

PATH = "./data/input/fo_monthly/"
FO_SYMBOLS_PATH = PATH + "fo_list.csv"

fo_df = pd.read_csv(FO_SYMBOLS_PATH)
fo_symbols = list(fo_df['SYMBOL'])


df1 = list(df1[df1['Symbol'].isin(fo_symbols)]['Symbol'])
df2 = list(df2[df2['Symbol'].isin(fo_symbols)]['Symbol'])
df3 = list(df3[df3['Symbol'].isin(fo_symbols)]['Symbol'])
for i in df3:
	print(i)
exit()
print(df2)
print(df3)

dataframe = pd.DataFrame(columns=['Nifty50', 'NiftyMidCap', 'NiftySmallCap'])

dataframe['Nifty50'] = df1
dataframe['NiftyMidCap'] = df2
dataframe['NiftySmallCap'] = df3
print(dataframe)
