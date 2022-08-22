import numpy as np 

import pandas as pd
import numpy as np

from tqdm import tqdm


import matplotlib.pyplot as plt
import tensorflow_addons as tfa
import tensorflow as tf

from transformers import BertTokenizer, TFBertForSequenceClassification


def convert_data(X_data,MAX_SEQ_LEN,tokenizer):
    # BERT 입력으로 들어가는 token, mask, segment, target 저장용 리스트

    
    tokens, masks, segments, targets = [], [], [], []
    
    for X in (X_data):
        # token: 입력 문장 토큰화
        token = tokenizer.encode(X, truncation = True, padding = 'max_length', max_length = MAX_SEQ_LEN)
        
        # Mask: 토큰화한 문장 내 패딩이 아닌 경우 1, 패딩인 경우 0으로 초기화
        num_zeros = token.count(0)
        mask = [1] * (MAX_SEQ_LEN - num_zeros) + [0] * num_zeros
        
        # segment: 문장 전후관계 구분: 오직 한 문장이므로 모두 0으로 초기화
        segment = [0]*MAX_SEQ_LEN

        tokens.append(token)
        masks.append(mask)
        segments.append(segment)

    # numpy array로 저장
    tokens = np.array(tokens)
    masks = np.array(masks)
    segments = np.array(segments)
  

    return [tokens, masks, segments]


# 최고 성능의 모델 불러오기
def get_title_score2():



    import warnings
    warnings.filterwarnings('ignore')

    from pathlib import Path
    BASE_DIR = Path(__file__).resolve().parent.parent

    MODEL_NAME = "klue/bert-base"
    tokenizer = BertTokenizer.from_pretrained(MODEL_NAME)

    model  = tf.keras.models.load_model(BASE_DIR/'Crawling/best_model.h5',
                                                      custom_objects={'TFBertForSequenceClassification': TFBertForSequenceClassification})



    df = pd.read_csv(BASE_DIR/'Crawling/after_prepros.csv')
    news_df = pd.read_csv(BASE_DIR/'Crawling/news_title.csv')
      
    df = df.drop('Unnamed: 0',axis= 1)
    try:
      news_df = news_df.drop('Unnamed: 0',axis= 1)
    except:
      news_df = news_df 

    df = df.merge(news_df,on='cor_name')

    X_data = news_df['title']
    MAX_SEQ_LEN = 64
    tokenizer = BertTokenizer.from_pretrained('klue/bert-base')

    # train 데이터를 Bert의 Input 타입에 맞게 변환

    train_x= convert_data(X_data,MAX_SEQ_LEN,tokenizer)

    # print(train_x)
    predicted_value = model.predict(train_x)
    predicted_label = np.argmax(predicted_value, axis = 1)
    df['label']=np.array(predicted_label)

    df.to_csv(BASE_DIR/'Crawling/after_prepros_label.csv')




