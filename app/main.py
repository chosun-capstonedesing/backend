## app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api.endpoints import files
from app.api.endpoints import reports  
from app.api.endpoints import ai_cnn_reports 
from app.api.endpoints import ai_rf_reports 
from app.api.endpoints import ai_integrate_reports

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(files.router, prefix="/files", tags=["File Detection"])
app.mount("/static", StaticFiles(directory="temp_uploads"), name="static")
app.include_router(reports.router, prefix="/files") 
#app.include_router(ai_cnn_reports.router, prefix="/files") 
#app.include_router(ai_rf_reports.router, prefix="/files") 
app.include_router(ai_integrate_reports.router, prefix="/files")
