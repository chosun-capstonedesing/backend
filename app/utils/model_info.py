# app/utils/model_info.py — 모델 정보 정의 및 추출 함수 모음
import os
import torch

# 확장자별 기본 모델 정보 정리 -> 확장자 추가 시 유지 보수 편함
MODEL_INFO_MAP = {
    "exe": {
        "type": "CNN",
        "input": "Grayscale, 256x256",
        "train_size": "30,000",
        "path": "../assets/CNN_exe.pth" 
    },
    "pdf": {
        "type": "CNN",
        "input": "Grayscale, 256x256",
        "train_size": "18,000"
    },
    "hwp": {
        "type": "CNN",
        "input": "Grayscale, 256x256",
        "train_size": "19,000"
    },
   
}

# 모델 성능 점수
MODEL_PERFORMANCE_SCORE = {
    "exe": {
        "F1-Score": 96.53,
        "Precision": 96.11,
        "Recall": 97.02,
        "Benign": 97.86,
        "Malware": 96.18,
        "Accuracy": 97.0
    }

}

# 모델 정보 자동 추출 함수
def extract_model_info(extension: str):
    ext = extension.lower().strip(".")
    info = MODEL_INFO_MAP.get(ext)

    if not info:
        # 예외 확장자용 기본값
        return {
            "type": "Unknown",
            "input": "(예: Grayscale, 256x256)",
            "train_size": "(예: 30,000)"
        }

    model_path = os.path.join(os.path.dirname(__file__), info.get("path", ""))

    # 모델 파일이 존재하지 않으면 그대로 info 반환
    if not os.path.exists(model_path):
        return {
            "type": info["type"],
            "input": info["input"],
            "train_size": info["train_size"]
        }

    try:
        checkpoint = torch.load(model_path, map_location="cpu")
        num_classes = checkpoint.get("num_classes")

        train_size = f"{num_classes * 15000:,}" if isinstance(num_classes, int) else info["train_size"]

        return {
            "type": info["type"],
            "input": info["input"],
            "train_size": train_size
        }

    except Exception as e:
        print(f"[extract_model_info] 모델 정보 추출 실패: {e}")
        return {
            "type": info["type"],
            "input": info["input"],
            "train_size": info["train_size"]
        }



# 모델 성능 점수 자동 추출 함수
def get_model_performance_score(extension: str):
    return MODEL_PERFORMANCE_SCORE.get(extension.lower().strip("."), {})
