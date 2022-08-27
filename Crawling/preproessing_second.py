import pandas as pd 
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

def processing_second():
    
    
    df = pd.read_csv(BASE_DIR/'final.csv',encoding='utf-8-sig')

    df = df.drop(['Unnamed: 0','Unnamed: 0.1','market_type','subs_day'],axis=1)
    df['h_exp_offer_price'] = df['h_exp_offer_price'].astype('int64')
    df['l_exp_offer_price'] = df['l_exp_offer_price'].astype('int64')
    df['offer_label'] = 0
    df.loc[df['h_exp_offer_price'] < df['offer_price'],'offer_label'] = 1
    df.loc[df['h_exp_offer_price'] == df['offer_price'],'offer_label'] = 1

    df.drop(['h_exp_offer_price','l_exp_offer_price'],axis=1,inplace=True) # 공모가가 희망공모가 최고랑 같으면 1 , 그렇지 않으면 0

    df['listed_date'] = pd.to_datetime(df['listed_date'], format='%Y%m%d')
    df = df.sort_values(by='listed_date',ascending=True).reset_index(drop=True)
    df['Year'] = df['listed_date'].dt.year 
    df['Month'] = df['listed_date'].dt.month 
    df = df.dropna(subset=['shares_to_pub'])
    df['profit'] = df['profit']-df['sales']

    return df





