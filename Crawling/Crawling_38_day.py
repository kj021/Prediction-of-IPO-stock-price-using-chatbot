from pathlib import Path
import pandas as pd
from bs4 import BeautifulSoup as bs
import urllib.request as ur
import numpy as np
import telegram
# from telegram_bot.config import api_key,chat_id
# from database.stock import StockModel
from pymongo import MongoClient
# from database.config import MONGO_DB_NAME
from glob import glob
import re

BASE_DIR = Path(__file__).resolve().parent

def crawling_38_day(BASE_DIR):

  un_search = []

  df_dic = {'기업명': [], '매출액': [], '순이익': [], '구주매출':[], '희망공모가액':[], '청약경쟁률':[], '확정공모가':[], '수요예측일':[],'청약일':[] } # 0802 뉴스 기사 크롤링을 위한 청약일, 예측일 추가

  for p in range(1,70+1): # page num
      base_url = 'http://www.38.co.kr/html/fund/'
      page = f'index.htm?o=r1&page={p}'
      html = ur.urlopen(base_url+page)
      soup = bs(html.read(), "html.parser")

      for menu in soup.find_all('a','menu'):

          cor_url = base_url + menu['href'][2:]
          #print(cor_url)
          cor_html = ur.urlopen(cor_url)
          cor_soup = bs(cor_html.read(), "html.parser")

          info_table = cor_soup.find('table',summary='기업개요')
          if info_table is None:
              un_search.append(cor_url)
              continue
          bids_table = cor_soup.find('table',summary='공모정보')
          table = cor_soup.find('table',summary='공모청약일정')
          sub_table = table.find_all('tr')

          # 기업개요
          기업명 = info_table.find('td',bgcolor='#FFFFFF').text.split()[0]

          trs = info_table.find_all('tr')

          for tr in trs:
              if tr==trs[7]:
                  tds = tr.find_all('td')
                  for td in tds:
                      매출액=tds[1].text.replace(u'\xa0',u'')
              elif tr==trs[8]:
                  tds=tr.find_all('td')
                  for td in tds:
                      순이익 = tds[1].text.replace(u'\xa0',u'')
          # 공모 정보
          trs = bids_table.find_all('tr')

          for tr in trs:
              if tr==trs[1]:
                  tds=tr.find_all('td')
                  for td in tds:
                      구주매출=tds[1].text.replace(u'\xa0',u'')

              if tr==trs[2]:
                  tds=tr.find_all('td')
                  for td in tds:
                      희망공모가액=tds[1].text.replace(u'\xa0',u'')
                      청약경쟁률 = tds[3].text.replace(u'\xa0',u'')

          확정공모가 = ''.join(sub_table[6].find('td', bgcolor='#FFFFFF').text.split())
          # 다영 코드 추가 (8월 1일)
          수요예측기간=''.join(sub_table[0].find('td',bgcolor="#FFFFFF").text.split())
          수요예측기간=re.split('~', 수요예측기간)
          수요예측일=수요예측기간[0] 
          청약기간 = ''.join(sub_table[1].find('td', bgcolor="#FFFFFF").text.split())
          청약기간=re.split('~', 청약기간)
          청약일=청약기간[1] # 2022.07.26~2022.07.27 중 뒤에 날짜만 가져옴



          df_dic['기업명'].append(기업명)
          df_dic['매출액'].append(매출액)
          df_dic['순이익'].append(순이익)
          df_dic['구주매출'].append(구주매출)
          df_dic['희망공모가액'].append(희망공모가액)
          df_dic['청약경쟁률'].append(청약경쟁률)
          df_dic['확정공모가'].append(확정공모가)
          df_dic['수요예측일'].append(수요예측일)
          df_dic['청약일'].append(청약일)          


  df=pd.DataFrame(df_dic, columns=('기업명','수요예측일','청약일'))
  df.to_csv(BASE_DIR/'38_day.csv', encoding='cp949')
  



crawling_38_add(BASE_DIR)