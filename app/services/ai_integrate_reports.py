## app/services/ai_integrate_reports.py
import os
from fastapi import UploadFile
import unicodedata
from app.services.ai_cnn_reports import generate_final_pdf_report as cnn_report
from app.services.ai_rf_reports import generate_final_pdf_report as rf_report


class DummyUploadFile:
    def __init__(self, filename: str, file_path: str):
        self.filename = filename

        normalized_path = unicodedata.normalize("NFC", file_path)

        print(f" DummyUploadFile → 입력 경로: {file_path}")
        print(f" DummyUploadFile → 정규화 경로: {normalized_path}")
        print(f" DummyUploadFile → 파일 존재 여부 (정규화): {os.path.exists(normalized_path)}")
        print(f" DummyUploadFile → 파일 존재 여부 (원본): {os.path.exists(file_path)}")

        # 정규화된 경로 존재할 경우
        if os.path.exists(normalized_path):
            self.file = open(normalized_path, "rb")

        # 정규화 실패 시 원본 경로가 존재한다면 fallback
        elif os.path.exists(file_path):
            print(" 정규화된 경로는 없지만, 원본 경로는 존재 → 그 경로 사용")
            self.file = open(file_path, "rb")

        # 둘 다 없을 때는 에러 발생
        else:
            raise FileNotFoundError(
                f" 파일 없음: {normalized_path}\n"
                f"➡ 먼저 /files/predict 와 /files/piechart 를 호출하세요."
            )


def generate_pdf_report_by_extension(file_path: str, ext: str, result_data: dict, prob_data: dict):
    file_path = os.path.abspath(file_path)
    file_name = os.path.basename(file_path)

    print(f" generate_pdf_report_by_extension → 절대 경로: {file_path}")
    print(f" 파일 존재 확인: {os.path.exists(file_path)}")

    dummy_upload = DummyUploadFile(file_name, file_path)

    if "confidence" not in result_data:
        result_data["confidence"] = round(prob_data["malicious"] / 100, 4)

    if ext == "pdf":
        return rf_report(dummy_upload, result_data)
    elif ext == "exe":
        return cnn_report(dummy_upload, result_data)
    else:
        raise ValueError(f" 지원하지 않는 확장자: {ext}")

# class DummyUploadFile:
#     def __init__(self, filename: str, file_path: str):
#         self.filename = filename
#         normalized_path = unicodedata.normalize("NFC", file_path)

#         print(f" DummyUploadFile → 입력 경로: {file_path}")
#         print(f" DummyUploadFile → 정규화 경로: {normalized_path}")
#         print(f" DummyUploadFile → 파일 존재 여부 (정규화): {os.path.exists(normalized_path)}")
#         print(f" DummyUploadFile → 파일 존재 여부 (원본): {os.path.exists(file_path)}")

#         #  정규화된 경로가 존재할 경우 우선 사용
#         if os.path.exists(normalized_path):
#             self.file = open(normalized_path, "rb")

#         #  정규화된 경로가 없고 원본 경로가 존재할 경우 fallback
#         elif os.path.exists(file_path):
#             print("  정규화된 경로는 없지만, 원본 경로는 존재 → 그 경로 사용")
#             self.file = open(file_path, "rb")

#         #  둘 다 없으면 에러 처리
#         else:
#             raise FileNotFoundError(
#                 f" 파일 없음: {normalized_path}\n"
#                 f"➡ 먼저 /files/predict 와 /files/piechart 를 호출하세요."
#             )

#         self.file = open(normalized_path, "rb")


# def generate_pdf_report_by_extension(file_path: str, ext: str, result_data: dict, prob_data: dict):
#     file_path = os.path.abspath(file_path)
#     file_name = os.path.basename(file_path)
#     print(f" generate_pdf_report_by_extension → 절대 경로: {file_path}")
#     print(f" 파일 존재 확인: {os.path.exists(file_path)}")

#     dummy_upload = DummyUploadFile(file_name, file_path)  

#     if "confidence" not in result_data:
#         result_data["confidence"] = round(prob_data["malicious"] / 100, 4)

#     if ext == "pdf":
#         return rf_report(dummy_upload, result_data)
#     elif ext == "exe":
#         return cnn_report(dummy_upload, result_data)
#     else:
#         raise ValueError(f" 지원하지 않는 확장자: {ext}")
