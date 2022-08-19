import matplotlib.pyplot as plt
import pandas as pd
from io import BytesIO
from pymongo import MongoClient
from tkinter.font import BOLD
import matplotlib.pyplot as plt
import pandas as pd
from io import BytesIO
from pymongo import MongoClient
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from math import pi
from matplotlib.path import Path
from matplotlib.spines import Spine
from matplotlib.transforms import Affine2D



def get_graph(cor_name,cor_shape):
    
    client = MongoClient('localhost', 27017)
    db = client['Ipo2']

    
    plt.style.use('ggplot')
    plt.rc('font', family='NanumGothic')
    df = pd.DataFrame(db.inform.find({},{'_id':False}))	# 모든 데이터 조회
    
    if cor_shape=='경쟁률' or cor_shape== '1':
        cor_shape1='cor_rate'
        cor_shape='경쟁률'
        
    elif cor_shape=='의무보유확약' or cor_shape== '2':
        cor_shape1='obligation'
        cor_shape='의무보유확약'
        
    elif cor_shape=='공모가' or cor_shape== '3':
        cor_shape1='offer_price'
        cor_shape='공모가'
        
    elif cor_shape=='매출액' or cor_shape== '4':
        cor_shape1='sales'
        cor_shape='매출액'
        
    elif cor_shape=='순이익' or cor_shape== '5':
        cor_shape1='profit'   
        cor_shape='순이익'
                             
    df['순위']=df[cor_shape1].rank(method='min',ascending=False)
    df=df.sort_values(by=[cor_shape1])
    
    plt.plot(df['순위'],df[cor_shape1],color='black')
        
    x=df.loc[df['cor_name']==cor_name]['순위'].unique()
    y=df.loc[df['cor_name']==cor_name][cor_shape1].unique()
        
    plt.scatter(x,y,color='r',s=200,label=cor_name) 
    
    
    plt.title(cor_name +"  "+ cor_shape)
    plt.xlabel('순위',labelpad=1)
    plt.ylabel(cor_shape,labelpad=1)        
    plt.legend(loc="upper right")

    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    
    count=df['순위'].count()    
    rank_count=df.loc[df['cor_name']==cor_name]['순위'].unique()
    rank_count=int(rank_count)
    return buf,rank_count,count




