import pandas as pd

def get_news_score():
    
    data = pd.read_csv('/Users/seop/Documents/GitHub/Prediction-of-IPO-stock-price-using-chatbot/jiseop_test/after_prepros_get_label.csv')
    print(data.columns)
    data.drop(['Unnamed: 0'], axis = 1,inplace = True)

    data['label']=data['label'].replace('negative','-1').replace('neutral','0').replace('positive','1')
    data = data.astype({'label':'int64'})

    df_sum=data.groupby("cor_name").sum()
    df_sum['count']=data.groupby("cor_name")['title'].count()
    df_sum['score']=round(df_sum['label']/df_sum['count'],3)

    # df_sum = df_sum.rename(columns={'label': '점수''count':'합계','score':'총점'})
    del df_sum['count']
    del df_sum['label']
    df_sum.to_csv('/Users/seop/Documents/GitHub/Prediction-of-IPO-stock-price-using-chatbot/jiseop_test/after_prerpos_get_score.csv',encoding="utf-8-sig")


get_news_score()