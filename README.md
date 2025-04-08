## 🛡️ MLD Web - Backend

파일 분석 요청 처리, CNN 기반 모델 예측 수행, 결과 반환 및 보고서(PDF) 추출 기능, 로그인 로직 등을 제공.  
FastAPI 기반의 비동기 REST API 서버로, 확장성과 유지보수성을 고려한 구조로 설계.

---

## 🌐 API 서버 배포 주소
👉 [API 서버 배포 주소 (준비 중)](https://your-api-server-link.com)

> 🔐 현재 백엔드 API 서버는 테스트 목적의 내부 확인용.  
> 외부 인증 없이 접근 가능하지만, 검색 엔진에는 노출되지 않으며  
> 정식 배포 전까지는 팀원 전용으로 공유 할 예정.

---

## 🔧 배포 계획 요약

| 단계 | 목적               | 플랫폼             | 설명 |
|------|--------------------|---------------------|------|
| ✅ 1단계 | 테스트용 간편 배포     | [Render](https://render.com) | 현재 사용 중. 백엔드 기능 확인 및 팀원 공유 목적 |
| 🔜 2단계 | 정식 서비스 배포       | AWS EC2 + Docker    | 보안 설정 및 운영 환경 구축 (정식 배포 시 사용 예정) |

---

## ✅ 향후 계획

- PDF 보고서 자동 생성 및 다운로드 기능 연동  
- 로그인 및 인증 처리 기능 구현 (DB 연동 예정)  
- 다양한 확장자 지원을 위한 모델 범용화 및 예외 처리 강화  

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
│   │       ├── files.py    -> /predict API 정의
│   │       ├── reports.py  -> /report/download API 정의
│   │       └── users.py
│   ├── assets/
│   │   └── CNN_exe.pth
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   ├── database/
│   │   └── session.py
│   ├── models/
│   │   ├── cnn_model.py
│   │   ├── file.py
│   │   └── users.py
│   ├── schemas/
│   │   ├── file.py
│   │   └── users.py
│   ├── services/
│   │   └── prediction.py
|   |   └── reports.py
│   ├── utils/
│   │   ├── file_processing.py
│   │   └── image_converter.py
│   ├── __init__.py
│   └── main.py
├── tests/
│   └── test_files.py
├── .gitignore
├── README.md
└── requirements.txt

```

