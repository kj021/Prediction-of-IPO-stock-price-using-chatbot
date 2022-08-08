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

def crawling_38_add(BASE_DIR):
  
    async def fetcher(session, url):

        global df
        global base_url

        async with session.get(url) as response:
            # print(url)
            html =  await response.content.read()
                      
            df_dic = {'기업명': [], '매출액': [], '순이익': [], '구주매출':[], '희망공모가액':[], '청약경쟁률':[], '확정공모가':[]}

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


              df_dic['기업명'].append(기업명)
              df_dic['매출액'].append(매출액)
              df_dic['순이익'].append(순이익)
              df_dic['구주매출'].append(구주매출)
              df_dic['희망공모가액'].append(희망공모가액)
              df_dic['청약경쟁률'].append(청약경쟁률)
              df_dic['확정공모가'].append(확정공모가)  

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


        async with aiohttp.ClientSession() as session:
            result = await asyncio.gather(*[fetcher(session, url) for url in urls])

        return result

    base_url = 'http://www.38.co.kr/html/fund/'

    start = time.time()
    answer = asyncio.run(main())

    dic = {'기업명': [], '매출액': [], '순이익': [], '구주매출':[], '희망공모가액':[], '청약경쟁률':[], '확정공모가':[]}

    for d in answer:
        dic['기업명'].append(d['기업명'][0])
        dic['매출액'].append(d['매출액'][0])
        dic['순이익'].append(d['순이익'][0])
        dic['구주매출'].append(d['구주매출'][0])
        dic['희망공모가액'].append(d['희망공모가액'][0])
        dic['청약경쟁률'].append(d['청약경쟁률'][0])
        dic['확정공모가'].append(d['확정공모가'][0])       

    pd.DataFrame(dic).to_csv('38_add_variable.csv',encoding='utf-8-sig')
    end = time.time()

    print("38_add_variable.csv done.")