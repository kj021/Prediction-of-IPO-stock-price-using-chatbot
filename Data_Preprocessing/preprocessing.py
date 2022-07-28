import pandas as pd
import numpy as np
from sklearn import preprocessing
import matplotlib.pyplot as plt
import re
def df_rename(data1):
    data1.rename(columns = {'name':'기업명',
        'type': '시장 종류',
        'day': '상장일',
        'now_p': '현재가',
        'gongmo_p': '공모가',
        'sicho_p': '시초가',
        'first_p': '종가',
        'corp_cd': '종목코드'}, inplace = True)
    return data1


def df_rename_final(final_data):
    final_data.rename(columns = {
            '매출액':'매출액(백만원)',
            '순이익': '순이익(백만원)',
            '청약경쟁률': '시장 종류',
            '청약경쟁률': '청약경쟁률(:1)',
            '확정공모가': '확정공모가(원)',
            '경쟁률': '경쟁률(:1)',
            '의무보유확약': '의무보유확약(:1)',
            '공모가': '공모가(원)',
            '시초가': '시초가(원)'}, inplace = True)
    return final_data

def preprocessing_to_datacsv(data1): # data.csv에 대한 전처리
    data1 = data1.transpose()
    data1.rename(columns=data1.iloc[0],inplace = True)
    data1 = data1.drop(data1.index[0])
    data1.reset_index(inplace = True)
    data1.drop('index',axis=1,inplace=True)
    
    data1 = df_rename(data1)
    #기업명에 스팩이 들어간 경우 제거
    data1 = data1[~data1['기업명'].str.contains('스팩')]
    return data1

def preprocessing_to_benefitcsv(data): # 38com_benefit.csv에 대한 전처리 
    data.drop(['Unnamed: 0'], axis = 1,inplace = True)
    data = data.dropna()
    index1 = data[data['의무보유확약'] == '0.00%'].index
    #의무보유확약이 0 인 것도 제거
    data = data.drop(index1)
    #변수들은 int형으로 바꿀 것이기 때문에 특수문자 제거 
    data.replace('(:1|%|,|:)','',regex = True, inplace= True)
    data.reset_index(inplace = True)
    data.drop('index',axis=1,inplace=True)
    data = data[1:]
    data = data.astype({'경쟁률':'float',
                    '의무보유확약': 'float',
                    '시초/공모%(수익률)':'float'})
    data = data[~data['기업명'].str.contains('스팩')]
    return data

def preprocessing_add_variablecsv(data_added,data1,data):
    data_added.drop(['Unnamed: 0'], axis = 1,inplace = True)
    
    regex = "\(.*\)|\s-\s.*" 
    for i in range(len(data_added)):
        data_added['매출액'][i] = re.sub(regex,'',data_added['매출액'][i])
    for i in range(len(data_added)):
        data_added['순이익'][i] = re.sub(regex,'',data_added['순이익'][i])
    
    data_added.replace('',np.nan,inplace = True)
    data_added.dropna(subset=['매출액'],inplace = True)
    data_added.dropna(subset=['순이익'],inplace = True)
    data_added = data_added[data_added['희망공모가액'] != '- ~ - 원']

    df_inner_join = pd.merge(data_added,data, left_on = '기업명',right_on ='기업명',how='inner')
    final_data = pd.merge(df_inner_join,data1, left_on = '기업명',right_on ='기업명',how='inner')
    final_data.drop('확정공모가',axis = 1)
    final_data.replace('(:1|:|원)','',regex = True, inplace= True)
    final_data.loc[final_data['구주매출'].str.contains('%') == True,'구주매출'] = 1
    
    final_data['희망공모가(최저)'] = final_data['희망공모가액']
    final_data['희망공모가(최고)'] = final_data['희망공모가액']

    final_data.drop('희망공모가액',axis = 1,inplace = True)

    final_data['희망공모가(최저)'] = final_data['희망공모가(최저)'].str[:10]
    final_data['희망공모가(최고)'] = final_data['희망공모가(최고)'].str[9:]


    final_data.replace('(,|~)','',regex = True, inplace= True)
    final_data.replace("\(.*\)|\ㄴ-\ㄴ.*",'',regex = True,inplace=True)
   
    final_data = df_rename_final(final_data)

    final_data = final_data.astype({'매출액(백만원)':'float',
                    '순이익(백만원)': 'float',
                    '희망공모가(최저)':'float',
                     '희망공모가(최고)':'float',
                     '청약경쟁률(:1)': 'float',
                     })
    final_data.drop('확정공모가(원)',axis = 1)



    return final_data




def total_preprocessing(data1,data,data_added):

    data_info = preprocessing_to_datacsv(data1)
    print(1)
    data_benefit = preprocessing_to_benefitcsv(data)
    print(2)
    final_data = preprocessing_add_variablecsv(data_added,data_info,data_benefit)
    
    return final_data