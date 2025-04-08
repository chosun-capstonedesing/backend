from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import files
from app.api.endpoints import reports  

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(files.router, prefix="/files", tags=["File Detection"])
app.include_router(reports.router, prefix="/files") 
#app.include_router(report_legacy.router, prefix="/legacy", tags=["Legacy Reports"])  # 📌 경로 충돌 없게 동일하게 해도 됨
