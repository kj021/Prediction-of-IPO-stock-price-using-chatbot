from pathlib import Path
import pandas as pd
from bs4 import BeautifulSoup as bs
import urllib.request as ur
import numpy as np
import re
import aiohttp
import asyncio
import time


BASE_DIR = Path(__file__).resolve().parent

def crawling_38_day(BASE_DIR):
    async def fetcher(session, url):

        global df
        global base_url

        async with session.get(url) as response:
            # print(url)
            html =  await response.content.read()


            df_dic = {'cor_name': [], 'sales': [], 'profit': [], 'shares_to_pub':[], 'exp_offer_price':[], 'sub_rate':[], 'offer_price':[], 'pre_demand_day':[],'subs_day':[] } # 0802 뉴스 기사 크롤링을 위한 청약일, 예측일 추가


            cor_soup = bs(html,"html.parser")


            info_table = cor_soup.find('table',summary='기업개요')
            if info_table is None:
                
                pass
            else:
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

                df_dic['cor_name'].append(기업명)
                df_dic['sales'].append(매출액)
                df_dic['profit'].append(순이익)
                df_dic['shares_to_pub'].append(구주매출)
                df_dic['exp_offer_price'].append(희망공모가액)
                df_dic['sub_rate'].append(청약경쟁률)
              
                df_dic['pre_demand_day'].append(수요예측일)
                df_dic['subs_day'].append(청약일)          

            return df_dic


    async def main():
        
        urls = []

        for p in range(1,1+1): # page num
            page = f'index.htm?o=r1&page={p}'
            html = ur.urlopen(base_url+page)
            soup = bs(html.read(), "html.parser")
            for menu in soup.find_all('a','menu'):
                cor_url = base_url + menu['href'][2:]
                urls.append(cor_url)

        connector = aiohttp.TCPConnector(force_close=True,limit=60)
        async with aiohttp.ClientSession(connector=connector) as session:
            result = await asyncio.gather(*[fetcher(session, url) for url in urls])

        return result

    base_url = 'http://www.38.co.kr/html/fund/'

    start = time.time()
    answer = asyncio.run(main())

    dic = {'cor_name': [], 'sales': [], 'profit': [], 'shares_to_pub':[], 'exp_offer_price':[], 'sub_rate':[], 'pre_demand_day':[],'subs_day':[] }

    for d in answer:
        
        if len(d['cor_name'])==0:
            continue
        
        if '스팩' in d['cor_name'][0]:
            continue

        dic['cor_name'].append(d['cor_name'][0])
        dic['sales'].append(d['sales'][0])
        dic['profit'].append(d['profit'][0])
        dic['shares_to_pub'].append(d['shares_to_pub'][0])
        dic['exp_offer_price'].append(d['exp_offer_price'][0])
        dic['sub_rate'].append(d['sub_rate'][0])
        dic['pre_demand_day'].append(d['pre_demand_day'][0])
        dic['subs_day'].append(d['subs_day'][0])
       

    pd.DataFrame(dic).to_csv(BASE_DIR/'Crawling/crawling_add.csv',encoding='utf-8-sig')
    end = time.time()

    print("crawling_add.csv done.")
