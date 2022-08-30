import pandas as pd
from bs4 import BeautifulSoup as bs
import urllib.request as ur
import numpy as np
from tqdm import tqdm
from datetime import datetime
from pytz  import timezone
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def Crawling_day_alarm():
    url='http://www.38.co.kr/html/fund/index.htm?o=k&page=1'


    html = ur.urlopen(url)
    soup = bs(html.read(), "html.parser")
    temp = soup.find('table', {'summary':'공모주 청약일정'})
    
    trs = temp.find_all('tr')[2:]
    list_compnay=[]
    
    for row in range(0,len(trs)):
        data_list = trs[row].text.replace('\xa0\xa0', '').split('\n')[1:-1]
        list_compnay.append(data_list[-2])

    trs = temp.find_all('tr')

    cor_name=[]
    link=[]
    for i1 in trs:
        tds = i1.find_all('td')
        for i2 in tds:
            tds2=i2.find_all('a')
            for i3 in tds2:
                cor_name.append(i3.text)
                link.append(i3.attrs['href'])
                
    i = len(cor_name) - 1 
    while i >= 0:
        if i % 2 == 1:  # 2로 나눈값이 1이면 홀수임
            del cor_name[i]
        i -= 1
        
    i = len(link) - 1 
    while i >= 0:
        if i % 2 == 0:  # 2로 나눈값이 1이면 홀수임
            del link[i]
        i -= 1
        
    for i in range(len(link)):
        link[i]='http://www.38.co.kr'+link[i]
        
    df=pd.DataFrame(cor_name,columns=['cor_name'])
    df['link']=link
    df['company']=list_compnay

    df = df[~df['cor_name'].str.contains('스팩')]
    df = df[~df['cor_name'].str.contains('리츠')]
    df.reset_index(inplace = True)
    df.drop('index',axis=1,inplace=True)

    search_link=[]
    for i in range(len(df)):
        search_link.append(df.iloc[i]['link'])

    list0=[]    
    list1=[]
    list2=[]
    list3=[]
    list4=[]
    list5=[]

    for row in tqdm(search_link):
        url=row
        html = ur.urlopen(url)
        soup = bs(html.read(), "html.parser")
        table = soup.find('table', {'summary': '공모청약일정'})
        tr = table.find_all('tr')[0:6]
        
        list_all=[]
        for i in tr:
            list_all.append(i.get_text().replace('\xa0', '').replace(' ', '').replace('\n','').replace('\t',''))
        
        list_all[0]=list_all[0].replace('주요일정','')
        list_all[2]=list_all[2].replace('(신문)','').replace('(주간사홈페이지참조)','')
        
        for i in range(len(list_all)):
            if i == 0:
                list0.append(list_all[i].split('일')[1])
            elif i == 1:
                list1.append(list_all[i].split('일')[1])
            elif i == 2:
                list2.append(list_all[i].split('일')[1])
            elif i == 3:
                list3.append(list_all[i].split('일')[1])
            elif i == 4:
                list4.append(list_all[i].split('일')[1])  
            elif i == 5:
                list5.append(list_all[i].split('일')[1])       

    list0_2=[]
    list0_1=[]
    list1_2=[]
    list1_1=[]

    for i in range(len(list0)):
        list0_2.append(list0[i].split('~')[1])
        list0_1.append(list0[i].split('~')[0])

    for i in range(len(list1)):
        list1_2.append(list0[i].split('~')[1])
        list1_1.append(list0[i].split('~')[0])

    df['수요예측일(1)']=list0_1
    df['수요예측일(2)']=list0_2
    df['공모청약일(1)']=list1_1
    df['공모청약일(2)']=list1_2
    df['배정공고일']=list2
    df['납입일']=list3
    df['환불일']=list4
    df['상장일']=list5
    
    df.to_csv(BASE_DIR/'Crawling/Crawling_ALL_day.csv',encoding='utf-8-sig')
    
    
    return df
   

def push_day_alarm(df):
    print("시작")
    # df=pd.read_csv("C:/Users/KHS/Desktop/Crawling_ALL_day.csv")
    # df.drop('Unnamed: 0',axis=1,inplace=True)
    # df.drop('link',axis=1,inplace=True)
    
    df['수요예측일(첫째날)'] = pd.to_datetime(df['수요예측일(1)'], format='%Y.%m.%d', errors='raise')
    df['수요예측일(둘째날)'] = pd.to_datetime(df['수요예측일(2)'], format='%Y.%m.%d', errors='raise')
    df['공모청약일(첫째날)'] = pd.to_datetime(df['공모청약일(1)'], format='%Y.%m.%d', errors='raise')
    df['공모청약일(둘째날)'] = pd.to_datetime(df['공모청약일(2)'], format='%Y.%m.%d', errors='raise')
    df['배정공고일'] = pd.to_datetime(df['배정공고일'], format='%Y.%m.%d', errors='raise')
    df['납입일'] = pd.to_datetime(df['납입일'], format='%Y.%m.%d', errors='raise')
    df['환불일'] = pd.to_datetime(df['환불일'], format='%Y.%m.%d', errors='raise')
    df['상장일'] = pd.to_datetime(df['상장일'], format='%Y.%m.%d', errors='raise')

    current_time = datetime.now(timezone('Asia/Seoul'))
    target_year=current_time.year
    target_month=current_time.month
    target_day=current_time.day 

    target_time=f"{target_year}년도 {target_month}월 {target_day}일"
    
    list_target=['수요예측일(첫째날)','수요예측일(둘째날)','공모청약일(첫째날)','공모청약일(둘째날)','배정공고일','납입일','환불일','상장일']

    count_number=[]
    count_row=[]
    count_company=[]
    count_Link=[]
    for i in range(len(df)):
        for row in list_target:
            if target_year==df.iloc[i][row].year:
                if target_month==df.iloc[i][row].month:
                    if target_day==df.iloc[i][row].day:
                        print(df.iloc[i]['cor_name'],row)
                        count_number.append(df.iloc[i]['cor_name'])
                        count_company.append(df.iloc[i]['company'])
                        count_Link.append(df.iloc[i]['link'])
                        count_row.append(row)
    
    Text=[]
    
    for i in range(len(count_number)):
        if count_number[i]!=count_number[i-1]:
            data='\n→ 기업명 : ['+count_number[i]+']('+count_Link[i]+')\n\n주간사 :'+count_company[i]+'\n\n'+count_row[i]+' 입니다!' 
            Text.append(data)
        elif len(count_number) == 1:
            data='\n→ 기업명 : ['+count_number[i]+']('+count_Link[i]+')\n\n주간사 :'+count_company[i]+'\n\n'+count_row[i]+' 입니다!'
            Text.append(data)
        else:
            data=count_row[i]+' 입니다!'
            print(data)
            Text.append(data)


    result_Text = "\n".join(Text)
        
    # print(result_Text)
    
    if result_Text=='':
        print(f"<오늘의 공모주 일정정보>\n\n일정: {target_time}\n\n일정이 없습니다!\n")
    else:
        print(f"<오늘의 공모주 일정정보>\n\n일정: {target_time}\n{result_Text}")
        

    return result_Text,target_time
    
    
# push_day_alarm()


       