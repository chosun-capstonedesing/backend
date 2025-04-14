## app/api/endpoints/ai_cnn_reports.py
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import FileResponse
from app.services.ai_cnn_reports import generate_final_pdf_report as generate_ai_pdf
from app.utils.model_info import extract_model_info
from app.services.prediction import predict_full_report_data
import os
import shutil

router = APIRouter()

@router.post("/report/ai/download")
def generate_ai_pdf_report(file: UploadFile = File(...)):
    """
    GPT 기반 AI 분석 보고서 다운로드 엔드포인트
    - .hwp / MS Office 등 GPT 기반 분석에 적합한 파일을 대상으로 실행됨
    """
    extension = os.path.splitext(file.filename)[1].lower()
    save_path = f"./temp_uploads/{file.filename}"
    os.makedirs("./temp_uploads", exist_ok=True)

    with open(save_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    predict_result, piechart_result = predict_full_report_data(save_path, extension)
    model_info = extract_model_info(extension)

    result = {
        "filename": file.filename,
        "extension": extension,
        "confidence": round(piechart_result["malicious"] / 100, 4),
        "malicious_percent": piechart_result["malicious"], 
        "accuracy": predict_result.get("accuracy"),
        "result": predict_result.get("result"),
        "log": predict_result.get("log"),
        "model_info": model_info
    }

    file.file.seek(0)
    pdf_path = generate_ai_pdf(file, result)

    return FileResponse(
        path=pdf_path,
        filename=f"{file.filename}_ai_report.pdf",
        media_type="application/pdf"
    )
