#from PyNaver import Datalab
import pandas as pd
import urllib.request
from datetime import datetime, timedelta
import json
import sys
import os
import warnings
import re
warnings.filterwarnings(action='ignore')

class NaverDataLabOpenAPI():
    """
    네이버 데이터랩 오픈 API 컨트롤러 클래스
    """
    def __init__(self, client_id, client_secret):
        """
        인증키 설정 및 검색어 그룹 초기화
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.keywordGroups = []
        self.url = "https://openapi.naver.com/v1/datalab/search"
    def add_keyword_groups(self, group_dict):
        """
        검색어 그룹 추가
        """
        keyword_gorup = {
            'groupName': group_dict['groupName'],#기업명 
            'keywords': group_dict['keywords'] #기업명 
        }
        
        self.keywordGroups.append(keyword_gorup)
        #print(f">>> Num of keywordGroups: {len(self.keywordGroups)}")
        
    def get_data(self, startDate, endDate, timeUnit, device, ages, gender):
        """
        요청 결과 반환
        timeUnit - 'date', 'week', 'month'
        device - None, 'pc', 'mo'
        ages = [], ['1' ~ '11']
        gender = None, 'm', 'f'
        """
        # Request body
        body = json.dumps({
            "startDate": startDate,
            "endDate": endDate,
            "timeUnit": timeUnit,
            "keywordGroups": self.keywordGroups,
            "device": device,
            "ages": ages,
            "gender": gender
        }, ensure_ascii=False)
        
        # Results
        request = urllib.request.Request(self.url)
        request.add_header("X-Naver-Client-Id",self.client_id)
        request.add_header("X-Naver-Client-Secret",self.client_secret)
        request.add_header("Content-Type","application/json")
        response = urllib.request.urlopen(request, data=body.encode("utf-8"))
        rescode = response.getcode()
        if(rescode==200):
            # Json Result
            result = json.loads(response.read())
            
            df = pd.DataFrame(result['results'][0]['data'])[['period']]
            for i in range(len(self.keywordGroups)):
                #df['period'] = df.apply(lambda r: [df['period'].values], axis=1, result_type='expand')
                tmp = pd.DataFrame(result['results'][i]['data'])
                tmp = tmp.rename(columns={'ratio': result['results'][i]['title']})
                df = pd.merge(df, tmp, how='left', on=['period'])
            self.df = df.rename(columns={'period': '날짜'})
            self.df['날짜'] = pd.to_datetime(self.df['날짜'])
            
        else:
            print("Error Code:" + rescode)
            
        return self.df


def main_search_amt(total_df):
    # API 인증 정보 설정
    client_id = "bcTwytF3s0lVKpYJEX_H"
    client_secret = "lXd0IXhpxb"
    days = total_df[['cor_name','subs_day']]
    days['subs_day'] = pd.to_datetime(days['subs_day'])
    df = pd.DataFrame(
            columns=[
                '날짜',
                "cor_name",
                "검색량",
            ]
        )

    df = pd.DataFrame(columns=[''])
    for i in range(len(days['subs_day'])):

        name = days['cor_name'][i]
     
        sub_date = str(days['subs_day'][i].date())
        day_before = str(days['subs_day'][i].date() - timedelta(days=1))

            
        keyword_group_set = {
        'keyword_group_1': {'groupName': '검색량', 'keywords': [name]}
                        }
        # 요청 파라미터 설정
        startDate = day_before
        endDate = sub_date
        timeUnit = 'date'
        device = ''
        ages = []
        gender = ''

    # 데이터 프레임 정의
        naver = NaverDataLabOpenAPI(client_id=client_id, client_secret=client_secret)

        naver.add_keyword_groups(keyword_group_set['keyword_group_1'])


        temp_df = naver.get_data(startDate, endDate, timeUnit, device, ages, gender)
        temp_df['cor_name'] = name

        df = pd.concat([df,temp_df])

    del df['']

    df.reset_index(drop=True,inplace=True)


    #최근 8일동안 검색량 
    client_id = "Wz_krysqKlKEn0ibIiIa"
    client_secret = "B9DQ4dvfQ3"
    ratio = pd.DataFrame(
            columns=[
                'date',
                "cor_name",
                "기업검색량",
            ]
        )

    for i in range(len(days['subs_day'])):
        
        
        name = days['cor_name'][i]
        curr_day = days['subs_day'][i].date()

        recent_8_days = str(curr_day - timedelta(weeks=1,days=1))
        
    #     print(recent_8_days)
        
        url = "https://openapi.naver.com/v1/datalab/search"
        body = "{\"startDate\":\""+recent_8_days+"\",\"endDate\":\""+curr_day.strftime("%Y-%m-%d")+"\",\"timeUnit\":\"date\",\"keywordGroups\":[{\"groupName\":\""+name+"\",\"keywords\":[\""+name+"\"]}]}";
        requested = urllib.request.Request(url)
        requested.add_header("X-Naver-Client-Id", client_id)
        requested.add_header("X-Naver-Client-Secret", client_secret)
        requested.add_header("Content-Type", "application/json")
        response = urllib.request.urlopen(requested, data=body.encode("utf-8"))
        rescode = response.getcode()


        response_body = response.read()
        output_data = response_body.decode('utf-8')



        result = json.loads(output_data)

        date = [a['period'] for a in result['results'][0]['data']]
        corp_ratio = [a['ratio'] for a in result['results'][0]['data']]
        temp_ratio = pd.DataFrame({'date':date, 
                    '기업검색량':corp_ratio,
                    'cor_name':name})

        ratio = pd.concat([ratio,temp_ratio])
        
    ratio.reset_index(drop=True,inplace=True)

    for i in range(days.shape[0]):
        cn = days.loc[i,'cor_name']

        days.loc[i,['청약일검색량']] = df.groupby('cor_name').mean().loc[cn,'검색량']

    
    for i in range(days.shape[0]):
        cn = days.loc[i,'cor_name']
        days.loc[i,['최근일주일검색량']] = ratio.groupby('cor_name').median().loc[cn,'기업검색량']
        
    import math
    score_list = []
    for i in range(len(days['청약일검색량'])):
        sub_search_amt = round(days['청약일검색량'][i],3)
        weekly_search_amt = round(days['최근일주일검색량'][i],3)
        score = math.log10(sub_search_amt) - math.log10(weekly_search_amt)
        score_list.append(score)
    days = days.assign(비정상검색량지수 = score_list)
    days['비정상검색량지수'] = round(days['비정상검색량지수'],3)
    days = days.dropna(axis=0).reset_index(drop=True)
    days.drop(['청약일검색량','최근일주일검색량'], axis = 1,inplace = True)
    
    days.rename(columns={"비정상검색량지수": "search_amt"},inplace=True)

    days = days[['cor_name','search_amt']]

    total_df = total_df.merge(days,on=['cor_name'])
    print(total_df.columns)
    return total_df
