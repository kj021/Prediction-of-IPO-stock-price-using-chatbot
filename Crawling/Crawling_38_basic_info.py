
# def crawling_38_basic_info(BASE_DIR):
#     import time
#     import pandas as pd
#     from bs4 import BeautifulSoup as bs
#     import urllib.request as ur
#     import numpy as np

#     df_dic = {}
#     df_dic['기업명'] = []
#     df_dic['경쟁률'] = []
#     df_dic['의무보유확약'] = []


#     for p in range(1,70+1): # page num
        
#         base_url = 'http://www.38.co.kr/html/fund/'
#         page = f'index.htm?o=r1&page={p}'
#         html = ur.urlopen(base_url+page)
#         soup = bs(html.read(), "html.parser")
#         for menu in soup.find_all('a','menu'):
            
#             cor_url = base_url + menu['href'][2:]
    
#             cor_html = ur.urlopen(cor_url)
#             cor_soup = bs(cor_html.read(), "html.parser")
            
#             info_table = cor_soup.find('table',summary='기업개요')
#             if info_table is None:
#                 # un_search.append(cor_url)
#                 continue
#             bids_table = cor_soup.find('table',summary='공모정보')
#             table = cor_soup.find('table',summary='공모청약일정')
#             sub_table = table.find_all('tr')
            
#             기업명 = info_table.find('td',bgcolor='#FFFFFF').text.split()[0]
#             수요예측일 = ''.join(sub_table[0].find('td',colspan=3).text.split())
#             공모청약일 = ''.join(sub_table[1].find('td',colspan=3).text.split())
#             확정공모가 = ''.join(sub_table[6].find('td',bgcolor='#FFFFFF').text.split())
            
#             if len(sub_table) == 22:
            
#                 경쟁률  = sub_table[-3].text.split()[1]
#                 의무보유확약 = sub_table[-3].text.split()[-1]
#             else:
#                 경쟁률  = sub_table[-1].text.split()[1]
#                 의무보유확약 = sub_table[-1].text.split()[-1]
#             if 경쟁률 == '의무보유확약':
#                 경쟁률 = np.nan

#             df_dic['기업명'].append(기업명)
#             df_dic['경쟁률'].append(경쟁률)
#             df_dic['의무보유확약'].append(의무보유확약)

#     df = pd.DataFrame(df_dic)
#     df.reset_index(drop=True).to_csv(BASE_DIR/'crawling_38com.csv')
            
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
            # print(url)
            html =  await response.content.read()

            soup = bs(html,"html.parser")

            df_dic = {}
            df_dic['기업명'] = []
            df_dic['경쟁률'] = []
            df_dic['의무보유확약'] = []

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

                df_dic['기업명'].append(기업명)
                df_dic['경쟁률'].append(경쟁률)
                df_dic['의무보유확약'].append(의무보유확약)


            
            return df_dic


    async def main():
        
        urls = []

        for p in range(1,70+1): # page num
            page = f'index.htm?o=r1&page={p}'
            html = ur.urlopen(base_url+page)
            soup = bs(html.read(), "html.parser")
            for menu in soup.find_all('a','menu'):
                cor_url = base_url + menu['href'][2:]
                urls.append(cor_url)

        async with aiohttp.ClientSession() as session:
            result = await asyncio.gather(*[fetcher(session, url) for url in urls])

        return result

    dic = {}
    dic['기업명'] = []
    dic['경쟁률'] = []
    dic['의무보유확약'] = []

    base_url = 'http://www.38.co.kr/html/fund/'

    start = time.time()
    answer = asyncio.run(main())

    for d in answer:
        dic['기업명'].append(d['기업명'][0])
        dic['경쟁률'].append(d['경쟁률'][0])
        dic['의무보유확약'].append(d['의무보유확약'][0])
    

    pd.DataFrame(dic).to_csv(BASE_DIR/'crawling_38com.csv',encoding='utf-8-sig')
    end = time.time()

    print("crawling_38com.csv done.")


        
    

