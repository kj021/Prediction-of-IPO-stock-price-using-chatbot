import telegram
from telegram.ext import Updater,MessageHandler,Filters,CommandHandler
import os
from telegram_bot.config import api_key
from pymongo import MongoClient
import matplotlib.pyplot as plt
import pandas as pd
import pickle
import numpy as np
from database.predict_database import get_data_csv
from DART.Search_report import get_find_Report
from naver_news.news import find_news_1
from draw_graph.draw import get_graph
from apscheduler.schedulers.blocking import BlockingScheduler
from naver_news.config import client_id,client_secret
import time
import requests





# 몽고디비,데이터모델,텔레그램 호환
bot = telegram.Bot(token = api_key)
BASE_PATH  = os.getcwd()

client = MongoClient('localhost', 27017)
db = client['Ipo']

with open('regression/saved_model.pickle','rb') as f:
        model3 = pickle.load(f)


#뉴스기사 보관 리스트
subscribe=[]       
old_links=[]    

Flag_toggle=0


# bot.sendMessage(chat_id = chat_id,text=info_message)

# updater
updater = Updater(token=api_key, use_context=True)
dispatcher = updater.dispatcher

def get_price(cor_name):
    
    x= db.inform.find_one({'기업명': cor_name})
    if(x==None):
        DIR = 'C:/Users/KHS/Desktop/대학교/데이터 청년 캠퍼스/깃허브/Prediction-of-IPO-stock-price-using-chatbot'
        df = pd.read_csv(DIR+'/raw data/refined_data.csv')
        data_pre=list(df.loc[0])
        price_origin,price,y_predict= get_data_csv(data_pre)
     
    else:
        x_test=[x['희망공모가최고'],x['청약경쟁률'],x['확정공모가'],x['경쟁률'],x['의무보유확약']]
        x_new=np.array(x_test).reshape(1,-1)
        
        y_predict = float(model3.predict(x_new))
        
        price_origin=int(x['공모가'])
        price= int(x['공모가']+x['공모가']*(y_predict/100))
        y_predict=int(y_predict)
        
        
    return price_origin,price,y_predict

#뉴스 구독리스트 함수

def find_news():
    
    for row in subscribe:
        print("---------진행중-----------")
        result_title=""
        search_word = row #검색어
        encode_type = 'json' #출력 방식 json 또는 xml
        max_display = 1 #출력 뉴스 수
        sort = 'date' #결과값의 정렬기준 시간순 date, 관련도 순 sim
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
    time.sleep(1)


info_message = '''다음의 명령어를 입력해주세요.

- 안부 물어보기 : 뭐해
- 공모주 가격 물어보기 : 공모주 + "기업명"
- 차트 보기 : "기업명" + 차트
- 사진 보기 : 사진
'''

def start(update, context):       
    bot.sendMessage(chat_id =update.effective_chat.id,text='안녕하세요 IPO 공모가 예측 봇 Stock-Manager 입니다.') # 채팅방에 입장했을 때, 인사말 
    bot.sendMessage(chat_id=update.effective_chat.id, text=info_message)

        
