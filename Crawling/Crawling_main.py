import time
import aiohttp
import asyncio
import numpy as np
import pandas as pd
import requests, re, time
import urllib.request as ur
from bs4 import BeautifulSoup as bs
from Crawling_38_basic_info import crawling_38_basic_info
from Crawling_38_day import crawling_38_day
from Crawling_data import crawling_data
from Crawling_news_url import news_main
from preprocessing import preprocessing




# from pathlib import Path
# BASE_DIR = Path(__file__).resolve().parent.parent
# print(2)
# crawling_38_basic_info(BASE_DIR)
# print(1)
# crawling_38_day(BASE_DIR)
# print(2)
# crawling_data(BASE_DIR)
# print(3)
# 
# preprocessing()

df = pd.DataFrame(
    columns=[
        "cor_name",
        "title",
    ]
)
start_time = time.time()
asyncio.run(news_main(df))
print('learning time : ',time.time()-start_time)