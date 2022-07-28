import pandas as pd

data1 = pd.read_csv('/Users/seop/Documents/GitHub/Prediction-of-IPO-stock-price-using-chatbot/Data_Preprocessing/data.csv',encoding='euc-kr')
data = pd.read_csv('/Users/seop/Documents/GitHub/Prediction-of-IPO-stock-price-using-chatbot/Data_Preprocessing/38com_benefit.csv')
data_added = pd.read_csv('/Users/seop/Documents/GitHub/Prediction-of-IPO-stock-price-using-chatbot/Data_Preprocessing/38_add_variable.csv', encoding = 'euc-kr')


from Data_Preprocessing.preprocessing import total_preprocessing
f = total_preprocessing(data1,data,data_added)

