## app/services/prediction.py
import torch
from torchvision import transforms
from PIL import Image
import os
import time
from datetime import datetime
from app.models.cnn_model import SimpleCNN as MyCNN
from app.utils.file_processing import CONVERTER_MAP
from app.utils.performance_timer import InferenceTimer


MODEL_CACHE = {}
MODEL_DIR = os.path.join(os.path.dirname(__file__), "../assets")

# 각 확장자별 정확도 (Test Accuracy)
ACCURACY_MAP = {
    "exe": 95.61,
    "pdf": 93.42,
    "hwp": 92.73,
    "docx": 94.15,
    "xlsx": 91.89,
}

## 확장자 받기
def load_model_by_extension(file_ext: str):
    ext = file_ext.strip(".").lower()
    if ext not in MODEL_CACHE:
        model_path = os.path.join(MODEL_DIR, f"CNN_{ext}.pth")
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"모델 {model_path} 이 존재하지 않습니다.")
        checkpoint = torch.load(model_path, map_location="cpu")

        num_classes = checkpoint.get('num_classes', 2)  # 혹시 없을 경우 대비해서 기본값 2
        model = MyCNN(num_classes)

        model.load_state_dict(checkpoint['model_state_dict'])
        model.eval()
        MODEL_CACHE[ext] = model
    return MODEL_CACHE[ext]

## 파일 악성/정상 판별 + 모델의 정확도 + 시간 측정
def predict(file_path: str, file_ext: str):
    ext = file_ext.lower().strip(".")
    timer = InferenceTimer()

    #model = load_model_by_extension(file_ext)
    model = load_model_by_extension(ext)
    timer.mark("model_load")

    try:
        if ext in CONVERTER_MAP:
            convert_func, resize_shape = CONVERTER_MAP[ext]
            image = convert_func(file_path) if convert_func else Image.open(file_path).convert("L")
        else:
            raise ValueError(f"{ext} 확장자는 아직 지원되지 않습니다.")
        timer.mark("preprocess")

        transform = transforms.Compose([
            transforms.Resize(resize_shape),
            transforms.ToTensor()
        ])
        input_tensor = transform(image).unsqueeze(0)

        with torch.no_grad():
            output = model(input_tensor)
            prediction = torch.argmax(output, 1).item()
        timer.mark("inference")

        result = "악성" if prediction == 1 else "정상"
        accuracy = ACCURACY_MAP.get(ext, None)

    except Exception as e:
        result = f"에러 발생: {str(e)}"
        accuracy = None

    finally:
        try:
            os.remove(file_path)
        except Exception as del_err:
            print(f"파일 삭제 실패: {del_err}")

    return {
        "result": result,
        "accuracy": accuracy,
        "log": timer.get_log()
    }

## Pie Chart : 파일 악성/정상 몇 % 비율인지
def predict_probabilities(file_path: str, file_ext: str):
    ext = file_ext.lower().strip(".")  # ".exe" → "exe"
    model = load_model_by_extension(ext)

    # print(f"[DEBUG] ext: {ext}")
    # print(f"[DEBUG] converter_map: {CONVERTER_MAP}")

    try:
        if ext in CONVERTER_MAP:
            convert_func, resize_shape = CONVERTER_MAP[ext]
            image = convert_func(file_path) if convert_func else Image.open(file_path).convert("L")
        else:
            raise ValueError(f"{ext} 확장자는 아직 지원되지 않습니다.")

        transform = transforms.Compose([
            transforms.Resize(resize_shape),
            transforms.ToTensor()
        ])
        input_tensor = transform(image).unsqueeze(0)

        with torch.no_grad():
            output = model(input_tensor)
            probabilities = torch.nn.functional.softmax(output, dim=1)[0]
            normal_score = round(probabilities[0].item() * 100, 2)
            malicious_score = round(probabilities[1].item() * 100, 2)

    except Exception as e:
        normal_score, malicious_score = 0.0, 0.0
        print(f"에러 발생: {str(e)}")

    finally:
        try:
            os.remove(file_path)
        except Exception as del_err:
            print(f"파일 삭제 실패: {del_err}")

    return {
        "normal": normal_score,
        "malicious": malicious_score
    }


def predict_full_report_data(file_path: str, file_ext: str):
    ext = file_ext.lower().strip(".")
    timer = InferenceTimer()
    model = load_model_by_extension(ext)
    timer.mark("model_load")

    try:
        if ext in CONVERTER_MAP:
            convert_func, resize_shape = CONVERTER_MAP[ext]
            image = convert_func(file_path) if convert_func else Image.open(file_path).convert("L")
        else:
            raise ValueError(f"{ext} 확장자는 아직 지원되지 않습니다.")
        timer.mark("preprocess")

        transform = transforms.Compose([
            transforms.Resize(resize_shape),
            transforms.ToTensor()
        ])
        input_tensor = transform(image).unsqueeze(0)

        with torch.no_grad():
            output = model(input_tensor)
            probabilities = torch.nn.functional.softmax(output, dim=1)[0]
            prediction = torch.argmax(output, 1).item()

        timer.mark("inference")

        result = "악성" if prediction == 1 else "정상"
        accuracy = ACCURACY_MAP.get(ext, None)
        normal_score = round(probabilities[0].item() * 100, 2)
        malicious_score = round(probabilities[1].item() * 100, 2)

    except Exception as e:
        result = f"에러 발생: {str(e)}"
        accuracy = None
        normal_score, malicious_score = 0.0, 0.0

    finally:
        try:
            os.remove(file_path)
        except Exception as del_err:
            print(f"파일 삭제 실패: {del_err}")

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
