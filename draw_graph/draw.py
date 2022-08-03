import matplotlib.pyplot as plt
import pandas as pd
from io import BytesIO
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['Ipo']

def get_graph(cor_name,cor_shape):
    
    plt.style.use('ggplot')
    plt.rc('font', family='NanumGothic')
    df = pd.DataFrame(db.inform.find({},{'_id':False}))	# 모든 데이터 조회
    
    
    df['순위']=df[cor_shape].rank(method='min',ascending=False)
    df=df.sort_values(by=[cor_shape])
    
    plt.plot(df['순위'],df[cor_shape],color='black')
        
    x=df.loc[df['기업명']==cor_name]['순위'].unique()
    y=df.loc[df['기업명']==cor_name][cor_shape].unique()
        
    plt.scatter(x,y,color='r',s=200,label=cor_name) 
    
    
    plt.title(cor_name +"  "+ cor_shape)
    plt.xlabel('순위',labelpad=1)
    plt.ylabel(cor_shape,labelpad=1)        
    plt.legend(loc="upper right")

    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    
    count=df['순위'].count()    
    rank_count=df.loc[df['기업명']==cor_name]['순위'].unique()
    rank_count=int(rank_count)
    return buf,rank_count,count