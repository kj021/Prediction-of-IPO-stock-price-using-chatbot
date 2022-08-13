def preprocessing():
    from pathlib import Path



    BASE_DIR = Path(__file__).resolve().parent
    import pandas as pd
    import numpy as np
    import warnings
    warnings.filterwarnings(action='ignore')

    df1 = pd.read_csv(BASE_DIR/'crawling_38com.csv')
    del df1['Unnamed: 0']

    df2 = pd.read_csv(BASE_DIR/'data.csv')
    del df2['Unnamed: 0']
    # del df2['offer_price_y'] # 중복 크롤링 해버림 ㄲㅂ ㅠ

    df3 = pd.read_csv(BASE_DIR/'crawling_add.csv')
    del df3['Unnamed: 0']

    for i in range(len(df2.index)):
        df2.loc[i,'cor_name'] =df2.loc[i,'cor_name'].replace('(유가)','')

    df = df1.merge(df2,on='cor_name').merge(df3,on='cor_name')

    for i in range(df.shape[0]):
        per = df.loc[i,'obligation'].split('%')[0]
        if float(per)== 0:
            df.loc[i,'obligation'] = np.nan
        else:
            df.loc[i,'obligation'] = float(per)
    df.replace('(:1|%|,|:)','',regex = True, inplace= True)
    df.replace('(,|~)','',regex = True, inplace= True)
    df.replace("\(.*\)|\ㄴ-\ㄴ.*",'',regex = True,inplace=True)

    df = df[~df['cor_name'].str.contains('스팩')]
    df = df[~df['cor_name'].str.contains('리츠')]
    df = df.dropna(subset=['cor_rate']) # 기관 경쟁률 

    df = df.reset_index(drop=True)

    import re
    regex = "\(.*\)|\s-\s.*" 
    for i in range(len(df)):
        df['sales'][i] = re.sub(regex,'',df['sales'][i])
    for i in range(len(df)):
        df['profit'][i] = re.sub(regex,'',df['profit'][i])
        
    df = df[df['exp_offer_price'] != '- ~ - 원']

    df['l_exp_offer_price'] = df['exp_offer_price']
    df['h_exp_offer_price'] = df['exp_offer_price']

    df.drop('exp_offer_price',axis = 1,inplace = True) # 희망공모가 
    for i in range(df.shape[0]):
        df.loc[i,'h_exp_offer_price'] = df.loc[i,'h_exp_offer_price'].split()[1]
        df.loc[i,'l_exp_offer_price'] = df.loc[i,'l_exp_offer_price'].split()[0]

    df = df.dropna(subset=['obligation']).reset_index(drop=True) # 의무보유확약 

    df['market_type'] = df['market_type'].replace(['kosdaq','kospi'],[0,1])    
    df['pre_demand_day'] = df['pre_demand_day'].str.replace('.','-')  
    df['subs_day'] = df['subs_day'].str.replace('.','-')  

    df.loc[df['shares_to_pub'].str.contains('구주')==False, 'shares_to_pub'] = 1
    # import re 
    for i in range(df.shape[0]):
        v = df.loc[i,'shares_to_pub']
        
        if v != 1:
            sinju,guju = v.split()[1],v.split()[-2]
            if sinju == '-':
                df.loc[i,'shares_to_pub'] = np.nan 
            else:
                sinju,guju = int(sinju),int(guju)
                df.loc[i,'shares_to_pub'] = round(sinju/(sinju+guju),2)

    df.dropna(subset=['shares_to_pub'],inplace=True) # 구주매출 

    df['sub_rate'] = df['sub_rate'].replace('  ',np.nan)
    df['sales'] = df['sales'].replace('',np.nan)   
    df = df.dropna(subset=['sub_rate','sales']) 
    df = df.reset_index(drop=True)

    df.to_csv(BASE_DIR/'after_prepros.csv',encoding='utf-8-sig')

    
