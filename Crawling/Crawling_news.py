import requests
import pandas as pd
from config import get_secret

keyword = 'lg에너지솔루션'

dfs = []

url = f"https://openapi.naver.com/v1/search/news?query={keyword}&start=1&display=10"

# headers = {"user-agent": UserAgent().chrome}
headers = {
        "X-Naver-Client-Id": get_secret("X-Naver-Client-Id"),
        "X-Naver-Client-Secret": get_secret("X-Naver-Client-Secret"),
    }
response = requests.get(url, headers=headers)
print(response.json()['items'])
# datas_df = pd.DataFrame(response.json())

# print(datas_df)
# datas_df = datas_df[["id"]]
# dfs.append(datas_df)

# result_df = pd.concat(dfs)
# result_df.reset_index(drop=True, inplace=True)



