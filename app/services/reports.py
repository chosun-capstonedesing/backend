## app/services/reports.py
import matplotlib
matplotlib.use("Agg")  # <- GUI 백엔드 막기
import matplotlib.pyplot as plt

from fpdf import FPDF
from datetime import datetime
import hashlib
import os
from matplotlib import rcParams
from app.utils.model_info import get_model_performance_score
from app.utils.model_info import extract_model_info 


rcParams['font.family'] = 'AppleGothic'

from fastapi import UploadFile


class CustomPDF(FPDF):
    def footer(self):
        self.set_y(-15)
        self.set_font("Noto", "", 10)
        self.set_text_color(100)
        page_num = f"- {self.page_no()} -"
        self.cell(0, 10, page_num, align='C')

# 모델 성능 점수 자동 추출 : F1/Recall/Precision, Benign/Malware 클래스 정확도 시각화 함수
def create_combined_model_performance_chart(perf):
    import matplotlib.pyplot as plt

    precision = perf["Precision"]
    recall = perf["Recall"]
    f1_score = perf["F1-Score"]
    benign = perf["Benign"]
    malware = perf["Malware"]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 3), gridspec_kw={'wspace': 0.8})

    # 좌측 막대 (가로)
    metrics = ['Precision', 'Recall', 'F1-Score']
    scores = [precision, recall, f1_score]
    colors1 = ['#A5C9FF', '#9BDCFD', '#CBA4F5']
    ax1.barh(metrics, scores, color=colors1)
    ax1.set_xlim(0, 100)
    ax1.set_xlabel("%")
    ax1.set_title("F1 / Precision / Recall", fontsize=12, y=1.05)  # 위로 올림

    for i, v in enumerate(scores):
        ax1.text(102, i, f"{v:.2f}%", va='center', fontsize=9)

    # 우측 막대 (세로)
    labels = ['Benign', 'Malware']
    values = [benign, malware]
    colors2 = ['#72A7F9', '#B295F8']
    bars = ax2.bar(labels, values, color=colors2)
    ax2.set_ylim(0, 110)
    ax2.set_ylabel("정확도 (%)")
    ax2.set_title("Accuracy by Class", fontsize=12, y=1.05)  # 위로 올림

    # 정확도 수치를 title 아래 위치하도록 조정
    for i, v in enumerate(values):
        ax2.text(i, 102, f"{v:.2f}%", ha='center', fontsize=9)

    chart_path = "combined_performance_chart.png"
    #plt.tight_layout()
    plt.subplots_adjust(bottom=0.2) # 하단 여백 확보 하기 위에 위 코드 주석 처리
    plt.savefig(chart_path)
    plt.close()
    return chart_path

# ✅ 추가: 간트 차트 스타일 로그 타임라인 시각화 함수
def create_log_gantt_chart(model_load, preprocess, inference):
    try:
        import matplotlib.pyplot as plt

        total = model_load + preprocess + inference
        segments = [model_load, preprocess, inference]
        labels = ['모델 로딩', '전처리', '추론']
        colors = ['#93C5FD', '#FDE68A', '#FCA5A5']

        fig, ax = plt.subplots(figsize=(6.5, 1))
        start = 0
        prev_start = -1
        for i in range(len(segments)):
            duration = segments[i]
            duration = max(duration, 0.02)
            ax.broken_barh([(start, duration)], (0, 12), facecolors=colors[i])
            ax.text(start, -1.5, f"{start:.2f}s", ha='center', fontsize=7, color='gray')

            # ✅ 겹치면 화살표 + 텍스트
            if abs(start - prev_start) < 1e-2:
                ax.annotate(f"{labels[i]} ({duration:.2f}s)",
                            xy=(start + duration / 2, 12),
                            xytext=(start + duration / 2, 18),
                            arrowprops=dict(arrowstyle="->", lw=1.2, color='black'),
                            ha='center', fontsize=9, color='black')
            else:
                label_y = 9 if i % 2 == 0 else 11
                ax.text(start + duration / 2, label_y, labels[i], ha='center', va='center', fontsize=8)

            prev_start = start
            start += duration

        ax.text(start, -1.5, f"{start:.2f}s", ha='center', fontsize=7, color='gray')

        ax.set_xlim(0, max(total + 0.2, 1.0))
        ax.set_ylim(-2, 20)
        ax.set_yticks([])
        ax.set_xlabel("Time (sec)", fontsize=9)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)

        chart_path = "gantt_log_chart.png"
        plt.tight_layout()
        plt.savefig(chart_path)
        plt.close()
        return chart_path
    except Exception as e:
        print(f"[Gantt Chart 생성 실패] {e}")
        return None



