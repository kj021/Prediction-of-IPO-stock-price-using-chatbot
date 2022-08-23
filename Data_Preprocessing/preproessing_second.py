def processing_second():
    import pandas as pd 

    df = pd.read_csv('/Users/seop/Documents/GitHub/Prediction-of-IPO-stock-price-using-chatbot/Crawling/after_prepros_get_score.csv')

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

def get_train_data(i):
    return df.loc[i,["cor_rate", "obligation","profit" ,"offer_price","score","sub_rate","offer_label","Quater_per","Month"]] # 마지막에 search_amt 변수 추가해야완성

df = processing_second()



