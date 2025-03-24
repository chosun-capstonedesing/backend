from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import files, users, reports
from app.database.session import engine, Base

# 만약 데베 쓴다면?
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Malware Detection Platform API")

# CORS_프론트엔드 연동
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API 라우터 등록
app.include_router(files.router, prefix="/files", tags=["files"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(reports.router, prefix="/reports", tags=["reports"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Malware Detection Platform API"}
