from pymongo import MongoClient
import certifi
from config import MONGO_URL
import pandas as pd 

DIR = 'C:/Users/KHS/Desktop/대학교/데이터 청년 캠퍼스/깃허브/Prediction-of-IPO-stock-price-using-chatbot'
df = pd.read_csv(DIR+'/raw data/refined_data.csv')
# print(df.info())

client = MongoClient('localhost', 27017)
db = client["Ipo"]
for i in range(len(df)):
    info = {
        "기업명" : df.iloc[i]["기업명"],
        "매출액": float(df.iloc[i]["매출액(백만원)"]),
        "순이익": float(df.iloc[i]["순이익(백만원)"]),
        "구주매출": float(df.iloc[i]["구주매출"]),
        "희망공모가최저": float(df.iloc[i]["희망공모가(최저)"]),
        "희망공모가최고": float(df.iloc[i]["희망공모가(최고)"]),
        "청약경쟁률": float(df.iloc[i]["청약경쟁률(:1)"]),
        "확정공모가": float(df.iloc[i]["확정공모가(원)"]),
        "경쟁률": float(df.iloc[i]["경쟁률(:1)"]),
        "의무보유확약": float(df.iloc[i]["의무보유확약(:1)"]),
        "공모가": int(df.iloc[i]["공모가(원)"]),
        "시초가": int(df.iloc[i]["시초가(원)"]),




    }
    # print(info)
    dpInsert = db.inform.insert_one(info)  # db에 정보 입력

print("finish!")