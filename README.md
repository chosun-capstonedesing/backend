## 🛡️ MLD Web - Backend

파일 분석 요청 처리, CNN 기반 모델 예측 수행, 결과 반환 및 보고서(PDF) 추출 기능, 로그인 로직 등을 제공.  
FastAPI 기반의 비동기 REST API 서버로, 확장성과 유지보수성을 고려한 구조로 설계.

---

## 🌐 API 서버 배포 주소
👉 [API 서버 배포 주소](http://52.79.208.233:8001)

> 🔐 현재 백엔드 API 서버는 테스트 목적의 내부 확인용.  
> 외부 인증 없이 접근 가능하지만, 검색 엔진에는 노출되지 않으며  
> 정식 배포 전까지는 팀원 전용으로 공유 할 예정.

---

## 🔧 배포 계획 요약
Render로 1차 배포가 목적이었으나, 그냥 AWS Ec2 + Docker OR venv 로 테스트 배포 중

---

## ✅ 향후 계획

- PDF 보고서 내 GPT API 기능 연동 후 출력 목표
- 로그인 및 인증 처리 기능 구현 (DB 연동 예정)  

---

## 🛠️ 사용 기술 스택

<div align="center">

<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
<img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" />
<img src="https://img.shields.io/badge/Uvicorn-44A833?style=for-the-badge&logo=uvicorn&logoColor=white" />
<img src="https://img.shields.io/badge/SQLAlchemy-336791?style=for-the-badge&logo=sqlalchemy&logoColor=white" />
<img src="https://img.shields.io/badge/PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white" />
<img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" />

</div>


---

## 📂 프로젝트 구조
```
backend/
├── app/
│   ├── api/
│   │   └── endpoints/
│   │       ├── files.py    -> /predict, /piechart, /meta API 정의
|   |       ├── ai_cnn_reports.py  
|   |       ├── ai_integrate_reports.py  -> /files/report API 정의
|   |       ├── ai_rf_reports.py  
|   |       ├── report_legacy.py 
│   │       ├── reports.py  
│   │       └── users.py
│   ├── assets/
│   │   ├── CNN_exe.pth
│   │   ├── Randomforest_pdf.pkl
│   │   ├── fonts/
│   │   │   ├── NotoSansKR-Bold.ttf
│   │   │   └── NotoSansKR-Regular.ttf
│   │   └── images/
│   │       └── report_logo.png
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   ├── database/
│   │   └── session.py
│   ├── models/
│   │   ├── cnn_model.py
│   │   ├── rf_model.py
│   │   ├── file.py
│   │   └── users.py
│   ├── schemas/
│   │   ├── file.py
│   │   └── users.py
│   ├── services/
│   │   └── ai_cnn_reports.py
│   │   └── ai_integrate_reports.py
│   │   └── ai_rf_reports.py
│   │   └── prediction.py
|   |   └── reports.py
│   ├── utils/
│   │   ├── file_processing.py
│   │   ├── image_converter.py
│   │   ├── model_info.py
│   │   ├── pdfid_info.py
│   │   └── performance_timer.py
│   ├── __init__.py
│   └── main.py
├── temp_uploads/
│   └── input/
│   └── output/
├── tests/
│   └── test_files.py
├── .dockerignore
├── .env
├── .gitignore
├── Dockerfile
├── README.md
└── requirements.txt

```

