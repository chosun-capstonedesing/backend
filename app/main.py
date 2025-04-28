## app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from app.api.endpoints import files
from app.api.endpoints import reports  
from app.api.endpoints import ai_cnn_reports 
from app.api.endpoints import ai_rf_reports 
from app.api.endpoints import ai_integrate_reports
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


os.makedirs("./temp_uploads/input", exist_ok=True)
os.makedirs("./temp_uploads/output", exist_ok=True)


app.include_router(files.router, prefix="/files", tags=["File Detection"])
app.mount("/static", StaticFiles(directory="temp_uploads/output"), name="static")
#app.include_router(reports.router, prefix="/files") 
#app.include_router(ai_cnn_reports.router, prefix="/files") 
#app.include_router(ai_rf_reports.router, prefix="/files") 
app.include_router(ai_integrate_reports.router, prefix="/files")


# 루트 접속 시 안내 페이지
# @app.get("/", response_class=HTMLResponse)
# def read_root():
#     return """
#     <html>
#         <head>
#             <meta name="robots" content="noindex, nofollow">
#             <title>테스트용 API 서버</title>
#         </head>
#         <body style="font-family: sans-serif;">
#             <h2>🔒 내부 테스트용 백엔드 API 서버입니다.</h2>
#             <p>이 서버는 <b>웹 개발 확인용</b>이며, 외부에 공개된 서비스가 아닙니다.</p>
#             <p>검색 엔진에 노출되지 않도록 <code>robots</code> 설정이 적용되어 있습니다.</p>
#         </body>
#     </html>
#     """

# 검색 로봇 접근 차단
@app.get("/robots.txt", response_class=PlainTextResponse)
def robots_txt():
    return "User-agent: *\nDisallow: /"
