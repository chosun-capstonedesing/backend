## app/services/prediction.py
import torch
from torchvision import transforms
from PIL import Image
import os
import time
import joblib
import pandas as pd
from datetime import datetime

from app.models.cnn_model import SimpleCNN as MyCNN
from app.models.rf_model import RandomForestPDFModel 
from app.models.auto_encoder_model import AEWithClassifier
from app.utils.file_processing import CONVERTER_MAP
from app.utils.performance_timer import InferenceTimer


MODEL_CACHE = {}
MODEL_DIR = os.path.join(os.path.dirname(__file__), "../assets")

# 정확도 맵 (하드코딩 값은 향후 동적 추출로 확장 가능)
ACCURACY_MAP = {
    "exe": 95.61,
    "pdf": 93.42,
    "hwp": 94.00,
    "docx": 79.00,
    "xlsx": 76.00,
}

# CNN + RandomForest + Auto Encoder 모델 로딩 통합
def load_model_by_extension(file_ext: str):
    ext = file_ext.strip(".").lower()
    if ext not in MODEL_CACHE:
        model_path = None
        for suffix in [".pth", ".pkl"]:
            for filename in os.listdir(MODEL_DIR):
                if filename.endswith(suffix) and f"_{ext}" in filename:
                    model_path = os.path.join(MODEL_DIR, filename)
                    break
            if model_path:
                break
        if not model_path:
            raise FileNotFoundError(f"{ext} 확장자에 맞는 모델 파일을 찾을 수 없습니다.")

        if ext in MODEL_CACHE:
            del MODEL_CACHE[ext]  # 캐싱된 모델 제거

        # AEWithClassifier 모델인 경우 (state_dict만 저장됨)
        if ext in ["hwp", "xlsx", "docx"] and model_path.endswith(".pth"):
            model = AEWithClassifier()
            model.load_state_dict(torch.load(model_path, map_location="cpu"))
            model.eval()

        # CNN 모델인 경우 (exe, hwp, xlsx, docx 등)
        elif model_path.endswith(".pth"):
            checkpoint = torch.load(model_path, map_location="cpu")
            num_classes = checkpoint.get("num_classes", 2)
            model = MyCNN(num_classes)
            model.load_state_dict(checkpoint["model_state_dict"])
            model.eval()

        # RandomForest 모델인 경우 (pdf 등)
        elif model_path.endswith(".pkl"):
            model = RandomForestPDFModel(model_path)

        else:
            raise ValueError(f"지원하지 않는 모델 형식: {model_path}")

        MODEL_CACHE[ext] = model

    return MODEL_CACHE[ext]



# 악성/정상 판단 함수 (CNN or RF or AE 공통 처리)
def predict(file_path: str, file_ext: str):
    ext = file_ext.lower().strip(".")
    timer = InferenceTimer()
    model = load_model_by_extension(ext)
    timer.mark("model_load")

    try:
        if ext not in CONVERTER_MAP:
            raise ValueError(f"{ext} 확장자는 아직 지원되지 않습니다.")
        convert_func, resize_shape = CONVERTER_MAP[ext]
        data = convert_func(file_path)
        timer.mark("preprocess")

        if isinstance(model, (MyCNN, AEWithClassifier)):
            transform = transforms.Compose([
                transforms.Resize(resize_shape),
                transforms.ToTensor()
            ])
            input_tensor = transform(data).unsqueeze(0)
            with torch.no_grad():
                if isinstance(model, AEWithClassifier):
                    _, logits = model(input_tensor)
                else:
                    logits = model(input_tensor)
                probs = torch.nn.functional.softmax(logits, dim=1)[0]
                prediction = torch.argmax(logits, 1).item()
            timer.mark("inference") 
        else:
            prediction, proba = model.predict(data)
            timer.mark("inference")  

        result = "악성" if prediction == 1 else "정상"
        accuracy = ACCURACY_MAP.get(ext, None)
        timer.mark("inference")

    except Exception as e:
        result = f"에러 발생: {str(e)}"
        accuracy = None

    # finally:
    #     try:
    #         os.remove(file_path)
    #     except Exception as del_err:
    #         print(f"파일 삭제 실패: {del_err}")

    return {
        "result": result,
        "accuracy": accuracy,
        "log": timer.get_log()
    }


