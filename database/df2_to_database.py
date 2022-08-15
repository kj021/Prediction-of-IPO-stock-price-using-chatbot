from pymongo import MongoClient
import certifi
from config import MONGO_URL
import pandas as pd 

DIR = 'C:/Users/KHS/Desktop/대학교/데이터 청년 캠퍼스/깃허브/Prediction-of-IPO-stock-price-using-chatbot/Crawling/'
df = pd.read_csv(DIR+'after_prepros_all.csv')
df.drop('Unnamed: 0',axis = 1,inplace = True)
df=df.dropna()


client = MongoClient('localhost', 27017)
db = client["Ipo2"]
for i in range(len(df)):
    info = {
        # "기업명" : df.iloc[i]["cor_name"],
        # "기관경쟁률": float(df.iloc[i]["cor_rate"]),
        # "의무보유확약": float(df.iloc[i]["obligation"]),
        # "시장종류": float(df.iloc[i]["market_type"]),
        # "상장일": float(df.iloc[i]["listed_date"]),
        # "공모가": float(df.iloc[i]["offer_price"]),
        # "시초가": float(df.iloc[i]["sicho_p"]),
        # "공모대비수익률": float(df.iloc[i]["profit_percent"]),
        # "매출액": float(df.iloc[i]["sales"]),
        # "순이익": float(df.iloc[i]["profit"]),
        # "구주매출": int(df.iloc[i]["shares_to_pub"]),
        # "수요예측일": df.iloc[i]["pre_demand_day"],
        # "청약일": df.iloc[i]["subs_day"],
        # "희망공모가(하단)": int(df.iloc[i]["l_exp_offer_price"]),
        # "희망공모가(상단)": int(df.iloc[i]["h_exp_offer_price"])
        
        "cor_name" : df.iloc[i]["cor_name"],
        "cor_rate": float(df.iloc[i]["cor_rate"]),
        "obligation": float(df.iloc[i]["obligation"]),
        "market_type": int(df.iloc[i]["market_type"]),
        "listed_date": int(df.iloc[i]["listed_date"]),
        "offer_price": int(df.iloc[i]["offer_price"]),
        "sicho_p": int(df.iloc[i]["sicho_p"]),
        "profit_percent": float(df.iloc[i]["profit_percent"]),
        "sales": int(df.iloc[i]["sales"]),
        "profit": int(df.iloc[i]["profit"]),
        "shares_to_pub": float(df.iloc[i]["shares_to_pub"]),
        "sub_rate": float(df.iloc[i]["sub_rate"]),
        "pre_demand_day": df.iloc[i]["pre_demand_day"],
        "subs_day": df.iloc[i]["subs_day"],
        "l_exp_offer_price": int(df.iloc[i]["l_exp_offer_price"]),
        "h_exp_offer_price": int(df.iloc[i]["h_exp_offer_price"]),
        "sicho_exp": None,
    }

    dpInsert = db.inform.insert_one(info)  # db에 정보 입력

print("finish!")


