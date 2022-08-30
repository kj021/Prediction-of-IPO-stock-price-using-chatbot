import telegram
from telegram.ext import Updater,MessageHandler,Filters,CommandHandler
import os
from pymongo import MongoClient
import matplotlib.pyplot as plt
import pandas as pd
import pickle
import numpy as np
from apscheduler.schedulers.blocking import BlockingScheduler

#아이디,비밀번호
from telegram_bot.config import api_key


# 주기적으로 DB 최신화
from Crawling.Crawling_main import Crawling_total

# 사용 함수
from DART.Search_report import get_find_Report
from naver_news.news import find_news_1
from naver_news.subscrible_new2 import find_news2
from draw_graph.draw import get_graph,get2_graph
from Crawling.Crawling_ALL_day import Crawling_day_alarm,push_day_alarm
from database.client_db import search_id,insert_sub,delete_sub,list_sub,toggle_sub

# 몽고디비,데이터모델,텔레그램 호환
bot = telegram.Bot(token = api_key)
BASE_PATH  = os.getcwd()

client = MongoClient('localhost', 27017)
db = client['Ipo2']
db2 = client['Ipo2_client']

# 예측 시초가 모델 
with open('regression/saved_model.pickle','rb') as f:
        model3 = pickle.load(f)


# updater
updater = Updater(token=api_key, use_context=True)
dispatcher = updater.dispatcher

# 시초가탐색 함수
def get_price(cor_name):
    
    x= db.inform.find_one({'cor_name': cor_name})
   
    x_test=[]
    x_test.append(x['cor_rate'])
    x_test.append(x['obligation'])
    x_test.append(x['shares_to_pub'])
    x_test.append(x['offer_price'])
    x_test.append(x['offer_label'])
    x_test.append(x['Quater_per'])
    x_test.append(x['search_amt'])

    x_new=np.array(x_test).reshape(1,-1)
    y_predict = float(model3.predict(x_new))
    print(y_predict)
    price_origin=int(x['offer_price'])
    y_predict=int(y_predict)
    price= round((((y_predict-price_origin)/price_origin)*100),2)
    
        
    return price_origin,y_predict,price


# 명령어 info 
info_message = '''<명령어 종류>

1. 일정 <알람>

    매일 오전 8시, 당일 공모주 일정을 자동적으로 보냅니다.
    
2. 시초가 예측

    명령어 : 예측 <기업> : 모델을 사용해, 기업의 시초가를 예측합니다.
    
3. 그래프 시각화

    - 전체 데이터 그래프 시각화
        명령어 : 종합차트 <기업>
        
    - 개별 데이터 그래프 종류 검색
        명령어 : 차트종류
        
    - 개별 데이터 그래프 시각화
        명령어 : 개별차트 <기업> <종류>

4. 공시 <검색>

    명령어 : 공시 <기업> <갯수:Default:3>

5. 뉴스 <검색>

    명령어 : 뉴스 <검색어> <갯수:Default:3>

6. 뉴스 <구독>  

    명령어 : 구독 <검색어>  : 수시로 가져올 검색어 구독
    명령어 : 구독취소 <검색어> : 수시로 가져올 검색어 구독해제
    명령어 : 구독리스트 : 구독리스트 확인
    명령어 : /news_toggle(메뉴) : 구독알람 시작/종료
'''

def start(update, context):       
    bot.sendMessage(chat_id =update.effective_chat.id,text='안녕하세요 IPO 공모가 예측 봇 Stock-Manager 입니다.') # 채팅방에 입장했을 때, 인사말 
    bot.sendMessage(chat_id=update.effective_chat.id, text=info_message)

        
