# 파일 실행을 위해 아래 두개 pip install 필요
# pip install yfinance --upgrade --no-cache-dir
# pip install pandas_datareader

import pandas as pd
import numpy as np
import seaborn as sns
from sklearn import preprocessing
from pandas_datareader import data as pdr
import yfinance as yf
from collections import defaultdict
import time 
from datetime import datetime,timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
print(BASE_DIR)
# Prediction-of-IPO-stock-price-using-Telegram-chatbot

def get_before_day(string, day): # 날짜(string)을 기준으로 숫자(day)만큼의 전날을 반환
  date = datetime.strptime(string, '%Y-%m-%d')

  before_one_day = date - timedelta(days=day) # 유동적인 사용을 위한 숫자를 변수 day로 변경
  if before_one_day.month<10:
      month =  '0'+str(before_one_day.month)
  else:
      month = str(before_one_day.month)

  if before_one_day.day<10:
      day =  '0'+str(before_one_day.day)
  else:
      day = str(before_one_day.day)
      
  before_day = str(before_one_day.year)+'-'+month+'-'+day
  return before_day


def nasdaq_add():
  yf.pdr_override() 

  # after_prepros_youtong.csv의 listed_date 컬럼의 제일 첫번째 요소를 가져와야 함.
  # after_prepros_youtong.csv 불러오기
  final_data = pd.read_csv(BASE_DIR/'regression/after_prerpos_get_score.csv', encoding='utf-8-sig')
  datetime_string =  str(final_data['listed_date'][0])
  datetime_format = "%Y%m%d"

  datetime_result = (datetime.strptime(datetime_string, datetime_format).date()) # .date() -> 뒤에 초 제거
  datetime_result = str(datetime_result)
  # print(type(datetime_result))

  # download dataframe
  # 종목명: NASDAQ Composite (^IXIC)
  data = pdr.get_data_yahoo("^IXIC", start="2006-01-01", end=datetime_result) 
  # 데이터를 갱신하기 위해 end를 변수로 설정

  data.to_csv(BASE_DIR/'nasdaq_output.csv') # 최신 날짜의 나스닥 지수를 가져와야

  # df로 변환
  nasdaq_df = pd.read_csv(BASE_DIR/'nasdaq_output.csv')


  # 컬럼명 변경
  nasdaq_df.columns=['date','open','high','low','close','adj_close','volume'] 

  # 시장 수익률 계산
  # 시장 수익률 = (전날 종가 - 시작일 종가)/시작일 종가
  dif = ['-']

  for i in range(1, len(nasdaq_df['close']-1)):
    difference = dif.append((nasdaq_df['close'][i]-nasdaq_df['close'][i-1])/nasdaq_df['close'][i-1])

  nasdaq_df = nasdaq_df.assign(ratio=dif)

  nasdaq_df = nasdaq_df.drop([0], axis = 0) # 인덱스 0 은 삭제

  nasdaq_df['ratio'].dtype
  nasdaq_df['ratio']=nasdaq_df['ratio'].astype(float)

  # round - 3번째자리까지 반올림
  nasdaq_df['ratio']=round(nasdaq_df['ratio'], 3)

  nasdaq_df.drop(['open', 'high', 'low', 'close', 'adj_close', 'volume'], axis=1, inplace=True)

  # 나스닥 지수 전처리
  dic_date , dic_ratio  = nasdaq_df.to_dict()['date'].values() , nasdaq_df.to_dict()['ratio'].values() 

  nasdaq_score = defaultdict(lambda : '0.0')

  for a,b in zip(dic_date, dic_ratio):
    nasdaq_score[a] = b

# 기존 파일에 나스닥 컬럼 추가
  final_data['nasdaq_day'] = 0
  final_data['nasdaq_score'] = 0

  for i in range(len(final_data)):
      string = str(final_data.loc[i,'listed_date'])
      datetime_format = "%Y%m%d"

      datetime_result = (datetime.strptime(string, datetime_format).date()) # .date() -> 뒤에 초 제거
      datetime_result = str(datetime_result)
      # print(datetime_result) # start day

      while 1:
          before_day = get_before_day(datetime_result, 1)

          if before_day in nasdaq_score:
              final_data.loc[i,'nasdaq_score'] = nasdaq_score[before_day]
              final_data.loc[i,'nasdaq_day'] = before_day
              # print(before_day) # 과거날짜
              break
          else:
              datetime_result = before_day
          
  # data.rename(columns={'name':'기업명'}, inplace=True)
  final_data.drop(['Unnamed: 0'], axis=1, inplace=True)
  final_data.drop(['nasdaq_day'], axis=1, inplace=True)

  print(final_data)


  final_data.to_csv(BASE_DIR/'regression/after_prerpos_get_score.csv', encoding='utf-8-sig')


nasdaq_add()