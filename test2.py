from Data_Preprocessing.preprocessing import total_preprocessing
import pandas as pd
from Crawling.Crawling_38_add import crawling_38_add
from Crawling.Crawling_38_basic_info import crawling_38_basic_info
from Crawling.Crawling_38_benefit import crawling_38_benefit
from Crawling.Crawling_data import crawling_data
from pymongo import MongoClient
from database.config import MONGO_URL, MONGO_DB_NAME
from pathlib import Path

import time
import threading

BASE_DIR = Path(__file__).resolve().parent/'Data_Preprocessing'
#함수 정의, 함수 내부에 threading 정의
def printhello():

    print('start crawling ')
    crawling_38_basic_info(BASE_DIR)
    # print(1)
    crawling_38_benefit(BASE_DIR)
    # print(2)
    crawling_data(BASE_DIR)
    # print(3)
    crawling_38_add(BASE_DIR)


    data1 = pd.read_csv(BASE_DIR/'data.csv')
    data = pd.read_csv(BASE_DIR/'38com_benefit.csv')
    data_added = pd.read_csv(BASE_DIR/'38_add_variable.csv',encoding='cp949')



    f = total_preprocessing(data1,data,data_added)

    print(f.head())
    
    f.to_csv('final_data.csv')

    print('end crawling',time.time())
    threading.Timer(120,printhello).start() # 100초 

printhello()

