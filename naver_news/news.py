import requests
import pandas as pd
import collections as co
from naver_news.config import client_id,client_secret

def find_news(cor_name,count):
    search_word = cor_name #검색어
    encode_type = 'json' #출력 방식 json 또는 xml
    max_display = count #출력 뉴스 수
    sort = 'date' #결과값의 정렬기준 시간순 date, 관련도 순 sim
    start = 1 # 출력 위치

    dfs=[]
    url = f"https://openapi.naver.com/v1/search/news.{encode_type}?query={search_word}&display={str(int(max_display))}&start={str(int(start))}&sort={sort}"

    #헤더에 아이디와 키 정보 넣기
    headers = {'X-Naver-Client-Id' : client_id,
           'X-Naver-Client-Secret':client_secret
            }

    #HTTP요청 보내기
    r = requests.get(url, headers=headers)
    #요청 결과 보기 200 이면 정상적으로 요청 완료 .json -> pandas
    df=pd.DataFrame(r.json()['items'])
    
    result_title=[]
    
    temp=df['originallink'].head(count)
    
    # title
    for i in temp:
        data= str(i.replace("</b>","").replace("<b>","").replace("&apos;","").replace("&quot;",""))
        result_title.append(data)
        
    return result_title

