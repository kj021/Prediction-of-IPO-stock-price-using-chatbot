
def crawling_38_basic_info(BASE_DIR):
    import time
    import pandas as pd
    from bs4 import BeautifulSoup as bs
    import urllib.request as ur
    import numpy as np

    df_dic = {}
    df_dic['기업명'] = []
    df_dic['경쟁률'] = []
    df_dic['의무보유확약'] = []


    for p in range(1,70+1): # page num
        
        base_url = 'http://www.38.co.kr/html/fund/'
        page = f'index.htm?o=r1&page={p}'
        html = ur.urlopen(base_url+page)
        soup = bs(html.read(), "html.parser")
        for menu in soup.find_all('a','menu'):
            
            cor_url = base_url + menu['href'][2:]
    
            cor_html = ur.urlopen(cor_url)
            cor_soup = bs(cor_html.read(), "html.parser")
            
            info_table = cor_soup.find('table',summary='기업개요')
            if info_table is None:
                # un_search.append(cor_url)
                continue
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

    df = pd.DataFrame(df_dic)
    df.to_csv(BASE_DIR/'crawling_38com.csv')
            