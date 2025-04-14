## app/api/endpoints/ai_rf_reports.py
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import FileResponse
from app.services.prediction import predict_full_report_data
from app.services.ai_rf_reports import generate_rf_pdf_report

import os
import shutil

router = APIRouter()

@router.post("/report/pdf")
async def generate_pdf_ai_report(file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename)[1].lower()
    save_path = f"./temp_uploads/{file.filename}"
    os.makedirs("./temp_uploads", exist_ok=True)

    with open(save_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    result_data, prob_data = predict_full_report_data(save_path, ext)
    pdf_path = generate_rf_pdf_report(file, ext, result_data, prob_data)

    return FileResponse(
        path=pdf_path,
        filename=f"{file.filename}_rf_report.pdf",
        media_type="application/pdf"
    )
