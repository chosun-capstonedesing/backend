from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Malware Detection Platform API"}

def test_upload_file():
    # 더미 파일 생성 및 업로드 테스트
    file_content = b"Dummy content for testing."
    response = client.post(
        "/files/upload",
        files={"file": ("test.txt", file_content, "text/plain")}
    )
    assert response.status_code == 200
    json_response = response.json()
    assert "filename" in json_response
    assert "prediction" in json_response
