import telegram
from telegram.ext import Updater,MessageHandler,Filters,CommandHandler
import emoji
import os
from telegram_bot.config import api_key,chat_id
from database.stock import StockModel
from pymongo import MongoClient
import matplotlib.pyplot as plt
import pandas as pd
from io import BytesIO
import pickle
import numpy as np
from database.config import MONGO_URL, MONGO_DB_NAME

with open('regression/saved_model.pickle','rb') as f:
    model3 = pickle.load(f)


bot = telegram.Bot(token = api_key)
BASE_PATH  = os.getcwd()

info_message = '''다음의 명령어를 입력해주세요.

- 안부 물어보기 : 뭐해
- 공모주 가격 물어보기 : 공모주 + "기업명"
- 차트 보기 : "기업명" + 차트
- 사진 보기 : 사진
'''
client = MongoClient(MONGO_URL)
db = client['Ipo']

def start(update, context):
    bot.sendMessage(chat_id = chat_id,text='안녕하세요 IPO 공모가 예측 봇 Stock-Manager 입니다.') # 채팅방에 입장했을 때, 인사말 
    bot.sendMessage(chat_id=update.effective_chat.id, text=info_message)
    

# bot.sendMessage(chat_id = chat_id,text=info_message)

# updater
updater = Updater(token=api_key, use_context=True)
dispatcher = updater.dispatcher
updater.start_polling() # 주기적으로 텔레그램 서버에 접속해서 chatbot으로부터 새로운 메세지가 존재하면 받아오는 명령어.

def get_price(cor_name):
    
    x= db.inform.find_one({'기업명': cor_name})
    x_test=[x['희망공모가최고'],x['청약경쟁률'],x['확정공모가'],x['경쟁률'],x['의무보유확약']]
    x_new=np.array(x_test).reshape(1,-1)
    
    y_predict = float(model3.predict(x_new))
    
    price= int(x['공모가']+x['공모가']*(y_predict/100))
    
    return price,y_predict

def get_graph(cor_name,cor_shape):
    
    plt.style.use('ggplot')
    plt.rc('font', family='NanumGothic')
    df = pd.DataFrame(db.inform.find({},{'_id':False}))   # 모든 데이터 조회
    df=df.dropna()
    
    df['순위']=df[cor_shape].rank(method='min',ascending=True)
    df=df.sort_values(by=[cor_shape],ascending=False)
    
    plt.plot(df['순위'],df[cor_shape],color='black')
        
    x=df.loc[df['기업명']=='영창케미칼']['순위'].unique()
    y=df.loc[df['기업명']=='영창케미칼']['경쟁률'].unique()
        
    plt.scatter(x,y,color='r',s=200,label=cor_name) 
    
    
    plt.title(cor_name +"  "+ cor_shape)
    plt.xlabel('DATA',labelpad=1)
    plt.ylabel(cor_shape,labelpad=1)  
      
    plt.legend(loc="upper right")

    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    
    count=df['순위'].count()    
    rank_count=df.loc[df['기업명']==cor_name]['순위'].unique()
    rank_count=int(rank_count)
    
    return buf,rank_count,count
    
def handler(update, context):

    user_text = update.message.text # 사용자가 보낸 메세지를 user_text 변수에 저장합니다.

    if '뭐해' in user_text: 
        bot.send_message(chat_id=update.effective_chat.id, text="챗봇에 대해 공부하는 중이에요.") # 답장 보내기
    elif '공모주'in user_text: 
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
        buf,rank,rank_sum = get_graph(cor_name,cor_shape)
        bot.send_photo(chat_id =update.effective_chat.id,photo=buf)
        bot.send_message(chat_id=update.effective_chat.id, text=f"{cor_name}주식은 전체 데이터의 {rank}/{rank_sum}등입니다.")
        
    elif '사진' in user_text:
        bot.send_photo(chat_id = update.effective_chat.id, photo=open(BASE_PATH+'/telegram_bot/test_chart.jpeg','rb')) #

    elif '크롤링' in user_text:
        cor_name = user_text.split()[1]
        bot.send_photo(chat_id = update.effective_chat.id, photo=open(BASE_PATH+'/telegram_bot/test_chart.jpeg','rb')) #
    elif '예측' in user_text:
        cor_name = user_text.split()[1]
        result_price,result_per=get_price(cor_name)
        print(result_price,result_per)
        bot.send_message(chat_id=update.effective_chat.id, text=f"{cor_name}\n주식의 예측 시초가: {result_price}\n예상 수익률:{result_per}")

start_handler = CommandHandler('start',start)
echo_handler = MessageHandler(Filters.text,handler) # chatbot에게 메세지를 전송하면,updater를 통해 필터링된 text가 handler로 전달이 된다. -> 가장 중요하고, 계속해서 수정할 부분


dispatcher.add_handler(start_handler)
dispatcher.add_handler(echo_handler)

