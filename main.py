import telegram
from telegram.ext import Updater,MessageHandler,Filters,CommandHandler
import emoji
import os
from telegram_bot.config import api_key,chat_id
from database.stock import StockModel
from pymongo import MongoClient
from database.config import MONGO_URL, MONGO_DB_NAME

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

def start(update, context):
    bot.sendMessage(chat_id = chat_id,text='안녕하세요 IPO 공모가 예측 봇 Stock-Manager 입니다.') # 채팅방에 입장했을 때, 인사말 
    bot.sendMessage(chat_id=update.effective_chat.id, text=info_message)


# bot.sendMessage(chat_id = chat_id,text=info_message)

# updater
updater = Updater(token=api_key, use_context=True)
dispatcher = updater.dispatcher
updater.start_polling() # 주기적으로 텔레그램 서버에 접속해서 chatbot으로부터 새로운 메세지가 존재하면 받아오는 명령어.

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

    elif '차트' in user_text:
        cor_name = user_text.split()[0]
        bot.send_message(chat_id=update.effective_chat.id, text=f"{cor_name}주식의 차트를 불러오는 중입니다!")
        bot.send_message(chat_id =update.effective_chat.id,text=emoji.emojize(':chart_with_upwards_trend:',language='alias'))

    elif '사진' in user_text:
        bot.send_photo(chat_id = update.effective_chat.id, photo=open(BASE_PATH+'/telegram_bot/test_chart.jpeg','rb')) #

start_handler = CommandHandler('start',start)
echo_handler = MessageHandler(Filters.text,handler) # chatbot에게 메세지를 전송하면,updater를 통해 필터링된 text가 handler로 전달이 된다. -> 가장 중요하고, 계속해서 수정할 부분


dispatcher.add_handler(start_handler)
dispatcher.add_handler(echo_handler)


'''

data1 = pd.read_csv('/Users/seop/Documents/GitHub/Prediction-of-IPO-stock-price-using-chatbot/Data_Preprocessing/data.csv',encoding='euc-kr')
data = pd.read_csv('/Users/seop/Documents/GitHub/Prediction-of-IPO-stock-price-using-chatbot/Data_Preprocessing/38com_benefit.csv')
data_added = pd.read_csv('/Users/seop/Documents/GitHub/Prediction-of-IPO-stock-price-using-chatbot/Data_Preprocessing/38_add_variable.csv', encoding = 'euc-kr')


from Data_Preprocessing.preprocessing import total_preprocessing
new_df = total_preprocessing(data1,data,data_added)

'''

