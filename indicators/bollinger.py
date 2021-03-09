from utils import *


def calculate_bands(ma, number_of_deviations, std_deviation):
    bolu = ma + number_of_deviations * std_deviation
    bold = ma - number_of_deviations * std_deviation

    return (bolu,bold)


def bollinger(df, day_range=10,view=False, number_of_deviations=2 ):
    means={}
    boll_upperband = {}
    boll_lowerband = {}
    j = 0
    for i in range(0, len(df)):
        
        temp_df = df.iloc[i:i+day_range, :]
        ma = temp_df['Close'].mean()
        
        curr_std_dev = np.array(temp_df['Close']).std()
        bolu, bold = calculate_bands(ma, number_of_deviations, curr_std_dev)

        means[j] = {"value":ma, "First":temp_df.iloc[0,0], "Last":temp_df.iloc[len(temp_df)-1, 0]}
        boll_upperband[j] = {"value":bolu, "First":temp_df.iloc[0,0], "Last":temp_df.iloc[len(temp_df)-1, 0]}
        boll_lowerband[j] = {"value":bold, "First":temp_df.iloc[0,0], "Last":temp_df.iloc[len(temp_df)-1, 0]}

        j=j+1

    return (means, boll_upperband, boll_lowerband)



if __name__ == "__main__":

    
    df = read_df("./tsla.csv")
    START_DATE = "2019-01-01"
    END_DATE = "2021-01-01"
    

    temp = filter_df(START_DATE, END_DATE, df)
    sma, bolu, bold = bollinger(temp, day_range=20)
    
    sma_values = []
    bolu_values = []
    bold_values = []

    for k in sma:
        sma_values.append(sma[k]['value'])
        bolu_values.append(bolu[k]['value'])
        bold_values.append(bold[k]['value'])
    
    plt.title("Upper Band (Green) and Lower Band (Red)")
    plt.plot(bolu_values, 'g')
    plt.plot(sma_values ,'black')
    plt.plot(bold_values, 'r')

    plt.show()
