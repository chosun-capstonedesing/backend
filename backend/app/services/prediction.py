def predict_file(processed_data):
    # 머신러닝 모델을 로드 -> 예측 수행
    return {
        "prediction": "malicious",
        "details": {"confidence": 0.95}
    }
