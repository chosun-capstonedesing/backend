# app/api/endpoints/history_download.py
from fastapi import APIRouter, Depends, Header, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.db_persistence.analysis import FileAnalysis
from app.services.auth_service.auth import decode_access_token
from app.services.ai_db_reports import generate_final_pdf_report_from_db
import os

router = APIRouter()

@router.get("/download/{analysis_id}")
def download_pdf_report_from_history(
    analysis_id: str,
    authorization: str = Header(...),
    db: Session = Depends(get_db)
):
    # 인증 처리
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid Authorization Header")

    token = authorization.split(" ")[1]
    payload = decode_access_token(token)
    if payload is None or "user_id" not in payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user_id = payload["user_id"]

    # 분석 결과 조회 및 사용자 권한 확인
    record = db.query(FileAnalysis).filter(FileAnalysis.analysis_id == analysis_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Analysis not found")
    if str(record.user_id) != str(user_id):
        raise HTTPException(status_code=403, detail="Permission denied")

    # PDF 생성
    output_path = generate_final_pdf_report_from_db(
        analysis_id=analysis_id,
        db=db
    )

    if not os.path.exists(output_path):
        raise HTTPException(status_code=500, detail="PDF generation failed")

    return FileResponse(
        path=output_path,
        filename=f"{record.filename}_report.pdf",  # 사용자에게 보여줄 이름
        media_type="application/pdf"
    )
