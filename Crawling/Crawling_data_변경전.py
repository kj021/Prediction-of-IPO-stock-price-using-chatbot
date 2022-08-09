# http://www.38.co.kr/html/fund/index.htm?o=nw&page=1   리스트만 쭉 뽑음
from pathlib import Path
import urllib.request as ur
import requests, re, time
from bs4 import BeautifulSoup as bs
from collections import defaultdict
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent


def crawling_data(BASE_DIR):
    url = 'http://www.38.co.kr/html/fund/index.htm?o=nw&page='  # 전체 리스트화면 url
    url2 = 'http://www.38.co.kr/chart/chart_page_new.php3?code='  # 개별 장외종가 url

    dics = defaultdict(list)
    for n in range(1, 1 + 1):

        temp = url + str(n)
        html = ur.urlopen(temp)
        temp = bs(html.read(), "html.parser")

        temp = temp.find('table', {'summary': '신규상장종목'})

        trs = temp.find_all('tr')
        # print(f'페이지 {n}')
        dics_page = {}
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
                dics['name'].append(name)  # 회사이름
                dics['type'].append(type)  # 시장종류
                dics['day'].append(td_list[1].replace('/', ''))  # 상장일
                dics['now_p'].append(td_list[2].replace(',', ''))  # 현재가
                dics['gongmo_p'].append(td_list[4].replace(',', ''))  # 공모가
                dics['sicho_p'].append(td_list[6].replace(',', ''))  # 시초가
                dics['first_p'].append(td_list[8].replace(',', ''))  # 첫날 종가

                if dics['sicho_p'] in ['-']:
                    raise Exception('데이터 없음')

                corp_cd = re.search("(?←\=)\d*$", tds[-1].find('a')['href'])[0]
                dics['corp_cd'].append(corp_cd)  # 종목코드
            except:
                pass
        time.sleep(5)

    df = pd.DataFrame(dics)
    print(df)
    df.to_csv(BASE_DIR / 'data.csv')

crawling_data(BASE_DIR)