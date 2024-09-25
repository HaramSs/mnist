import jigeum.seoul
import os
import random
import numpy as np
from PIL import Image
from keras.models import load_model

def get_job_img_task():
    from mnist.db import select
    sql="select num, file_name, file_path from image_processing where prediction_result IS NULL order by num limit 1"
    r=select(sql, 1)

    if len(r)>0:
        return r[0]
    else:
        return None

# 모델 로드
model = load_model('./mnist240924.keras')  # 학습된 모델 파일 경로

# 사용자 이미지 불러오기 및 전처리
def preprocess_image(image_path):
    img = Image.open(image_path).convert('L')  # 흑백 이미지로 변환
    img = img.resize((28, 28))  # 크기 조정

    # 흑백 반전
    img = 255 - np.array(img)  # 흑백 반전
    
    img = np.array(img)
    img = img.reshape(1, 28, 28, 1)  # 모델 입력 형태에 맞게 변형
    img = img / 255.0  # 정규화
    return img

# 예측
def predict_digit(image_path):
    img = preprocess_image(image_path)
    prediction = model.predict(img)
    digit = np.argmax(prediction)
    return digit

def prediction(file_path, num):
    from mnist.db import dml
    sql="update image_processing set prediction_result=%s, prediction_model='n19', prediction_time=%s where num=%s"
    job=get_job_img_task()
    file_path=job['file_path']
    presult=predict_digit(file_path)
    dml(sql, presult, jigeum.seoul.now(), num)
    return presult

def run():
    job=get_job_img_task()
    if job is None:
        print(f"{jigeum.seoul.now()}- job is None")
        return

    num=job['num']
    file_name=job['file_name']
    file_path=job['file_path']
    
    presult= prediction(file_path, num)

    print(jigeum.seoul.now())

    # line
    import requests
    api_url = "https://notify-api.line.me/api/notify"
    token = os.getenv('LINE_TOKEN', None)

    headers={'Authorization':'Bearer '+token}

    message={
        "message": f"{jigeum.seoul.now()}: 작업에 성공, result={presult}"
            }

    requests.post(api_url, headers=headers, data=message)
