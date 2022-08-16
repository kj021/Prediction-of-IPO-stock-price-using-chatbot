from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
def crawling_38_basic_info(BASE_DIR):
    import aiohttp
    import asyncio
    import time
    import pandas as pd
    from bs4 import BeautifulSoup as bs
    import urllib.request as ur
    import numpy as np


    async def fetcher(session, url):

        global df
        global base_url
        
        async with session.get(url) as response:

            html =  await response.content.read()
            
            soup = bs(html,"html.parser")

            df_dic = {}
            df_dic['cor_name'] = []
            df_dic['cor_rate'] = []
            df_dic['obligation'] = []

            cor_soup = bs(html,"html.parser")
            
            
            info_table = cor_soup.find('table',summary='기업개요')
            if info_table is None:
                # un_search.append(cor_url)
                pass
            else:
                bids_table = cor_soup.find('table',summary='공모정보')
                table = cor_soup.find('table',summary='공모청약일정')
                sub_table = table.find_all('tr')
                
                기업명 = info_table.find('td',bgcolor='#FFFFFF').text.split()[0]
                수요예측일 = ''.join(sub_table[0].find('td',colspan=3).text.split())
                공모청약일 = ''.join(sub_table[1].find('td',colspan=3).text.split())
                확정공모가 = ''.join(sub_table[6].find('td',bgcolor='#FFFFFF').text.split())
                
                if len(sub_table) == 22:
                
                    경쟁률  = sub_table[-3].text.split()[1]
                    의무보유확약 = sub_table[-3].text.split()[-1]
                else:
                    경쟁률  = sub_table[-1].text.split()[1]
                    의무보유확약 = sub_table[-1].text.split()[-1]
                    
                if 경쟁률 == '의무보유확약':
                    경쟁률 = np.nan

                df_dic['cor_name'].append(기업명)
                df_dic['cor_rate'].append(경쟁률)
                df_dic['obligation'].append(의무보유확약)


            
            return df_dic


    async def main():

        base_url = 'http://www.38.co.kr/html/fund/'
        urls = []

        for p in range(1,54+1): # page num
            page = f'index.htm?o=r1&page={p}'
            html = ur.urlopen(base_url+page)
            soup = bs(html.read(), "html.parser")
            for menu in soup.find_all('a','menu'):
                
                cor_url = base_url + menu['href'][2:]
                # print(cor_url)
                urls.append(cor_url)
        connector = aiohttp.TCPConnector(force_close=True)
        async with aiohttp.ClientSession(connector=connector) as session:
            result = await asyncio.gather(*[fetcher(session, url) for url in urls])

        return result

    dic = {}
    dic['cor_name'] = []
    dic['cor_rate'] = []
    dic['obligation'] = []

    

    start = time.time()
    answer = asyncio.run(main())


    for d in answer:
        try:
            dic['cor_name'].append(d['cor_name'][0])
            dic['cor_rate'].append(d['cor_rate'][0])
            dic['obligation'].append(d['obligation'][0])
        except:
            pass


    pd.DataFrame(dic).to_csv(BASE_DIR/"Crawling/crawling_38com_53.csv",encoding='utf-8-sig')
    end = time.time()
    print(end-start)
    print('crawling_38com.csv done.')


        
    
