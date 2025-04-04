import torch
from torchvision import transforms
from PIL import Image
import os
from app.models.cnn_model import SimpleCNN as MyCNN
from app.utils.file_processing import CONVERTER_MAP


MODEL_CACHE = {}
MODEL_DIR = os.path.join(os.path.dirname(__file__), "../assets")

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


def predict(file_path: str, file_ext: str):
    ext = file_ext.lower()
    model = load_model_by_extension(file_ext)

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
            probabilities = torch.nn.functional.softmax(output, dim=1)
            confidence, prediction = torch.max(probabilities, 1)
            result = "악성" if prediction.item() == 1 else "정상"

    except Exception as e:
        result = f"에러 발생: {str(e)}"
        confidence = 0.0

    finally:
        try:
            os.remove(file_path)
        except Exception as del_err:
            print(f"파일 삭제 실패: {del_err}")

    return {
        "result": result,
        "confidence": round(confidence.item(), 4)
    }

