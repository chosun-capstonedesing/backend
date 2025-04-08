## app/api/endpoints/reports.py
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import FileResponse
from app.services.reports import generate_final_pdf_report
from app.services.prediction import predict, predict_probabilities
from app.utils.model_info import extract_model_info
from app.services.prediction import predict_full_report_data
import os
import shutil

router = APIRouter()

@router.post("/report/download")
def generate_auto_pdf(file: UploadFile = File(...)):
    """
    배포용 PDF 리포트 자동 생성 API
    - 파일 하나만 입력하면 내부적으로 /predict, /piechart 호출 후 결과 종합
    - 모델 정보 및 로그 포함하여 자동 보고서 생성
    """
    # 1. 파일 저장
    extension = os.path.splitext(file.filename)[1].lower()
    save_path = f"./temp_uploads/{file.filename}"
    os.makedirs("./temp_uploads", exist_ok=True)

    with open(save_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # 2. 예측 결과 (/predict), 3. 퍼센트 예측 (/piechart)
    predict_result, piechart_result = predict_full_report_data(save_path, extension)

    # 4. 모델 정보
    model_info = extract_model_info(extension)

    # 5. 최종 result 객체 구성
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

    # 6. PDF 생성
    file.file.seek(0)  # PDF 생성을 위한 포인터 초기화
    pdf_path = generate_final_pdf_report(file, result)

    return FileResponse(
        path=pdf_path,
        filename=f"{file.filename}_report.pdf",
        media_type="application/pdf"
    )