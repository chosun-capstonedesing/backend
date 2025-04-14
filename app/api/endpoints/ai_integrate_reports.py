# app/api/endpoints/ai_integrate_reports.py
import os
from fastapi import APIRouter, UploadFile, File
from app.services.prediction import predict_full_report_data
from app.services.ai_integrate_reports import generate_pdf_report_by_extension

router = APIRouter()

# app/api/endpoints/ai_integrate_reports.py
import os

@router.post("/report")
async def generate_report(file: UploadFile = File(...)):
    ext = file.filename.split(".")[-1]
    save_dir = "./temp_uploads"
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, file.filename)
    file_bytes = await file.read()

    # 저장
    with open(save_path, "wb") as f:
        f.write(file_bytes)

    # 저장 확인
    print(f"📁 Save path (절대경로): {os.path.abspath(save_path)}")
    print(f"🧪 저장 직후 존재 확인: {os.path.exists(save_path)}")

    result_data, prob_data = predict_full_report_data(save_path, ext)

    # 생성 시점에 다시 존재 확인
    print(f"📄 generate_pdf_report_by_extension → 절대 경로: {save_path}")
    print(f"📄 파일 존재 확인: {os.path.exists(save_path)}")

    ## postmand에서 파일 보게 하는거
    # pdf_path = generate_pdf_report_by_extension(save_path, ext, result_data, prob_data)
    # return {"report_path": pdf_path}
    file_path = save_path
    pdf_path = generate_pdf_report_by_extension(file_path, ext, result_data, prob_data)
  # 실제 파일 저장 경로
    static_url = f"/static/{os.path.basename(pdf_path)}"
    return {"download_url": static_url}