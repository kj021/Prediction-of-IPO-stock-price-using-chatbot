import pandas as pd
import numpy as np
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
def get_per():

    df_new=pd.read_csv(BASE_DIR/'Crawling/data.csv')

    df_new.drop(['Unnamed: 0'], axis = 1,inplace = True)
    df_new.drop(['market_type'], axis = 1,inplace = True)
    df_new.drop(['profit_percent'], axis = 1,inplace = True)
    df_new.drop(['first_p'], axis = 1,inplace = True)

    for i in range(len(df_new)):
        df_new.loc[i,'cor_name']=df_new.loc[i,'cor_name'].replace('(유가)','')
    
    df_new = df_new[~df_new['cor_name'].str.contains('스팩')] 
    df_new = df_new[~df_new['cor_name'].str.contains('리츠')]
        
        # 공모값 - 값 제거
    index1 = df_new[df_new['offer_price'] == '-'].index
    df_new = df_new.drop(index1)
        
        # 시초값 - 값 제거
    index1 = df_new[df_new['sicho_p'] == '-'].index
    df_new = df_new.drop(index1)
        
        # 공모<시초?1:0 and 비교를 위한 타입변경
    df_new = df_new.astype({'offer_price':'int64'})
    df_new = df_new.astype({'sicho_p':'int64'})
    df_new['count']=np.where(df_new['sicho_p']>df_new['offer_price'],1,-1)

    df_new['listed_date'] = pd.to_datetime(df_new['listed_date'], format='%Y%m%d', errors='raise')    
    data_cross=df_new.loc[::-1]

    count_sum=0
    count_def=0
    count=0
    result=[]
    count_Qt=0
    A=0

    data_cross['총점']=0
    data_cross['카운트']=0
    data_cross['분기카운트']=0

    data_cross["range"]=range(len(data_cross))
    data_cross=data_cross.set_index('range')

    data_cross['listed_date'] = pd.to_datetime(data_cross['listed_date'], format='%Y%m%d', errors='raise')  
    data_cross['quarter']=data_cross['listed_date'].dt.quarter
    data_cross['year']=data_cross['listed_date'].dt.year

    for i in range(len(data_cross)):
        
            if data_cross.iloc[i]["quarter"]!=data_cross.iloc[i-1]["quarter"] and i!=0:
                count_Qt+=round((count_sum+count_def)/count,3)
                result.append(count_Qt)
                
                count_sum=0
                count_def=0
                count_Qt=0
                count=0
                
            if data_cross.iloc[i]["count"]==-1:
                count_def=count_def-1
                count+=1
                data_cross.loc[i,"카운트"]=count
            else:
                count_sum=count_sum+1
                count+=1
                data_cross.loc[i,"카운트"]=count
                
            data_cross.loc[i,"총점"]=count_sum+count_def
    print(result)     
    data_cross['Quater_per']=0

    x=-1
    data_cross.reset_index(drop=True,inplace = True)
    for i in range(len(data_cross)):
        if data_cross.iloc[i]["quarter"]==4 and data_cross.iloc[i]["year"]==2009:
            data_cross.loc[i,"Quater_per"]=0
            continue
        elif data_cross.iloc[i]["quarter"]!=data_cross.iloc[i-1]["quarter"]and i!=0:
            x=x+1

        data_cross.loc[i,"Quater_per"]=result[x]
        
    data_cross.drop(['listed_date'], axis = 1,inplace = True)
    data_cross.drop(['offer_price'], axis = 1,inplace = True)
    data_cross.drop(['sicho_p'], axis = 1,inplace = True)
    data_cross.drop(['count'], axis = 1,inplace = True)
    data_cross.drop(['quarter'], axis = 1,inplace = True)
    data_cross.drop(['year'], axis = 1,inplace = True)
    data_cross.drop(['분기카운트'], axis = 1,inplace = True)

    df=pd.read_csv(BASE_DIR/'Crawling/data.csv')
    df.drop(['Unnamed: 0'], axis = 1,inplace = True)

    for i in range(len(df)):
        df.loc[i,'cor_name']=df.loc[i,'cor_name'].replace('(유가)','')
        
    df = df[~df['cor_name'].str.contains('스팩')] 
    df = df[~df['cor_name'].str.contains('리츠')]

    df_join=pd.merge(df, data_cross,how='left',left_on='cor_name', right_on='cor_name')

    df_join['listed_date'] = pd.to_datetime(df_join['listed_date'], format='%Y%m%d', errors='raise')  
    df_join['quarter']=df_join['listed_date'].dt.quarter
    df_join['year']=df_join['listed_date'].dt.year

    df_join=df_join.fillna(method='bfill')
    # print(df_join.columns)
    df = df_join[['cor_name','Quater_per']]
    temp = pd.read_csv(BASE_DIR/'Crawling/after_prepros.csv')
    merge_df = df.merge(temp,on='cor_name')
    merge_df.to_csv(BASE_DIR/'Crawling/after_prepros.csv')
