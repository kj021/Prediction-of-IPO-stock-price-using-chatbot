#http://www.38.co.kr/html/fund/index.htm?o=nw&page=1   리스트만 쭉 뽑음
from pathlib import Path
import urllib.request as ur
import requests, re, time
from bs4 import BeautifulSoup as bs
from collections import defaultdict
import pandas as pd
import aiohttp
import asyncio
import time

BASE_DIR = Path(__file__).resolve().parent


def crawling_data(BASE_DIR):
    async def fetcher(session, url):
        global df
        global base_url

        async with session.get(url) as response:
            print(url)
            html = await response.content.read()

            df_dic = {'name': [], 'type': [], 'day': [], 'now_p': [], 'gongmo_p': [], 'sicho_p': [], 'first_p': [], 'corp_cd': []}

            cor_soup = bs(html, "html.parser")

            temp = cor_soup.select('table', {'summary': '신규상장종목'})

            if temp is None:
                pass
            else:
                trs = temp.find_all('tr')
                i = 1 # trs의 0번째 요소는 표제
                for i in trs:
                    td_list = []
                    tds = i.find_all('td')
                    for ii in tds:
                        td_list.append(ii.text.replace('\xa0', ''))

                    try:
                        # 이름구간
                        name = td_list[0]
                        if not name:
                            continue
                        type = ''  # 시장
                        if bool(re.search('\(유가\)', name)):  # 코스피
                            type = 'kospi'
                            name.replace('(유가)', '')
                        else:
                            type = 'kosdaq'
                        # print(name,type)
                        df_dic['name'].append(name)  # 회사이름
                        df_dic['type'].append(type)  # 시장종류
                        df_dic['day'].append(td_list[1].replace('/', ''))  # 상장일
                        df_dic['now_p'].append(td_list[2].replace(',', ''))  # 현재가
                        df_dic['gongmo_p'].append(td_list[4].replace(',', ''))  # 공모가
                        df_dic['sicho_p'].append(td_list[6].replace(',', ''))  # 시초가
                        df_dic['first_p'].append(td_list[8].replace(',', ''))  # 첫날 종가

                        if df_dic['sicho_p'] in ['-']:
                            raise Exception('데이터 없음')

                        corp_cd = re.search("(?←\=)\d*$", tds[-1].find('a')['href'])[0]
                        df_dic['corp_cd'].append(corp_cd)  # 종목코드
                    except:
                        pass

            return df_dic

    async def main():
        urls = []

        for p in range(1, 70 + 1):
            page = f'index.htm?o=nw&page={p}'
            page_url = base_url + page
            html = ur.urlopen(base_url + page)
            soup = bs(html.read(), "html.parser")

            urls.append(page_url)


        async with aiohttp.ClientSession() as session:
            result = await asyncio.gather(*[fetcher(session, url) for url in urls])
        return result

    base_url = 'http://www.38.co.kr/html/fund/'  # 전체 리스트화면 url

    start = time.time()
    answer = asyncio.run(main())

    dic = {'name': [], 'type': [], 'day': [], 'now_p': [], 'gongmo_p': [], 'sicho_p': [], 'first_p': [], 'corp_cd': []}

    for d in answer:
        dic['name'].append(d['name'])
        dic['type'].append(d['type'])
        dic['day'].append(d['day'])
        dic['now_p'].append(d['now_p'])
        dic['gongmo_p'].append(d['gongmo_p'])
        dic['sicho_p'].append(d['sicho_p'])
        dic['first_p'].append(d['first_p'])
        dic['corp_cd'].append(d['corp_cd'])


    pd.DataFrame(dic).to_csv('data.csv', encoding='utf-8-sig')
    end = time.time()

    print(end-start)

    print("data.csv done.")



crawling_data(BASE_DIR)
