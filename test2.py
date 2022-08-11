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
from naver_news.news import find_news
from draw_graph.draw import get_graph
from naver_news.subscribe_news import find_news
import threading
import time


bot = telegram.Bot(token = api_key)
BASE_PATH  = os.getcwd()

info_message = '''다음의 명령어를 입력해주세요.

- 안부 물어보기 : 뭐해
- 공모주 가격 물어보기 : 공모주 + "기업명"
- 차트 보기 : "기업명" + 차트
- 사진 보기 : 사진
'''
client = MongoClient('localhost', 27017)
db = client['Ipo']



with open('regression/saved_model.pickle','rb') as f:
        model3 = pickle.load(f)

        


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

subscribe=[]
reset=0
flag=0
reset=0

flag_stop=0

def start(update, context):
        
    bot.sendMessage(chat_id =update.effective_chat.id,text='안녕하세요 IPO 공모가 예측 봇 Stock-Manager 입니다.') # 채팅방에 입장했을 때, 인사말 
    bot.sendMessage(chat_id=update.effective_chat.id, text=info_message)


# def stop(update, context):
#     bot.sendMessage(chat_id =update.effective_chat.id,text='<명령어 실행>') # 채팅방에 입장했을 때, 인사말 
   
#     if flag==0: 
#         t=threading.Timer(30,find_news(subscribe))
#         t.start() 
#     if flag==1: 
#         t.cancel() 
        
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
       
    elif '공시' in user_text: 
        # except 발생안함 -> 내부 안에서 변경해야함
        cor_name = user_text.split()[1]
        count = int(user_text.split()[2])
        Text=[]
        Text.clear() 
        
        try:       
            Text=get_find_Report(cor_name,count)
            result_Text = "\n".join(Text)
            bot.send_message(chat_id=update.effective_chat.id, text=f"공시정보\n\n{result_Text}")
        except KeyError:
            bot.send_message(chat_id=update.effective_chat.id, text="수집되지 않은 정보입니다.")
        
    elif '뉴스' in user_text:
        # except 발생안함 -> 내부 안에서 변경해야함
        cor_name = user_text.split()[1]
        count = int(user_text.split()[2])
        
     
        Text2=[]
        Text2.clear()        
        Text2=find_news(cor_name,count)
        
        try:
            for rows in Text2:
                bot.send_message(chat_id=update.effective_chat.id, text=f"{rows}")
        except KeyError:
            bot.send_message(chat_id=update.effective_chat.id, text="수집되지 않은 정보입니다.")
                         
                  
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
    
    elif '/sub' in user_text:
        cor_name = user_text.split()[1]
        subscribe.append(cor_name)
        print(subscribe)
        
        bot.send_message(chat_id=update.effective_chat.id, text=f"<뉴스구독리스트>\n <{cor_name}> 추가되었습니다.")
    
    elif '/list' in user_text:
        bot.send_message(chat_id=update.effective_chat.id, text=f"<뉴스구독리스트>\n {subscribe}")
    
    
    elif '/del' in user_text:
        
        cor_name = user_text.split()[1]
        subscribe.remove(cor_name)
        print(subscribe)
        
        bot.send_message(chat_id=update.effective_chat.id, text=f"<뉴스구독리스트>\n <{cor_name}> 삭제됐습니다.")     
   
    elif user_text=='종료':
        global flag_stop
        flag_stop=0
        print(flag_stop)
        
    elif user_text=='시작':
        
        flag_stop=1
        print(flag_stop) 
        
    elif user_text=='수정':
        global reset
        reset=1
        print(flag_stop)      


   
start_handler = CommandHandler('start',start)
echo_handler = MessageHandler(Filters.text,handler) # chatbot에게 메세지를 전송하면,updater를 통해 필터링된 text가 handler로 전달이 된다. -> 가장 중요하고, 계속해서 수정할 부분
# stop_handler = CommandHandler('stop',stop) 

updater.dispatcher.add_handler(start_handler)
updater.dispatcher.add_handler(echo_handler)
# updater.dispatcher.add_handler(stop_handler)

updater.start_polling() # 주기적으로 텔레그램 서버에 접속해서 chatbot으로부터 새로운 메세지가 존재하면 받아오는 명령어.

flag_t=0
print("--------실행중-----\n")

while True:
    if subscribe!=None and flag_t==0 and flag_stop==1:
        print("시작")
        t=threading.Timer(30,find_news(subscribe))
        t.start()
        flag_t=1
    
    if reset==1 and flag_t==1:
        print("종료(수정")
        t.cancel()
        reset=0
        flag_t=0
        

    if flag_t==1 and flag_stop==0:
        print("종료")
        t.cancel()
        flag_t=0 
            
        
    print(flag_t,flag_stop,reset)
    time.sleep(2)