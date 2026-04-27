import sys
sys.path.insert(0, 'C:/Users/a9144/Projects/computer')

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from gmail_sender import send_with_file

PDF_PATH = "C:/Users/a9144/Projects/computer/learning_summary.pdf"

pdfmetrics.registerFont(TTFont('Malgun', 'C:/Windows/Fonts/malgun.ttf'))
pdfmetrics.registerFont(TTFont('MalgunBold', 'C:/Windows/Fonts/malgunbd.ttf'))
pdfmetrics.registerFontFamily('Malgun', normal='Malgun', bold='MalgunBold')

T  = ParagraphStyle('T',  fontName='MalgunBold', fontSize=18, leading=28, spaceAfter=6)
H  = ParagraphStyle('H',  fontName='MalgunBold', fontSize=13, leading=22, spaceBefore=10, spaceAfter=4)
H2 = ParagraphStyle('H2', fontName='MalgunBold', fontSize=11, leading=18, spaceBefore=6, spaceAfter=2)
NM = ParagraphStyle('NM', fontName='Malgun',     fontSize=11, leading=18)
BL = ParagraphStyle('BL', fontName='Malgun',     fontSize=11, leading=18, leftIndent=16)
CD = ParagraphStyle('CD', fontName='Malgun',     fontSize=10, leading=16, backColor='#eeeeee', leftIndent=8, rightIndent=8, spaceBefore=2, spaceAfter=2)

def sec(title):
    return [HRFlowable(width="100%", thickness=1, color='#cccccc', spaceAfter=4),
            Paragraph(title, H)]

c = []

c.append(Paragraph("Python 자동화 학습 요약", T))
c.append(Paragraph("Phase 1 챕터 1~3  |  2026-04-27", NM))
c.append(Spacer(1, 5*mm))

# ── 챕터 1 ──
c += sec("챕터 1 — Python 기초")
c.append(Paragraph("<b>이해해야 할 것</b>", H2))
c.append(Paragraph("• 함수: 재료를 넣으면 결과를 돌려주는 기계", BL))
c.append(Paragraph("• 조건문(if): 상황에 따라 다르게 실행", BL))
c.append(Paragraph("• 반복문(for/while): 같은 작업을 여러 번 자동으로", BL))
c.append(Paragraph("<b>외워야 할 것</b>", H2))
c.append(Paragraph("• 없음 — 흐름과 논리만", BL))
c.append(Spacer(1, 3*mm))

# ── 챕터 2 ──
c += sec("챕터 2 — API 다루기")
c.append(Paragraph("<b>이해해야 할 것</b>", H2))
c.append(Paragraph("• API: 다른 서비스에 '요청'을 보내고 '결과'를 받는 방식", BL))
c.append(Paragraph("• .env 파일: API 키 같은 비밀 정보는 코드에 직접 쓰지 않고 분리", BL))
c.append(Paragraph("• requests.get(): 인터넷에서 데이터 가져오는 흐름", BL))
c.append(Paragraph("• 실제 연동 완료: 날씨, Canvas 공지, Gmail", BL))
c.append(Paragraph("<b>외워야 할 것</b>", H2))
c.append(Paragraph("• 없음", BL))
c.append(Spacer(1, 3*mm))

# ── 챕터 3 ──
c += sec("챕터 3 — 파일 자동화 (pathlib, schedule)")
c.append(Paragraph("<b>이해해야 할 것</b>", H2))
c.append(Paragraph("• pathlib.Path: 파일/폴더 경로를 문자열이 아닌 '객체'로 다루는 방식", BL))
c.append(Paragraph("• .iterdir(): 폴더 안을 하나씩 꺼내서 처리하는 흐름", BL))
c.append(Paragraph("• .suffix / .name: 확장자와 파일 이름을 꺼내는 법", BL))
c.append(Paragraph("• dry_run 패턴: 실행 전 미리보기로 실수 방지 — 실무 필수 습관", BL))
c.append(Paragraph("• schedule: 예약 설정(every/at) + while True로 대기하는 세트 구조", BL))
c.append(Paragraph("• 함수(get_category)는 확장자를 넣으면 카테고리 이름을 돌려줌", BL))
c.append(Spacer(1, 2*mm))
c.append(Paragraph("<b>핵심 코드 패턴</b>", H2))
c.append(Paragraph("폴더 안 파일 순회:", NM))
c.append(Paragraph("for f in Path('경로').iterdir():  →  f.name, f.suffix 사용", CD))
c.append(Paragraph("schedule 예약 실행:", NM))
c.append(Paragraph("schedule.every().day.at('09:00').do(함수)  +  while True: run_pending()", CD))
c.append(Paragraph("<b>외워야 할 것</b>", H2))
c.append(Paragraph("• 없음 — 검색해서 쓰면 됨. 흐름만 기억", BL))
c.append(Spacer(1, 5*mm))

c += sec("전체 원칙")
c.append(Paragraph("• 문법은 외우지 않는다 — 흐름과 논리를 이해한다", BL))
c.append(Paragraph("• Claude가 만든 코드는 분해해서 읽는 연습을 한다", BL))
c.append(Paragraph("• 짧은 코드라도 직접 실행해보는 것이 가장 빠른 이해 방법", BL))
c.append(Paragraph("• dry_run처럼 '안전하게 먼저 확인' 하는 습관을 들인다", BL))

doc = SimpleDocTemplate(PDF_PATH, pagesize=A4,
    leftMargin=20*mm, rightMargin=20*mm,
    topMargin=20*mm, bottomMargin=20*mm)
doc.build(c)
print("PDF 생성 완료")

send_with_file(
    subject="Python 자동화 학습 요약 - 챕터 1~3",
    message="Phase 1 챕터 1~3 학습 내용 요약 PDF입니다.",
    file_path=PDF_PATH
)
