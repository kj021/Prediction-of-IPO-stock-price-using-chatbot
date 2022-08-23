
# // ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts.
# // tensorflow-macos 2.6.0 requires numpy~=1.19.2, but you have numpy 1.22.4 which is incompatible.
import numpy as np
from preproessing_second import get_train_data,processing_second
import xgboost
import pickle
import pandas as pd

df = processing_second()

with open('/Users/seop/Documents/GitHub/Prediction-of-IPO-stock-price-using-chatbot/Data_Preprocessing/saved_model.pkl','rb') as f:
    model = pickle.load(f)


for i in range(df.shape[0]):
    if df.loc[i]['cor_name'] == '쏘카':
        x=get_train_data(i)
        break

x['search_amt'] = 0.5
x
x= np.array(x)
print(x)

y =model.predict(x.reshape(1,-1))
print(y)