import pandas as pd

def get_news_score(DIR):
    
    data = pd.read_csv(DIR+'news_title_labelprocessing.csv')

    data.drop(['Unnamed: 0'], axis = 1,inplace = True)

    data['label']=data['label'].replace('negative','-1').replace('neutral','0').replace('positive','1')
    data = data.astype({'label':'int64'})

    df_sum=data.groupby("기업명").sum()
    df_sum['count']=data.groupby("기업명")['제목'].count()
    df_sum['score']=round(df_sum['label']/df_sum['count'],3)

    df_sum = df_sum.rename(columns={'label': '점수','count':'합계','score':'총점'})

    df_sum.to_csv(DIR+'title_labelprocessing_Score.csv',encoding="UTF-8")

DIR='C:/Users/KHS/Desktop/대학교/데이터 청년 캠퍼스/깃허브/Prediction-of-IPO-stock-price-using-chatbot/Data_Preprocessing/'
get_news_score(DIR)