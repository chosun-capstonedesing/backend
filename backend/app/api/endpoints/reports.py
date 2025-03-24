from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_reports():
    # 리포트 생성 로직 (추후 구현)
    return {"message": "Report generation endpoint. (Not implemented yet)"}
