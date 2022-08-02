
import time
import pandas as pd
from bs4 import BeautifulSoup as bs
import urllib.request as ur
import numpy as np
import urllib
'''
word = 'lg에너지솔루션'
ds,de = '2020.10.04','2020.12.14'

'''
word = 'lg에너지솔루션'
ds,de = '2022.01.11','2022.01.18'

def search_news_url(word,ds,de):

    titles,urls = [],[]
    keyword = urllib.parse.quote_plus(word)
    for i in range(1,5+1):
        base_url = f'https://search.naver.com/search.naver?where=news&query={keyword}&sm=tab_opt&sort=0&photo=0&field=0&pd=3&ds={ds}&de={de}&start=1'
        
        html = ur.urlopen(base_url)
        soup = bs(html.read(), "html.parser")

        title_url = soup.select('a.news_tit')

        for tit in title_url:
            title,url = tit.text, tit['href']

            titles.append(title)
            urls.append(url)

    return titles,urls

titles,urls = search_news_url(word,ds,de)

dic = {}
dic['title'] = []
for i in titles:
    dic['title'].append(i)


print(dic)

pd.DataFrame(dic).to_csv('test_title.csv')