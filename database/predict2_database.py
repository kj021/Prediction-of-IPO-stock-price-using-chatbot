import numpy as np
import pandas as pd
import pickle
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['Ipo2']

with open('regression/saved_model.pickle','rb') as f:
        model3 = pickle.load(f)
        
            
def get2_data_csv():
        df=pd.read_csv()
        # y_predict = int(model3.predict(x_new))
        # data_pre.append(y_predict)

        # len(data_pre)
        # data_pre[1:17]

        # info={
        #     "기업명" :data_pre[1],
        #     "매출액": float(data_pre[2]), #5
        #     "순이익": float(data_pre[3]), #4
        #     "구주매출": float(data_pre[4]),
        #     "희망공모가최저": float(data_pre[5]),
        #     "희망공모가최고": float(data_pre[6]), #6
        #     "청약경쟁률": float(data_pre[7]), 
        #     "확정공모가": float(data_pre[8]),
        #     "경쟁률": float(data_pre[9]), #3
        #     "의무보유확약": float(data_pre[10]), #2
        #     "공모가": int(data_pre[11]), #1
        #     "시초가": int(data_pre[12]),
        #     "예상시초가":int(data_pre[13]),
        # }

        # dpInsert = db.inform.insert_one(info)
        
        # price_origin=int(data_pre[11])
        # price= int(int(data_pre[11])+int(data_pre[11])*(y_predict/100))
        # y_predict=int(y_predict)
        
        # return price_origin,price,y_predict
        
