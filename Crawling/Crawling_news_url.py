
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


BASE_DIR = Path(__file__).resolve().parent

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
    
    dic = {}
    dic['cor_name'] = []
    dic['title'] = []

    async with session.get(url) as response:
        html = await response.text()
        soup = bs(html,"html.parser")
        title_url = soup.select('a.news_tit')

        for tit in title_url:

            dic['cor_name'].append(name)
            title = tit.text
            dic['title'].append(title)
        return dic


async def news_main(df):

    merge_data = pd.read_csv(BASE_DIR/'after_prepros.csv')
    

    merge_data = merge_data[['cor_name','pre_demand_day','subs_day']]

    length = len(merge_data) 

    urls = []

    s = time.time()
    for i in tqdm.tqdm(range(length)):

        word = merge_data.iloc[i]['cor_name']

        ds = merge_data.iloc[i]['pre_demand_day']
        url_list = search_news_url(word,ds)
        urls+=url_list

    async with aiohttp.ClientSession() as session:
        result = await asyncio.gather(*[fetch(session, name, url) for name,url in urls])
        
        for dic in result:

            df = pd.concat([df,pd.DataFrame(dic)])

        
        # print('l time : ',time.time()-s)

    df.to_csv(BASE_DIR/'news_title.csv',encoding='utf-8-sig')

# if __name__ == '__main__':

#     df = pd.DataFrame(
#         columns=[
#             "cor_name",
#             "title",
#         ]
#     )
#     start_time = time.time()
#     asyncio.run(news_main())
#     print('learning time : ',time.time()-start_time)