def get2_graph(cor_name):
    
        
    client = MongoClient('localhost', 27017)
    db = client['Ipo2']
    
    df2 = pd.DataFrame(db.inform.find({},{'_id':False}))
    
    count=0
    Search_name=cor_name
    for i in range(len(df2)):
        if df2.iloc[i]['cor_name']==Search_name:
            count=i
            
    # 필요컬럼외 지우기
    df2.drop(['market_type'], axis = 1,inplace = True)
    df2.drop(['listed_date'], axis = 1,inplace = True)
    df2.drop(['sicho_p'], axis = 1,inplace = True)
    # df2.drop(['profit_percent'], axis = 1,inplace = True)
    df2.drop(['shares_to_pub'], axis = 1,inplace = True)
    # df2.drop(['sub_rate'], axis = 1,inplace = True)
    df2.drop(['pre_demand_day'], axis = 1,inplace = True)
    df2.drop(['subs_day'], axis = 1,inplace = True)
    df2.drop(['l_exp_offer_price'], axis = 1,inplace = True)
    df2.drop(['sicho_exp'], axis = 1,inplace = True)
    
    # TEXT
    df3=pd.DataFrame(df2)
    df3['경쟁률']=df2['cor_rate'].rank(method='min',ascending=False)
    df3['의무보유확약']=df2['obligation'].rank(method='min',ascending=False)
    df3['공모가']=df2['offer_price'].rank(method='min',ascending=False)
    df3['매출액']=df2['sales'].rank(method='min',ascending=False)
    df3['순이익']=df2['profit'].rank(method='min',ascending=False)
    
    data1=int(df3.iloc[count]['경쟁률'])
    data2=int(df3.iloc[count]['의무보유확약'])
    data3=int(df3.iloc[count]['공모가'])
    data4=int(df3.iloc[count]['매출액'])
    data5=int(df3.iloc[count]['순이익'])
    data_len=len(df2)
    
    
    print("데이터 랭크순")
    print(data1,data2,data3,data4,data5,data_len)
    
    
    


    #사용할 라벨
    labels = ['경쟁률','의무보유확약','공모가','매출액','순이익']
    num_labels = len(labels)

    angles = [x/float(num_labels)*(2*pi) for x in range(num_labels)]
    angles += angles[:1]

    my_palette = plt.cm.get_cmap("Set2", len(df2.index))
    my_palette

    fig = plt.figure(figsize=(8,8))
    fig.set_facecolor('white')


    df2['경쟁률']=df2['cor_rate'].rank(method='min',ascending=True)
    df2['의무보유확약']=df2['obligation'].rank(method='min',ascending=True)
    df2['공모가']=df2['offer_price'].rank(method='min',ascending=True)
    df2['매출액']=df2['sales'].rank(method='min',ascending=True)
    df2['순이익']=df2['profit'].rank(method='min',ascending=True)
    # df2['희망공모가(상단)']=df2['h_exp_offer_price'].rank(method='min',ascending=False)

    df2.drop(['cor_rate'], axis = 1,inplace = True)
    df2.drop(['obligation'], axis = 1,inplace = True)
    df2.drop(['offer_price'], axis = 1,inplace = True)
    df2.drop(['profit_percent'], axis = 1,inplace = True)
    df2.drop(['sales'], axis = 1,inplace = True)
    df2.drop(['sub_rate'], axis = 1,inplace = True)
    df2.drop(['profit'], axis = 1,inplace = True)
    df2.drop(['h_exp_offer_price'], axis = 1,inplace = True)
    
    df2['경쟁률비율']=None
    df2['의무보유확약비율']=None
    df2['공모가비율']=None
    df2['매출액비율']=None
    df2['순이익비율']=None
    
    data_count=0
    for row in labels:
        for i in range(len(df2)):
            data_count=df2.loc[i,row]
            df2.loc[i,row+'비율']=round(100*(data_count/462),2) 
    
    df2.drop(['경쟁률'], axis = 1,inplace = True)
    df2.drop(['의무보유확약'], axis = 1,inplace = True)
    df2.drop(['공모가'], axis = 1,inplace = True)
    df2.drop(['매출액'], axis = 1,inplace = True)
    df2.drop(['순이익'], axis = 1,inplace = True)
    # df2.drop(['희망공모가(상단)'], axis = 1,inplace = True) 
     
    plt.style.use('default')   
    plt.rc('font', family='NanumGothic')

    data = df2.iloc[count].drop('cor_name').tolist()
    data += data[:1]

    ax = plt.subplot(1,1,1, polar=True)

    ax.set_theta_offset(pi / 2) ## 시작점
    ax.set_theta_direction(-1) ## 그려지는 방향 시계방향

    plt.xticks(angles[:-1], labels, fontsize=10) ## x축 눈금 라벨
    ax.tick_params(axis='x', which='major', pad=15) ## x축과 눈금 사이에 여백을 준다.

    ax.set_rlabel_position(0) ## y축 각도 설정(degree 단위)
    plt.yticks([0,20,40,60,80,100],['0','20','40','60','80','100'], fontsize=10) ## y축 눈금 설정
    plt.ylim(0,100)
    
    print(angles)
    print(data)
    
    ax.plot(angles, data, color='blue', linewidth=2, linestyle='solid') ## 레이더 차트 출력
    ax.fill(angles, data, color='blue', alpha=0.1) ## 도형 안쪽에 색을 채워준다.

    plt.title(df2.iloc[count]['cor_name'],font={'size':20,'weight':BOLD},pad=20)
    
    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    
    
    return buf,data1,data2,data3,data4,data5,data_len