def handler(update, context):
    user_text = update.message.text # 사용자가 보낸 메세지를 user_text 변수에 저장합니다.
    chat_id_News = update.effective_chat.id
    
    search_id(chat_id_News)
    
    
    if user_text.split()[0]=='예측':
        
        try:
            cor_name = user_text.split()[1]
            price,result_price,result_per=get_price(cor_name)
            bot.send_message(chat_id=update.effective_chat.id, text=f"<{cor_name}>\n공모가:  {price}\n예측 시초가:  {result_price}\n예상 수익률:  {result_per}%")
        except TypeError:
            bot.send_message(chat_id=update.effective_chat.id, text="수집되지 않은 정보입니다.")
        
        
    
    # 그래프 시각화 종류
    elif user_text.split()[0]=='차트종류':
           bot.send_message(chat_id=update.effective_chat.id, text=f"1.경쟁률\n2.의무보유확약\n3.공모가\n4.매출액\n5.순이익")
           
    # 방사그래프 차트 구현완료   
    elif user_text.split()[0]=='종합차트':
        cor_name = user_text.split()[1]
        
        bot.send_message(chat_id=update.effective_chat.id, text=f"{cor_name} 주식의 차트를 불러오는 중입니다!")
        plt.clf()
        try:
            buf,data1,data2,data3,data4,data5,data_len= get2_graph(cor_name)
            
            bot.send_photo(chat_id =update.effective_chat.id,photo=buf)
            bot.send_message(chat_id=update.effective_chat.id, text=f"<{cor_name} 의 컬럼별 순위>\n\n경쟁률 : {data1}/{data_len}등\n\n의무보유확약 : {data2}/{data_len}등\n\n공모가 : {data3}/{data_len}등\n\n매출액 : {data4}/{data_len}등\n\n순이익 : {data5}/{data_len}등")
            
        except KeyError:
            bot.send_message(chat_id=update.effective_chat.id, text="수집되지 않은 정보입니다.")
     
    # 각각 그래프 구현 구현완료    
    elif user_text.split()[0]=='개별차트':
        
        cor_name = user_text.split()[1]
        cor_shape = user_text.split()[2]
            
        bot.send_message(chat_id=update.effective_chat.id, text=f"{cor_name} 주식의 차트를 불러오는 중입니다!")
        plt.clf()
        
        try:
            buf,rank,rank_sum = get_graph(cor_name,cor_shape)
            
            bot.send_photo(chat_id =update.effective_chat.id,photo=buf)
            bot.send_message(chat_id=update.effective_chat.id, text=f"{cor_name} 주식은 전체 데이터의 {rank}/{rank_sum}등입니다.")
        except KeyError:
            bot.send_message(chat_id=update.effective_chat.id, text="수집되지 않은 정보입니다.")
        
    #다트(검색) -> 완료
    elif user_text.split()[0]=='공시':
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
    elif user_text.split()[0]=='뉴스':
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
            if rows != '':
                bot.send_message(chat_id=update.effective_chat.id, text=f"{rows}")
        
        
       
    # 뉴스(구독) -> 완료
    
    elif user_text.split()[0]=='구독':
        cor_name = user_text.split()[1]
        
        insert_sub(chat_id_News,cor_name)
        
    elif user_text.split()[0]=='구독리스트':
        list_sub(chat_id_News)
    
    
    elif user_text.split()[0]=='구독취소':
        
        cor_name = user_text.split()[1]
        delete_sub(chat_id_News,cor_name)
        
           
#뉴스(구독) 스위치 -> 완료      
def News_toggle(update, context):
    chat_id_News = update.effective_chat.id
    toggle_sub(chat_id_News)       
        
    
             
   
start_handler = CommandHandler('start',start)
toggle_handler = CommandHandler('News_toggle',News_toggle) 
echo_handler = MessageHandler(Filters.text,handler) # chatbot에게 메세지를 전송하면,updater를 통해 필터링된 text가 handler로 전달이 된다. -> 가장 중요하고, 계속해서 수정할 부분


dispatcher.add_handler(start_handler)
dispatcher.add_handler(toggle_handler)
dispatcher.add_handler(echo_handler)



updater.start_polling() # 주기적으로 텔레그램 서버에 접속해서 chatbot으로부터 새로운 메세지가 존재하면 받아오는 명령어.

def Crawling_main():
    Crawling_total()
        
 
# 각종 일정 알람뿌리기 구현완료
def alarm():
    
    df_temp=Crawling_day_alarm()
    result_Text,target_time=push_day_alarm(df_temp)
    
    send_id=[]

    df = pd.DataFrame(db2.inform.find({},{'_id':False}))

    for i in range(len(df)):
        send_id.append(int(df['number_id'][i]))
     

    print("진행중")
    for row in send_id:
        if result_Text=='':
            bot.send_message(chat_id=row, text=f"<오늘의 공모주 일정정보>\n\n일정: {target_time}\n\n일정이 없습니다!\n",parse_mode= 'Markdown',disable_web_page_preview=True)
        else:
            bot.send_message(chat_id=row, text=f"<오늘의 공모주 일정정보>\n\n일정: {target_time}\n{result_Text}",parse_mode= 'Markdown',disable_web_page_preview=True)
        
sched = BlockingScheduler(timezone='Asia/Seoul')
sched.add_job(find_news2, 'interval', minutes=1, id='my_job_id1')
sched.add_job(Crawling_main, 'interval', minutes=30, id='my_job_id2')
sched.add_job(alarm, 'cron',hour=8,minute=0, second=0, id='my_job_id3')

sched.start()
 