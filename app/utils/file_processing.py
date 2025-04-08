## app/utils/file_processing.py
""
" 전처리 : 확장자 추가 시 유연하게 확장하기 위한 파일"
""
from PIL import Image
import numpy as np


def convert_exe_to_image(file_path):
    with open(file_path, 'rb') as f:
        byte_data = f.read()

    max_size = 256 * 256
    byte_data = byte_data[:max_size] + b'\x00' * max(0, max_size - len(byte_data))
    byte_arr = np.frombuffer(byte_data, dtype=np.uint8)
    image_arr = byte_arr.reshape((256, 256))
    return Image.fromarray(image_arr, mode='L')


def convert_pdf_to_image(file_path):
    raise NotImplementedError("PDF 변환 준비 중")


def convert_hwp_to_image(file_path):
    raise NotImplementedError("HWP 변환 준비 중")


# 확장자별로 (변환 함수, resize 크기) 관리
CONVERTER_MAP = {
    "exe": (convert_exe_to_image, (256, 256)),
    "pdf": (convert_pdf_to_image, (224, 224)),
    "hwp": (convert_hwp_to_image, (224, 224)),
}