# 확률 반환 함수 (CNN & RandomForest & AE 모두 대응)
def predict_probabilities(file_path: str, file_ext: str):
    ext = file_ext.lower().strip(".")
    model = load_model_by_extension(ext)

    try:
        if ext not in CONVERTER_MAP:
            raise ValueError(f"{ext} 확장자는 아직 지원되지 않습니다.")
        convert_func, resize_shape = CONVERTER_MAP[ext]
        data = convert_func(file_path)

        if isinstance(model, (MyCNN, AEWithClassifier)):
            transform = transforms.Compose([
                transforms.Resize(resize_shape),
                transforms.ToTensor()
            ])
            input_tensor = transform(data).unsqueeze(0)
            with torch.no_grad():
                if isinstance(model, AEWithClassifier):
                    _, logits = model(input_tensor)
                else:
                    logits = model(input_tensor)

                probs = torch.nn.functional.softmax(logits, dim=1)[0]
                normal_score = round(probs[0].item() * 100, 2)
                malicious_score = round(probs[1].item() * 100, 2)

        else:
            _, proba = model.predict(data)
            normal_score = round(proba[0] * 100, 2)
            malicious_score = round(proba[1] * 100, 2)

    except Exception as e:
        normal_score, malicious_score = 0.0, 0.0
        print(f"에러 발생: {str(e)}")

    # finally:
    #     try:
    #         os.remove(file_path)
    #     except Exception as del_err:
    #         print(f"파일 삭제 실패: {del_err}")

    return {
        "normal": normal_score,
        "malicious": malicious_score
    }


# 전체 보고서 출력용 데이터
def predict_full_report_data(file_path: str, file_ext: str):
    ext = file_ext.lower().strip(".")
    timer = InferenceTimer()
    model = load_model_by_extension(ext)
    timer.mark("model_load")

    try:
        if ext not in CONVERTER_MAP:
            raise ValueError(f"{ext} 확장자는 아직 지원되지 않습니다.")
        convert_func, resize_shape = CONVERTER_MAP[ext]
        data = convert_func(file_path)
        timer.mark("preprocess")

        if isinstance(model, (MyCNN, AEWithClassifier)):
            transform = transforms.Compose([
                transforms.Resize(resize_shape),
                transforms.ToTensor()
            ])
            input_tensor = transform(data).unsqueeze(0)
            with torch.no_grad():
                if isinstance(model, AEWithClassifier):
                    _, logits = model(input_tensor)
                else:
                    logits = model(input_tensor)

                probs = torch.nn.functional.softmax(logits, dim=1)[0]
                prediction = torch.argmax(logits, 1).item()
                normal_score = round(probs[0].item() * 100, 2)
                malicious_score = round(probs[1].item() * 100, 2)

        else:
            prediction, proba = model.predict(data)
            normal_score = round(proba[0] * 100, 2)
            malicious_score = round(proba[1] * 100, 2)

        result = "악성" if prediction == 1 else "정상"
        accuracy = ACCURACY_MAP.get(ext, None)
        timer.mark("inference")

    except Exception as e:
        result = f"에러 발생: {str(e)}"
        accuracy = None
        normal_score, malicious_score = 0.0, 0.0

    # finally:
    #     try:
    #         os.remove(file_path)
    #     except Exception as del_err:
    #         print(f"파일 삭제 실패: {del_err}")

    return (
        {
            "result": result,
            "accuracy": accuracy,
            "log": timer.get_log()
        },
        {
            "normal": normal_score,
            "malicious": malicious_score
        }
    )
