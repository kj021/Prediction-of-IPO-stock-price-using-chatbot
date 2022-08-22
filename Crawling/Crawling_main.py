
def test():
    import time
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
    from get_title_score import get_title_score2
    from news_title_score import get_news_score

    from pathlib import Path
    BASE_DIR = Path(__file__).resolve().parent.parent

    crawling_38_basic_info(BASE_DIR)

    crawling_38_day(BASE_DIR)

    crawling_data(BASE_DIR)

    preprocessing()

    df = pd.DataFrame(
        columns=[
            "cor_name",
            "title",
        ]
    )
    start_time = time.time()

    asyncio.run(news_main(df))

    get_title_score2()
    get_news_score()


print(1)
test()