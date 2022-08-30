import pandas as pd
from pymongo import MongoClient
import time
from telegram.ext import Updater,MessageHandler,Filters,CommandHandler
from naver_news.config import client_id,client_secret
import requests
import telegram
from telegram_bot.config import api_key

client = MongoClient('localhost', 27017)
db2 = client['Ipo2_client']

bot = telegram.Bot(token = api_key)

def find_news2():
    
    search_item=[]
    df2 = pd.DataFrame(db2.inform.find({},{'_id':False}))
    
    for i in range(len(df2)):
        
        if df2.loc[i,'toggle_id']==1:
            
            id_name=int(df2.loc[i,'number_id'])
            id_old_link=df2.loc[i,'old_link_id']
            data_re=df2.loc[i,'sub_id']
            
            if data_re==None:
                continue
            else:
                for row in data_re:
                    search_item.append(row)
        
            for row in data_re:
                print("---------진행중-----------")
                result_title=""
                search_word = row #검색어
                encode_type = 'json' #출력 방식 json 또는 xml
                max_display = 1 #출력 뉴스 수
                sort = 'sim' #결과값의 정렬기준 시간순 date, 관련도 순 sim
                start = 1 # 출력 위치
                
                check=0

            
                url = f"https://openapi.naver.com/v1/search/news.{encode_type}?query={search_word}&display={str(int(max_display))}&start={str(int(start))}&sort={sort}"

                #헤더에 아이디와 키 정보 넣기
                headers = {'X-Naver-Client-Id' : client_id,
                    'X-Naver-Client-Secret': client_secret
                        }

                #HTTP요청 보내기
                r = requests.get(url, headers=headers)
                time.sleep(1)
                #요청 결과 보기 200 이면 정상적으로 요청 완료 .json -> pandas
                df=pd.DataFrame(r.json()['items'])
                news_title=df['originallink'].head(1)
                
                # 링크 전처리
                for j in news_title:
                    data= str(j.replace("</b>","").replace("<b>","").replace("&apos;","").replace("&quot;",""))
                    result_title=data
                    
                    
                # (구)링크 와 (신)링크 비교
                try:
                    for rows in id_old_link:
                        if result_title == rows:
                            check=1
                except:
                    id_old_link=['temp']
                    pass
                
                      
                # 메세지 보내기
                if check==0:
                    bot.send_message(chat_id=id_name, text=f"{result_title}")
                
            
                
                for i in news_title:
                    data= str(i.replace("</b>","").replace("<b>","").replace("&apos;","").replace("&quot;",""))
                    id_old_link.append(data)
                    id_old_link=list(set(id_old_link))
                
                if len(id_old_link)>=15:
                    del id_old_link[0:8]
                       
                db2.inform.update_one(
                {"number_id" : id_name},
                {"$set" : {
                    "old_link_id" : id_old_link
                }
                })
            
                check=0
                time.sleep(1)

        elif df2.loc[i,'toggle_id']==0:
            print("안보냄")
            
            
find_news2()