import telegram
from telegram.ext import Updater,MessageHandler,Filters,CommandHandler
import os
from telegram_bot.config import api_key
from pymongo import MongoClient
import matplotlib.pyplot as plt
import pandas as pd
import pickle
import numpy as np
from database.predict2_database import get2_data_csv
from DART.Search_report import get_find_Report
from naver_news.news import find_news_1
from naver_news.subscrible_new2 import find_news2
from draw_graph.draw import get_graph,get2_graph
from apscheduler.schedulers.blocking import BlockingScheduler
from naver_news.config import client_id,client_secret
import time
import requests
import asyncio
# from Crawling.Crawling_main import Crawling_main

from Crawling.Crawling_38_basic_info import crawling_38_basic_info
from Crawling.Crawling_38_day import crawling_38_day
from Crawling.Crawling_data import crawling_data
from Crawling.Crawling_data import crawling_data
from Crawling.Crawling_news_url import news_main
from Crawling.preprocessing import preprocessing

from Crawling_ALL_day import Crawling_day_alarm,push_day_alarm
from client_db import search_id,insert_sub,delete_sub,list_sub,toggle_sub

# 몽고디비,데이터모델,텔레그램 호환
bot = telegram.Bot(token = api_key)
BASE_PATH  = os.getcwd()

client = MongoClient('localhost', 27017)
db = client['Ipo2']
db2 = client['Ipo2_client']

with open('regression/saved_model.pickle','rb') as f:
        model3 = pickle.load(f)


#뉴스기사 보관 리스트
subscribe=[]       
old_links=[]    

Flag_toggle=0
chat_id_News=0

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


info_message = '''<명령어 종류>

- 그래프 시각화

    - 전체 데이터 그래프 시각화
        /chart <기업>
        
    - 개별 데이터 그래프 시각화
        /chart2 <기업> <종류>

- 공시 <검색>

    /Search_Dart <기업> <갯수:Default:3>

- 뉴스 <검색>

    /Search_News <검색어> <갯수:Default:3>

- 뉴스 <구독>  

    /sub <검색어>  : 수시로 가져올 검색어 구독
    /unsub <검색어> : 수시로 가져올 검색어 구독해제
    /News_toggle : 구독알람 시작/종료
'''

def start(update, context):       
    bot.sendMessage(chat_id =update.effective_chat.id,text='안녕하세요 IPO 공모가 예측 봇 Stock-Manager 입니다.') # 채팅방에 입장했을 때, 인사말 
    bot.sendMessage(chat_id=update.effective_chat.id, text=info_message)

        
def handler(update, context):
    user_text = update.message.text # 사용자가 보낸 메세지를 user_text 변수에 저장합니다.
    chat_id_News = update.effective_chat.id
    
    search_id(chat_id_News)
    
    
    
    #############################미구현###################################################################################################################
    
    if '시초가' in user_text: 
        cor_name = user_text.split()[1]
        

        if  db.inform.find_one({'기업명': cor_name}):
            price = db.inform.find_one({'기업명': cor_name})['시초가']
            bot.send_message(chat_id=update.effective_chat.id, text=f"{cor_name} 주식의 시초가는 {price}원 입니다.") # 답장 보내기
        else:
            bot.send_message(chat_id=update.effective_chat.id, text="수집되지 않은 정보입니다.") # 답장 보내기
        
    
    elif '예측' in user_text:
            
        cor_name = user_text.split()[1]
        price,result_price,result_per=get_price(cor_name)
        bot.send_message(chat_id=update.effective_chat.id, text=f"<{cor_name}>\n공모가:  {price}\n예측 시초가:  {result_price}\n예상 수익률:  {result_per}%")
        
    
    #####################################################################################################################################################
    
    
    # 그래프 시각화 종류
    elif '차트종류' in user_text:
           bot.send_message(chat_id=update.effective_chat.id, text=f"1.경쟁률\n2.의무보유확약\n3.공모가\n4.매출액\n5.순이익")
           
    # 방사그래프 차트 구현완료   
    elif user_text.split()[0]=='/chart':
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
    elif user_text.split()[0]=='/chart2':
        
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
    elif '/dart' in user_text: 
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
    elif '/news' in user_text:
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
        
        insert_sub(chat_id_News,cor_name)
        
    elif user_text == '/list' :
        list_sub(chat_id_News)
    
    
    elif '/unsub' in user_text:
        
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
    
    # 데이터 갱신
    BASE_DIR = 'C:/Users/KHS/Desktop/대학교/데이터 청년 캠퍼스/깃허브/Prediction-of-IPO-stock-price-using-chatbot/Crawling/'
    start_time = time.time()
    print("시작")
    crawling_38_basic_info(BASE_DIR)
    crawling_38_day(BASE_DIR)
    crawling_data(BASE_DIR)

    preprocessing(BASE_DIR)
    

    df = pd.DataFrame(
        columns=[
            "cor_name",
            "title",
        ]
    )
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(news_main(df))
    
    df2 = pd.read_csv(BASE_DIR+'after_prepros.csv')
    df2.drop('Unnamed: 0',axis = 1,inplace = True)
    
    data=db.inform.find()
    df_origin=pd.DataFrame(data)
    df_origin.drop('_id',axis = 1,inplace = True)
    
    list_cor_name=[]
    
    for i in range(len(df2)):
        for j in range(len(df_origin)):
            if df2.iloc[i]['cor_name']==df_origin.iloc[j]['cor_name']:
                list_cor_name.append(df2.iloc[i]['cor_name'])

    list_cor_name=list(set(list_cor_name))
    
    for row in list_cor_name:
        df2 = df2[~df2['cor_name'].str.contains(row)]
            
    get2_data_csv(df2)
    
    print("종료")
    print('learning time : ',time.time()-start_time)
 
# 각종 일정 알람뿌리기 구현완료
def alarm():
    
    Crawling_day_alarm()
    result_Text,target_time=push_day_alarm()
    
    send_id=[]

    df = pd.DataFrame(db2.inform.find({},{'_id':False}))
    print(df)

    for i in range(len(df)):
        send_id.append(int(df['number_id'][i]))
     

    print("진행중")
    for row in send_id:
        print(row)
        if result_Text=='':
            bot.send_message(chat_id=row, text=f"<오늘의 공모주 일정정보>\n\n일정: {target_time}\n\n일정이 없습니다!\n")
        else:
            bot.send_message(chat_id=row, text=f"<오늘의 공모주 일정정보>\n\n일정: {target_time}\n{result_Text}")
            
sched = BlockingScheduler(timezone='Asia/Seoul')
sched.add_job(find_news2, 'interval', seconds = 10, id='my_job_id1')
sched.add_job(Crawling_main, 'interval', minutes = 10, id='my_job_id2')
sched.add_job(alarm, 'cron',hour=8,minute=0, second=0, id='my_job_id3')
sched.start()
 