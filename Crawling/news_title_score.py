import pandas as pd
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
def get_news_score():
    
    data = pd.read_csv(BASE_DIR/'Crawling/after_prepros_label.csv')

    print(data.columns)
    data.drop(['Unnamed: 0'], axis = 1,inplace = True)



    data['label']=data['label'].replace('negative','-1').replace('neutral','0').replace('positive','1')
    data = data.astype({'label':'int64'})
    data
    df_sum=data.groupby("cor_name").sum()

    df_count=data.groupby("cor_name").count()


    df_sum['score'] = round(df_sum['label']/df_count['label'],2)


    temp_df = pd.DataFrame(df_sum['score'])

    temp_df = temp_df .reset_index()

    df = pd.read_csv(BASE_DIR/'Crawling/after_prepros.csv').drop('Unnamed: 0',axis = 1)
    df = df.merge(temp_df,on='cor_name')

    df.to_csv(BASE_DIR/'Crawling/after_prepros_get_score.csv',encoding="utf-8-sig")
    print('score finish')

