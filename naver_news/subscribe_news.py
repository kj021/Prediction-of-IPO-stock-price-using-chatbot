from re import T
import time
import requests
import pandas as pd
import time
import threading
import telegram
from telegram.ext import Updater,MessageHandler,Filters,CommandHandler
import os
from telegram_bot.config import api_key,chat_id
from naver_news.config import client_id,client_secret

old_links=[]    
bot = telegram.Bot(token = api_key)
BASE_PATH  = os.getcwd()



def find_news(subscribe):
    
    for row in subscribe:
        print("-진행중-")
        result_title=""
        search_word = row #검색어
        encode_type = 'json' #출력 방식 json 또는 xml
        max_display = 1 #출력 뉴스 수
        sort = 'sim' #결과값의 정렬기준 시간순 date, 관련도 순 sim
        start = 1 # 출력 위치
        
        check=0

        dfs=[]
        url = f"https://openapi.naver.com/v1/search/news.{encode_type}?query={search_word}&display={str(int(max_display))}&start={str(int(start))}&sort={sort}"

        #헤더에 아이디와 키 정보 넣기
        headers = {'X-Naver-Client-Id' : client_id,
               'X-Naver-Client-Secret':client_secret
                }

        #HTTP요청 보내기
        r = requests.get(url, headers=headers)
        time.sleep(1)
        #요청 결과 보기 200 이면 정상적으로 요청 완료 .json -> pandas
        df=pd.DataFrame(r.json()['items'])
        news_title=df['originallink'].head(1)
        
        
        global old_links
       

        # 링크 전처리
        for i in news_title:
            data= str(i.replace("</b>","").replace("<b>","").replace("&apos;","").replace("&quot;",""))
            result_title=data
            
            
        # (구)링크 와 (신)링크 비교
        for rows in old_links:
            if result_title == rows:
                check=1
                
        # 메세지 보내기
        if check==0:
            bot.send_message(chat_id=1181758634, text=f"{result_title}")
        
        
        for i in news_title:
            data= str(i.replace("</b>","").replace("<b>","").replace("&apos;","").replace("&quot;",""))
            old_links.append(data)
            old_links=list(set(old_links))
      
        check=0
        
    # global t
    # t=threading.Timer(30,find_news(subscribe))
    # t.start()
    time.sleep(1)

# def Stop_find_news():
#     print("-종료-")
#     global t
#     t.cancel()
    


# find_news(subscribe)
# Stop_find_news()