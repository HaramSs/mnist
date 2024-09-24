import jigeum.seoul
import os 
import numpy as np
from PIL import Image
from keras.models import load_model

# 모델 로드
model = load_model('/home/haram/code/mnist/note/mnist240924.keras')  # 학습된 모델 파일 경로

# 사용자 이미지 불러오기 및 전처리
def preprocess_image(image_path):
    img = Image.open(image_path).convert('L')  # 흑백 이미지로 변환
    img = img.resize((28, 28))  # 크기 조정

    # 흑백 반전
    # img = 255 - np.array(img)  # 흑백 반전
    img = np.array(img)
    
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

def get_job_img_task():
    from mnist.db import select
    sql="select num, file_name, file_path from image_processing where prediction_result IS NULL order by num limit 1"
    r=select(sql, 1)

    if len(r)>0:
        return r[0]
    else:
        return None
    
def run():
    """image_processing 테이블을 읽어서 가장 오래된 요청 하나씩을 처리"""
  
    # STEP 1
    # image_processing 테이블의 prediction_result IS NULL 인 ROW 1 개 조회 - num 가져오기
    from mnist.db import select,dml 
    sql= "SELECT num FROM image_processing where prediction_result IS NULL"
    result = select(query=sql,size=1)
    if len(result) == 0:
        print("job is Zero")
        return

    # STEP 2
    # RANDOM 으로 0 ~ 9 중 하나 값을 prediction_result 컬럼에 업데이트
    job=get_job_img_task()
    file_path=job['file_path']
    rnum= predict_digit(file_path) 
    sql= "UPDATE image_processing SET prediction_result=%s WHERE num = %s"
    num = result[0]['num']
    insert_row=dml(sql, rnum, num)
    # 동시에 prediction_model, prediction_time 도 업데이트
    sql= "UPDATE image_processing SET prediction_model= %s,prediction_time=%s WHERE num = %s"
    insert_row=dml(sql,'n19',jigeum.seoul.now(),result[0]['num'])

    # STEP 3
    # LINE 으로 처리 결과 전송
    send_noti(num)

    print(f"작업 요청 시간:{jigeum.seoul.now()}")

def send_noti(num=999):
    import requests   
    api_url = "https://notify-api.line.me/api/notify"
    token = os.getenv('LINE_TOKEN')
    headers = {'Authorization':'Bearer '+ token}
    print(headers)

    message = {
       "message" : f"{jigeum.seoul.now()}:task done successful=>{num}"
    }

    r = requests.post(api_url, headers= headers , data = message)
    print(r)
