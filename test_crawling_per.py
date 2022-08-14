from Data_Preprocessing.preprocessing_per import total_preprocessing
import pandas as pd
# from pymongo import MongoClient
from database.config import MONGO_URL, MONGO_DB_NAME
# from pathlib import Path

import time
import threading

#함수 정의, 함수 내부에 threading 정의
def printhello(BEST_DIR):

    # print('start crawling ')
    # crawling_38_basic_info(BASE_DIR)
    # # print(1)
    # crawling_38_benefit(BASE_DIR)
    # # print(2)
    # crawling_data(BASE_DIR)
    # # print(3)
    # crawling_38_add(BASE_DIR)


    data1=pd.read_csv(BEST_DIR+'data.csv')
    data2=pd.read_csv(BEST_DIR+'38com_benefit.csv')
    data_added=pd.read_csv(BEST_DIR+'38_add_variable.csv')
    data3=pd.read_csv(BEST_DIR+'title_labelprocessing_Score.csv')
    data4=pd.read_csv(BEST_DIR+'Result_per.csv')



    f = total_preprocessing(data1,data2,data_added,data3,data4)

    print(f.head())
    
    f.to_csv('temp.csv',encoding="CP949")

    print('end crawling',time.time())
    threading.Timer(10,printhello(BEST_DIR)).start() # 100초 



