
# https://docs.aiohttp.org/en/stable/
# pip install aiohttp~=3.7.3

import time
import pandas as pd
from bs4 import BeautifulSoup as bs
import urllib.request as ur
import urllib
import tqdm
import asyncio
import aiohttp
from pathlib import Path
from datetime import datetime, timedelta


BASE_DIR = Path(__file__).resolve().parent.parent

def get_next_day(string):
    date = datetime.strptime(string, '%Y-%m-%d')
    after_one_day = date + timedelta(days=1)
    if after_one_day.month<10:
        month =  '0'+str(after_one_day.month)
    else:
        month = str(after_one_day.month)

    if after_one_day.day<10:

        day =  '0'+str(after_one_day.day)
    else:

        day = str(after_one_day.day)
        
    after_day = str(after_one_day.year)+'.'+month+'.'+day
    return after_day


def search_news_url(word,ds):


    url_list = []

    keyword = urllib.parse.quote_plus(word)

    for i in range(7+1):
        
        base_url = f'https://search.naver.com/search.naver?where=news&query={keyword}&sm=tab_opt&sort=0&photo=0&field=0&pd=3&ds={ds}&de={ds}&start=1'
        url_list.append([word,base_url])

        ds = get_next_day(ds.replace('.','-'))

    return url_list



async def fetch(session, name , url):
    global df 
    dic = {}
    dic['기업명'] = []
    dic['제목'] = []

    async with session.get(url) as response:
        html = await response.text()
        soup = bs(html,"html.parser")
        title_url = soup.select('a.news_tit')

        for tit in title_url:

            dic['기업명'].append(name)
            title = tit.text
            dic['제목'].append(title)
    df = pd.concat([df,pd.DataFrame(dic)])


async def main():

    global df

    day_38 = pd.read_csv(BASE_DIR/'Data_Preprocessing/38_day.csv',encoding = 'euc-kr') 
    refined_data = pd.read_csv(BASE_DIR/'Data_Preprocessing/refined_data_초기파일.csv')
    merge_data = refined_data.merge(day_38,on='기업명')

    merge_data = merge_data[['기업명','수요예측일','청약일']]

    length = len(merge_data) # time out 이 발생하여 100개식 잘라서 진행 

    # num = length//100


    # for k in range(1,num+1):
    #     print(k)
    urls = []

    s = time.time()
    for i in tqdm.tqdm(range(length)):

        word = merge_data.iloc[i]['기업명']

        ds = merge_data.iloc[i]['수요예측일']
        url_list = search_news_url(word,ds)
        urls+=url_list

    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*[fetch(session, name, url) for name,url in urls])
        
            
            # result_df.to_csv(f'test_to_csv{k}.csv',encoding='utf-8-sig')

        
        # print('l time : ',time.time()-s)

    df.to_csv('news_title.csv',encoding='utf-8-sig')

if __name__ == '__main__':

    df = pd.DataFrame(
        columns=[
            "기업명",
            "제목",
        ]
    )
    start_time = time.time()
    asyncio.run(main())
    print('learning time : ',time.time()-start_time)