def generate_final_pdf_report(file: UploadFile, result: dict, model_name=None):
    model_type = result.get("model_info", {}).get("type") or model_name or "Unknown"

    """
    출력 아래와 같이 나와야 함
    result = {
        "confidence": 0.87,
        "accuracy": 95.61,
        "result": "악성",
        "log": {
            "start_time": "2025/04/07 14:22:10",
            "model_load": 0.91,
            "preprocess": 0.72,
            "inference": 1.07
        },
        "model_info": {
            "type": "CNN",
            "input": "Grayscale, 256x256",
            "train_size": "20,000"
        }
    }
    """
    def create_pie_chart(malicious_percent):
        benign_percent = 100 - malicious_percent
        labels = ['악성 : {:.1f}%'.format(malicious_percent), '정상 : {:.1f}%'.format(benign_percent)]
        sizes = [malicious_percent, benign_percent]
        colors = ['#C084FC', '#93C5FD']

        fig, ax = plt.subplots(figsize=(3.5, 3.5))
        ax.pie(sizes, labels=['Malicious', 'Benign'], colors=colors,
               autopct='%1.1f%%', startangle=90, textprops={'fontsize': 10})
        ax.axis('equal')
        plt.legend(labels, loc="center left", bbox_to_anchor=(1, 0.5), fontsize=10)

        chart_path = "pie_chart.png"
        plt.savefig(chart_path, bbox_inches='tight')
        plt.close()
        return chart_path

    contents = file.file.read()
    file_name = file.filename
    extension = os.path.splitext(file_name)[1]
    file_size = f"{len(contents) / 1024 / 1024:.2f} MB"
    file_hash = hashlib.sha256(contents).hexdigest()

    confidence = result["confidence"]
    test_acc = result["accuracy"]
    detection_result = result["result"]

    now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    malicious_percent = round(confidence * 100, 1)
    chart_path = create_pie_chart(malicious_percent)

    pdf = CustomPDF()  
    pdf.alias_nb_pages() # 하단 페이지 개수
    pdf.add_page()


    font_dir = os.path.join(os.path.dirname(__file__), "../assets/fonts")
    pdf.add_font("Noto", "", os.path.join(font_dir, "NotoSansKR-Regular.ttf"))
    pdf.add_font("Noto", "B", os.path.join(font_dir, "NotoSansKR-Bold.ttf"))

    logo_path = os.path.join(os.path.dirname(__file__), "../assets/images/report_logo.png")
    pdf.image(logo_path, x=10, y=10, w=45)
    pdf.set_xy(150, 10)
    pdf.set_font("Noto", "", 9)
    pdf.multi_cell(0, 6, "65, Chosundae 5-gil, Dong-gu\nSouth Korea, Gwangju 61452\nhttps://ict.chosun.ac.kr", align='R')

    pdf.set_xy(10, 38)
    pdf.set_font("Noto", "B", 18)
    pdf.cell(0, 10, "Malicious File Analysis Report", align='L')
    pdf.ln(10)
    pdf.set_font("Noto", "", 12)
    pdf.cell(0, 10, now)
    pdf.ln(12)

    pdf.set_font("Noto", "B", 14)
    pdf.cell(0, 10, "1. 파일 분석 정보 (File analysis information)")
    pdf.ln(12)
    pdf.set_font("Noto", "", 12)
    pdf.set_x(15)
    table_data = [
        ["File name", file_name],
        ["File Size", file_size],
        ["Extension", extension],
        ["SHA-256 Hash", file_hash]
    ]
    for row in table_data:
        pdf.set_x(15)
        pdf.cell(40, 10, row[0], border=1)
        pdf.cell(150, 10, row[1], border=1)
        pdf.ln()
    pdf.ln(8)

    pdf.set_font("Noto", "B", 14)
    pdf.cell(0, 10, "2. 탐지 결과 요약 (Summary of Detection Results)")
    pdf.ln(10)
    pdf.set_font("Noto", "", 12)
    pdf.cell(0, 10, f"탐지 결과 : {detection_result}")
    pdf.ln(8)
    pdf.cell(0, 10, f"신뢰도 (Confidence) : {test_acc:.2f} %")
    pdf.ln(8)

    pdf.set_text_color(100)
    pdf.set_font("Noto", "", 10)
    pdf.multi_cell(0, 8, "※ 본 보고서에서의 신뢰도는 모델의 성능을 의미합니다.")
    pdf.set_text_color(0)
    pdf.set_font("Noto", "", 12)
    pdf.ln(10)

    image_width = 100
    x_centered = (pdf.w - image_width) / 2
    pdf.image(chart_path, x=x_centered, w=image_width)
    pdf.ln(10)

    pdf.cell(0, 10, f"해당 \"{file_name}\" 파일은 {detection_result}으로 탐지되었으며,", align='C')
    pdf.ln(8)
    pdf.cell(0, 10, f"{malicious_percent:.1f}%의 탐지 확률을 기반으로 판단됩니다.", align='C')
    pdf.ln(10)

    pdf.set_text_color(100)
    pdf.set_font("Noto", "", 10)
    lines = [
        "※ 본 보고서에서는 악성 및 정상 중 예측 확률이 더 높은 값을 기준으로 판별하며,",
        "악성 확률이 60% 이상일 경우 '악성'으로 판별합니다."
    ]
    for line in lines:
        pdf.cell(0, 6, line, align='C')
        pdf.ln(6)
    pdf.set_text_color(0)
    pdf.ln(8)

    model_info = extract_model_info(extension)
    model_type = model_info.get("type", "Unknown")
    input_info = model_info.get("input", "-")
    train_size = model_info.get("train_size", "-")

    pdf.set_font("Noto", "B", 14)
    pdf.cell(0, 10, "3. 분석 환경 (AI Models Used)")
    pdf.ln(10)
    pdf.set_font("Noto", "", 12)
    pdf.multi_cell(0, 8,
        f"{model_type} 기반의 머신러닝 모델을 사용하여 파일을 분석하였습니다.\n"
        f"해당 모델은 약 {train_size}개의 학습 데이터를 기반으로 학습되었으며,\n"
        f"{input_info} 형태로 전처리된 데이터를 사용합니다.\n"
        f"모델의 테스트 정확도는 {test_acc:.2f}%입니다."
    )
    pdf.ln(6)
    # 모델 성능 점수 자동 추출 : F1/Recall/Precision, Benign/Malware 클래스 정확도 시각화 함수
    perf = get_model_performance_score(extension)
    combined_chart_path = create_combined_model_performance_chart(perf)

    # 3. PDF에 삽입
    if os.path.exists(combined_chart_path):
        pdf.image(combined_chart_path, x=pdf.l_margin + 10, w=pdf.w - 2 * (pdf.l_margin + 10))
        pdf.ln(10)

    # 4. 이미지 파일 정리
    if os.path.exists(combined_chart_path):
        os.remove(combined_chart_path)


    log = result.get("log", {})
    pdf.set_font("Noto", "B", 14)
    pdf.cell(0, 10, "4. 분석 로그 요약 (Analysis Log Summary)")
    pdf.ln(10)
    pdf.set_font("Noto", "", 12)
    pdf.multi_cell(0, 8,
        f"- 분석 시작 시간: {log.get('start_time', '-')}\n"
        f"- 모델 로딩 시간: {log.get('model_load', '-')}초\n"
        f"- 파일 전처리 시간: {log.get('preprocess', '-')}초\n"
        f"- 추론 시간: {log.get('inference', '-')}초"
    )
    pdf.ln(8)
    try:
        model_load = float(log.get('model_load', 0))
        preprocess = float(log.get('preprocess', 0))
        inference = float(log.get('inference', 0))

        gantt_chart_path = create_log_gantt_chart(model_load, preprocess, inference)

        if gantt_chart_path and os.path.exists(gantt_chart_path):
            pdf.image(gantt_chart_path, x=pdf.l_margin + 10, w=pdf.w - 2 * (pdf.l_margin + 10))
            pdf.ln(10)
            os.remove(gantt_chart_path)
    except Exception as e:
        print(f"[PDF] 로그 시각화 실패: {e}")



    pdf.set_font("Noto", "B", 14)
    pdf.cell(0, 10, "5. 대응 및 권장 조치 (Response and Recommended Actions)")
    pdf.ln(10)
    pdf.set_font("Noto", "", 12)
    pdf.multi_cell(0, 8,
        "- 백신 프로그램으로 전체 검사 수행\n"
        "- 출처가 불분명한 첨부파일 실행 금지\n"
        "- 샌드박스 환경에서 파일 실행 권장\n"
        "- 운영체제 및 보안 프로그램 최신 상태 유지\n"
        "- 중요 데이터는 주기적으로 백업"
    )
    

    output_dir = "/Users/yoonhyejun/Desktop/pdf_output"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{file_name}_report.pdf")
    pdf.output(output_path)

    if os.path.exists(chart_path):
        os.remove(chart_path)

    return output_path