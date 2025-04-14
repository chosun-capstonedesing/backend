## app/api/endpoints/files.py
from fastapi import APIRouter, UploadFile, File
import os
import shutil
from datetime import datetime
from app.services.prediction import predict
from app.services.prediction import predict, predict_probabilities
from app.utils.model_info import extract_model_info

router = APIRouter()

## 파일 악성/정상 판별 + 모델의 정확도
@router.post("/predict")
async def predict_file(file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename)[1]
    save_path = f"./temp_uploads/{file.filename}"
    os.makedirs("temp_uploads", exist_ok=True)

    with open(save_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    try:
        prediction_result = predict(save_path, ext)
        return {
            "filename": file.filename,
            "extension": ext,
            "result": prediction_result["result"],
            "accuracy": prediction_result["accuracy"],
            "log": prediction_result["log"]
        }
    except Exception as e:
        return {"error": str(e)}


## Pie Chart : 파일 악성/정상 몇 % 비율인지
@router.post("/piechart")
async def predict_piechart(file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename)[1]
    save_path = f"./temp_uploads/{file.filename}"
    os.makedirs("temp_uploads", exist_ok=True)

    with open(save_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    try:
        result = predict_probabilities(save_path, ext)
        return {
            "filename": file.filename,
            "extension": ext,
            "normal": result["normal"],
            "malicious": result["malicious"]
        }
    except Exception as e:
        return {"error": str(e)}
    
## 분석 환경 + 분석 로그 요약
@router.post("/meta")
async def extract_file_meta(file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename)[1]
    save_path = f"./temp_uploads/{file.filename}"
    os.makedirs("temp_uploads", exist_ok=True)

    with open(save_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    try:
        # 분석 결과 예측 (여기서 log 포함돼서 나옴)
        result = predict(save_path, ext)
        log = result.get("log", {})
        model_info = extract_model_info(ext)

        return {
            "model_info": {
                "type": model_info.get("type", "Unknown"),
                "input": model_info.get("input", "-"),
                "train_size": model_info.get("train_size", "-"),
                "test_accuracy": result.get("accuracy", None)
            },
            "log": {
                "start_time": log.get("start_time", "-"),
                "model_load": log.get("model_load", "-"),
                "preprocess": log.get("preprocess", "-"),
                "inference": log.get("inference", "-")
            }
        }

    except Exception as e:
        return {"error": str(e)}
