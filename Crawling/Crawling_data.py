#http://www.38.co.kr/html/fund/index.htm?o=nw&page=1   리스트만 쭉 뽑음
import aiohttp
import asyncio
import time
import pandas as pd
from bs4 import BeautifulSoup as bs
import urllib.request as ur
import numpy as np
from collections import defaultdict
import re

def crawling_data(BASE_DIR=None):
    
    url = 'http://www.38.co.kr/html/fund/index.htm?o=nw&page=' #전체 리스트화면 url
    

    dics = defaultdict(list)
    for n in range(1,70+1):
        
        temp = url+str(n)
        html = ur.urlopen(temp)
        temp = bs(html.read(), "html.parser")

        temp = temp.find('table', {'summary':'신규상장종목'})

        trs = temp.find_all('tr')
        # print(f'페이지 {n}')
        dics_page = {}
        for i in trs:
            td_list = []
            tds = i.find_all('td')
            for ii in tds:
                td_list.append(ii.text.replace('\xa0',''))

            try:
                #이름구간
                
                name = td_list[0]
                if not name:
                    continue
                type = ''#시장
                if bool(re.search('\(유가\)',name)): #코스피
                    type = 'kospi'
                    name.replace('(유가)','')
                else:
                    type = 'kosdaq'

                dics['cor_name'].append(name)  #회사이름
                dics['market_type'].append(type)  #시장종류
                dics['listed_date'].append(td_list[1].replace('/',''))  #상장일
                
                if not td_list[4].replace(',','') :
                    dics['offer_price'].append('not yet')
                else:
                    dics['offer_price'].append(td_list[4].replace(',',''))

                # print(td_list[6])
                dics['sicho_p'].append(td_list[6].replace(',', ''))  # 시초가
                dics['profit_percent'].append(td_list[7])

                if dics['sicho_p'] in ['-']:
                    raise Exception('데이터 없음')

            except:
                pass
        # time.sleep(5)
    # print(dics)
    df = pd.DataFrame(dics)
    df.to_csv('jiseop_test/data.csv')
crawling_data()