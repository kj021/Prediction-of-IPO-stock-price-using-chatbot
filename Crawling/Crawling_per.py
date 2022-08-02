#http://www.38.co.kr/html/fund/index.htm?o=nw&page=1   리스트만 쭉 뽑음

import urllib.request as ur
import requests, re, time
from bs4 import BeautifulSoup as bs
from collections import defaultdict
import pandas as pd
import numpy as np

url = 'http://www.38.co.kr/html/fund/index.htm?o=nw&page=' #전체 리스트화면 url
url2 = 'http://www.38.co.kr/chart/chart_page_new.php3?code=' #개별 장외종가 url

def crawling_data_per():
    dics = defaultdict(list)
    for n in range(1,66):
            
        temp = url+str(n)
        html = ur.urlopen(temp)
        temp = bs(html.read(), "html.parser")

        temp = temp.find('table', {'summary':'신규상장종목'})

        trs = temp.find_all('tr')
            # print(f'페이지 {n}')
        dics_page = {}
        for i in trs:
            td_list = []
            tds = i.find_all('td')
            for ii in tds:
                td_list.append(ii.text.replace('\xa0',''))

            try:
                    #이름구간
                    
                name = td_list[0]
                if not name:
                    continue
                type = ''#시장
                if bool(re.search('\(유가\)',name)): #코스피
                    type = 'kospi'
                    name.replace('(유가)','')
                else:
                    type = 'kosdaq'
                    # print(name,type)
                dics['name'].append(name)  #회사이름
                dics['type'].append(type)  #시장종류
                dics['day'].append(td_list[1].replace('/',''))  #상장일
                dics['gongmo_p'].append(td_list[4].replace(',','')) #공모가
                dics['sicho_p'].append(td_list[6].replace(',','')) #시초가
                    
                if dics['sicho_p'] in ['-']:
                    raise Exception('데이터 없음')

                corp_cd = re.search("(?←\=)\d*$",tds[-1].find('a')['href'])[0]
                dics['corp_cd'].append(corp_cd)  # 종목코드
            except:
                pass
        time.sleep(5)
    
    df = pd.DataFrame(dics)
    df.to_csv('D:/jupyterNotebook/data.csv')
    
def New_DataFrame():
    df_new=pd.read_csv('D:/jupyterNotebook/data.csv')
   
    df_new.drop(['Unnamed: 0'], axis = 1,inplace = True)
    
    # 스팩,리츠 제거
    df_new = df_new[~df_new['name'].str.contains('스팩')] 
    df_new = df_new[~df_new['name'].str.contains('리츠')]
    
    # 공모값 - 값 제거
    index1 = df_new[df_new['gongmo_p'] == '-'].index
    df_new = df_new.drop(index1)
    
    # 시초값 - 값 제거
    index1 = df_new[df_new['sicho_p'] == '-'].index
    df_new = df_new.drop(index1)
    
    # 공모<시초?1:0 and 비교를 위한 타입변경
    df_new = df_new.astype({'gongmo_p':'int64'})
    df_new = df_new.astype({'sicho_p':'int64'})
    df_new.info()
    df_new['count']=np.where(df_new['sicho_p']>df_new['gongmo_p'],1,0)
    
    
    df_new['day'] = pd.to_datetime(df_new['day'], format='%Y%m%d', errors='raise')
    
    # 역순으로 정렬
    data_cross=df_new.loc[::-1]
    data_cross['quarter']=data_cross['day'].dt.quarter
    data_cross['year']=data_cross['day'].dt.year
    
    count_sum=0
    count_def=0
    result=[]
    
    # per 구하는 공식
    for i in range(len(data_cross)):
    
        if data_cross.iloc[i]["quarter"]!=data_cross.iloc[i-1]["quarter"] and i!=0:
            count_sum=0
            count_def=0
            
        if data_cross.iloc[i]["count1"]==0:
            count_def=count_def+1
            count_sum=count_sum+1
        else:
            count_sum=count_sum+1
        
        result.append(round(1-(count_def/count_sum),2))
        
    data_cross['per']=result
    data_final=data_cross.loc[::-1]
    
    data_final.to_csv('D:/jupyterNotebook/temp.csv')

New_DataFrame()