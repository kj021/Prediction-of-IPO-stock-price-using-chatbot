import pandas as pd
import xml.etree.ElementTree as ET
import OpenDartReader
from DART.config import api_key

def get_find_Report(cor_name,count):
    count=int(count)
    dart = OpenDartReader(api_key) 
    find_code=dart.find_corp_code(cor_name)
    df=dart.list(find_code)
    
    URL = 'http://dart.fss.or.kr/api/link.jsp?rcpNo='
    df['link']=URL+df['rcept_no']
    
    data=[]
    
    Day=[]
    Report_name=[]
    Link=[]
    
    Text=[]
    
    for i in range(count):
        data.append(df.iloc[i].to_list())
    
    for i in range(count):
        Day.append(data[i][7])
        Report_name.append(data[i][4])
        Link.append(data[i][9])
        
    for i in range(count):
        data_new = Day[i] + " - " + cor_name + " - " +Report_name[i]+"\n"+Link[i]+"\n"
        Text.append(data_new)
        
    return Text
    
