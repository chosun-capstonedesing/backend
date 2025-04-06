from fastapi import APIRouter, UploadFile, File
import os
import shutil
from app.services.prediction import predict
from app.services.prediction import predict, predict_probabilities

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
            "accuracy": prediction_result["accuracy"]
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