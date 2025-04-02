from fastapi import APIRouter, UploadFile, File
import os
import shutil
from app.services.prediction import predict

router = APIRouter()

@router.post("/predict")
async def predict_file(file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename)[1]
    save_path = f"./temp_uploads/{file.filename}"
    os.makedirs("temp_uploads", exist_ok=True)

    with open(save_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    try:
        result = predict(save_path, ext)
        return {"filename": file.filename, "extension": ext, "result": result}
    except Exception as e:
        return {"error": str(e)}
