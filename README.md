# 🛡️ Malware Detection Web - Backend


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
│   │   ├── endpoints/
│   │   │   ├── files.py         
│   │   │   ├── users.py        
│   │   │   └── reports.py      
│   ├── core/
│   │   ├── config.py            
│   │   └── security.py         
│   ├── models/
│   │   ├── file.py              
│   │   └── user.py             
│   ├── schemas/
│   │   ├── file.py              
│   │   └── user.py             
│   ├── services/
│   │   ├── prediction.py       
│   │   └── file_processing.py   
│   ├── database/
│   │   └── session.py          
│   ├── main.py                  
│   └── __init__.py
├── tests/
│   └── test_files.py           
├── requirements.txt          
├── .env                       
├── Dockerfile                 
└── README.md


```

