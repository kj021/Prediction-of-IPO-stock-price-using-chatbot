import pandas as pd
from pymongo import MongoClient
import telegram
from telegram_bot.config import api_key

bot = telegram.Bot(token = api_key)
client = MongoClient('localhost', 27017)
db2 = client['Ipo2_client']
 
# DB 생성하기    
def search_id(chat_id_News):
    df = pd.DataFrame(db2.inform.find({},{'_id':False}))
    
    print(df)	
    print(chat_id_News)

    CHECK=0
    
    for i in range(len(df)):
       
        if df['number_id'][i]==chat_id_News:
            CHECK=1
    
    print(CHECK)

    if CHECK==0:
        print("들어감")
        info={
        "number_id" :chat_id_News,
        "sub_id" : None
        }
        db2.inform.insert_one(info)
    else:
        print("안들어감")


# DB 넣기  

def insert_sub(chat_id_News,cor_name):
    chat_id_News=int(chat_id_News)
    
    df = pd.DataFrame(db2.inform.find({},{'_id':False}))
    
    for i in range(len(df)):
        if df['number_id'][i]==chat_id_News:
            i_save=i
    
    if df.iloc[i_save]['sub_id'] == None:
        data_re=[]
    else:   
        data_re=df.iloc[i_save]['sub_id']
    
    data_re.append(cor_name)
    
    
    db2.inform.update_one(
    {"number_id" : chat_id_News},
    {"$set" : {
        "sub_id" : data_re
    }
    })
    
    bot.send_message(chat_id=chat_id_News, text=f"<뉴스구독리스트>\n <{cor_name}> 추가되었습니다.")
    print("삽입완료")

# DB 뺴기
    
def delete_sub(chat_id_News,cor_name):
    chat_id_News=int(chat_id_News)
    i_delete=0
    
    df = pd.DataFrame(db2.inform.find({},{'_id':False}))
    
    for i in range(len(df)):
        if df['number_id'][i]==chat_id_News:
            i_delete=i
        
    data_re=df.iloc[i_delete]['sub_id']
    
    
    if cor_name in data_re:
        for i in range(len(data_re)):
            if cor_name==data_re[i]:
                i_delete=i
                
        del data_re[i_delete]
            
        db2.inform.update_one(
        {"number_id" : chat_id_News},
        {"$set" : {
            "sub_id" : data_re
        }
        })
        
        print("삭제완료")
        bot.send_message(chat_id=chat_id_News, text=f"<뉴스구독리스트>\n <{cor_name}> 삭제됐습니다.")         
    else:
        bot.send_message(chat_id=chat_id_News, text=f"<뉴스구독리스트>\n 자료가 없습니다.")         
        print("관련 자료가 없습니다")

#DB 조회하기
    
def list_sub(chat_id_News):
    search_item=[]
    chat_id_News=int(chat_id_News)
    i_search=0
    
    df = pd.DataFrame(db2.inform.find({},{'_id':False}))
    
    for i in range(len(df)):
        if df['number_id'][i]==chat_id_News:
            i_search=i
        
    data_re=df.iloc[i_search]['sub_id']

    if len(data_re)!=0:
        for row in data_re:
            search_item.append(row)
    else:
        print("자료가 없습니다.")    
        
    Text = "\n".join(search_item)
    
    print("조회 완료")
    bot.send_message(chat_id=chat_id_News, text=f"<뉴스구독리스트>\n\n{Text}")
    
    
    
    
        
    
    