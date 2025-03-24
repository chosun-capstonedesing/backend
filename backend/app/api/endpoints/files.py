from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services import file_processing, prediction
from app.schemas.file import FileResponse
import shutil
import os

router = APIRouter()

UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload", response_model=FileResponse)
async def upload_file(file: UploadFile = File(...)):
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # 파일 전처리 가져오는 거
    processed_data = file_processing.process_file(file_location)
    
    # 머신러닝 모델을 통한 예측 (더미 함수)
    prediction_result = prediction.predict_file(processed_data)
    
    return FileResponse(
        filename=file.filename,
        prediction=prediction_result.get("prediction", "unknown"),
        details=prediction_result.get("details", {})
    )
