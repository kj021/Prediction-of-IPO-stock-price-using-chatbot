import numpy as np
import pandas as pd
import pickle
from pathlib import Path
from pymongo import MongoClient


from Crawling.Crawling_38_basic_info import crawling_38_basic_info
from Crawling.Crawling_38_day import crawling_38_day
from Crawling.Crawling_data import crawling_data
from Crawling.preprocessing import preprocessing
from Crawling.Crawling_per import get_per
from Crawling.Crawling_search_amt import main_search_amt
from Crawling.preproessing_second import processing_second

# from Crawling_38_basic_info import crawling_38_basic_info
# from Crawling_38_day import crawling_38_day
# from Crawling_data import crawling_data
# from preprocessing import preprocessing
# from Crawling_per import get_per
# from Crawling_search_amt import main_search_amt
# from preproessing_second import processing_second



client = MongoClient('localhost', 27017)
db = client['Ipo2']
db2 = client['Ipo2_client']


with open('regression/saved_model.pickle','rb') as f:
        model3 = pickle.load(f)   
        
        
def Crawling_total():

    BASE_DIR = Path(__file__).resolve().parent.parent
    
    print("들어감2")

    crawling_38_basic_info(BASE_DIR)

    crawling_38_day(BASE_DIR)

    crawling_data(BASE_DIR)

    preprocessing()
    
    get_per()
    
    

    total_df = pd.read_csv(BASE_DIR/'Crawling/after_prepros.csv')
    result = main_search_amt(total_df)
    result.drop('Unnamed: 0',axis=1,inplace=True)
    result.to_csv(BASE_DIR/'Crawling/final.csv',encoding='utf-8-sig')
    
    df2=processing_second()
    print(df2)

    for i in range(len(df2)):
        if db.inform.find_one({'cor_name': df2.loc[i,'cor_name']}) is None:
            
            print("없음")
            
            x_test=[]
            
            x_test.append(df2.loc[i,'cor_rate'])
            x_test.append(df2.loc[i,'obligation'])
            x_test.append(df2.loc[i,'shares_to_pub'])
            x_test.append(df2.loc[i,'offer_price'])
            x_test.append(df2.loc[i,'offer_label'])
            x_test.append(df2.loc[i,'Quater_per'])
            x_test.append(df2.loc[i,'search_amt'])
            
            x_new=np.array(x_test).reshape(1,-1)
            y_predict = float(model3.predict(x_new))
            y_predict= int(y_predict)
            
            
            info = {
            
            "cor_name" : df2.iloc[i]["cor_name"],
            "cor_rate": float(df2.iloc[i]["cor_rate"]),
            "obligation": float(df2.iloc[i]["obligation"]),
            "offer_price": int(df2.iloc[i]["offer_price"]),
            "market_type": None,
            "sicho_p": int(df2.iloc[i]["sicho_p"]),
            "profit_percent": float(df2.iloc[i]["profit_percent"]),
            "sales": float(df2.iloc[i]["sales"]),
            "profit": float(df2.iloc[i]["profit"]),
            "shares_to_pub": float(df2.iloc[i]["shares_to_pub"]),
            "sub_rate": float(df2.iloc[i]["sub_rate"]),
            "pre_demand_day": df2.iloc[i]["pre_demand_day"],
            "score": None,
            "nasdaq_score": None,
            "Quater_per": float(df2.iloc[i]["Quater_per"]),
            "search_amt": float(df2.iloc[i]["search_amt"]),
            "first_p": str(df2.iloc[i]["first_p"]),
            "offer_label":int(df2.iloc[i]["offer_label"]),
            "Year": int(df2.iloc[i]["Year"]),
            "Month": int(df2.iloc[i]["Month"]),
            "sicho_predict" : int(y_predict)
            }
            
            dpInsert = db.inform.insert_one(info)  # db에 정보 입력
            
        else:
            print("DB에 있음")
    
   
  