def handler(update, context):
    user_text = update.message.text # 사용자가 보낸 메세지를 user_text 변수에 저장합니다.

    if '시초가' in user_text: 
        cor_name = user_text.split()[1]

        if  db.inform.find_one({'기업명': cor_name}):
            price = db.inform.find_one({'기업명': cor_name})['시초가']
            bot.send_message(chat_id=update.effective_chat.id, text=f"{cor_name} 주식의 시초가는 {price}원 입니다.") # 답장 보내기
        else:
            bot.send_message(chat_id=update.effective_chat.id, text="수집되지 않은 정보입니다.") # 답장 보내기
            
    elif '차트종류' in user_text:
       bot.send_message(chat_id=update.effective_chat.id, text=f"1.경쟁률\n2.의무보유확약\n3.청약경쟁률\n4.확정공모가\n")
       
    
    elif '차트' in user_text:
        
        cor_name = user_text.split()[1]
        cor_shape = user_text.split()[2]
            
        bot.send_message(chat_id=update.effective_chat.id, text=f"{cor_name}주식의 차트를 불러오는 중입니다!")
        plt.clf()
        
        try:
            buf,rank,rank_sum = get_graph(cor_name,cor_shape)
            
            bot.send_photo(chat_id =update.effective_chat.id,photo=buf)
            bot.send_message(chat_id=update.effective_chat.id, text=f"{cor_name}주식은 전체 데이터의 {rank}/{rank_sum}등입니다.")
        except KeyError:
            bot.send_message(chat_id=update.effective_chat.id, text="수집되지 않은 정보입니다.")
        
    elif '예측' in user_text:
        
        cor_name = user_text.split()[1]
        price,result_price,result_per=get_price(cor_name)
        bot.send_message(chat_id=update.effective_chat.id, text=f"<{cor_name}>\n공모가:  {price}\n예측 시초가:  {result_price}\n예상 수익률:  {result_per}%")
    
    
    #다트(검색)
    elif '/Search_Dart' in user_text: 
        # except 발생안함 -> 내부 안에서 변경해야함
        cor_name = user_text.split()[1]
        cor_name_len = len(user_text.split())
        
        if cor_name_len<=2 or user_text.split()[2].isnumeric() == False:
            count=3
        else:
            count = int(user_text.split()[2])
            
        Text=[]
        Text.clear() 
        
        try:       
            Text=get_find_Report(cor_name,count)
            result_Text = "\n".join(Text)
            bot.send_message(chat_id=update.effective_chat.id, text=f"공시정보\n\n{result_Text}")
        except KeyError:
            bot.send_message(chat_id=update.effective_chat.id, text="수집되지 않은 정보입니다.")
                       
    
    
    #뉴스(검색) -> 완료
    elif '/Search_News' in user_text:
        # except 발생안함 -> 내부 안에서 변경해야함
        cor_name = user_text.split()[1]
        cor_name_len = len(user_text.split())
        
        # 검색량(기사) 디폴트 : 3
        if cor_name_len<=2 or user_text.split()[2].isnumeric() == False:
            count=3
        else:
            count = int(user_text.split()[2])
        
     
        Text2=[]
        Text2.clear()        
        Text2=find_news_1(cor_name,count)
        
        for rows in Text2:
            bot.send_message(chat_id=update.effective_chat.id, text=f"{rows}")
        
       
    # 뉴스(구독) -> 완료
    elif '/sub' in user_text:
        cor_name = user_text.split()[1]
        subscribe.append(cor_name)
        
        bot.send_message(chat_id=update.effective_chat.id, text=f"<뉴스구독리스트>\n <{cor_name}> 추가되었습니다.")
    
    elif user_text == '/list' :
        Text2 = "\n".join(subscribe)
        bot.send_message(chat_id=update.effective_chat.id, text=f"<뉴스구독리스트>\n\n{Text2}")
    
    
    elif '/unsub' in user_text:
        
        cor_name = user_text.split()[1]
        subscribe.remove(cor_name)
        print(subscribe)
        
        bot.send_message(chat_id=update.effective_chat.id, text=f"<뉴스구독리스트>\n <{cor_name}> 삭제됐습니다.")     
     
           
#뉴스(구독) 스위치 -> 완료      
def News_toggle(update, context):       
    global Flag_toggle
        
    if Flag_toggle==0:
        context.bot.send_message(chat_id=update.effective_chat.id, text="작업을 시작합니다.")
 
        print("뉴스(구독) 시작")
        sched.add_job(find_news, 'interval', seconds = 10, id='my_job_id')
        Flag_toggle=1
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="작업을 중단합니다.")
 
        print("뉴스(구독) 종료")
        sched.remove_job('my_job_id')
        Flag_toggle=0
             
   
start_handler = CommandHandler('start',start)
toggle_handler = CommandHandler('News_toggle',News_toggle) 
echo_handler = MessageHandler(Filters.text,handler) # chatbot에게 메세지를 전송하면,updater를 통해 필터링된 text가 handler로 전달이 된다. -> 가장 중요하고, 계속해서 수정할 부분


dispatcher.add_handler(start_handler)
dispatcher.add_handler(toggle_handler)
dispatcher.add_handler(echo_handler)


updater.start_polling() # 주기적으로 텔레그램 서버에 접속해서 chatbot으로부터 새로운 메세지가 존재하면 받아오는 명령어.

    
sched = BlockingScheduler(timezone='Asia/Seoul')
sched.start()
 