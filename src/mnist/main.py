from typing import Annotated

from fastapi import FastAPI, File, UploadFile

app = FastAPI()


@app.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    # 파일 저장
    img = await file.read()
    file_name = file.filename
    # 디렉토리가 없으면 오류, 코드에서 확인 및 만들기 추가
    upload_dir = "./photo"
    import os
    file_full_path = os.path.join(upload_dir, file_name)

    with open(file_full_path, "wb") as f:
        f.write(img)

    # 파일 저장 경로 DB INSERT
    # tablename : image_processing
    # 컬럼 정보 : num (초기 인서트, 자동 증가)
    # 컬럼 정보 : 파일이름, 파일경로, 요청시간(초기 인서트), 요청사용자(n00)
    # 컬럼 정보 : 예측모델, 예측결과, 예측시간(추후 업데이트)
    return {
            "filename": file.filename,
            "content_type": file.content_type,
            "file_full_path": file_full_path
           }





