import sys, os, subprocess, requests
from pathlib import Path
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

sys.stdout.reconfigure(encoding='utf-8')
load_dotenv(Path('C:/Users/a9144/Projects/computer/.env'))

TOKEN = '8557290326:AAEACzsAqyG1LA9oF8EpYAewYZF4EJ9lbRg'
PROJECT_DIR = Path('C:/Users/a9144/Projects/computer')
WEATHER_KEY = os.getenv('OPENWEATHER_API_KEY')

async def run_script(update, context, script, arg=None):
    await update.message.reply_text("실행 중...")
    try:
        cmd = [sys.executable, str(PROJECT_DIR / script)]
        if arg:
            cmd.append(arg)
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', cwd=str(PROJECT_DIR))
        out = result.stdout.strip() or result.stderr.strip() or "완료"
        await update.message.reply_text(out[:4000])
    except Exception as e:
        await update.message.reply_text(f"오류: {e}")

async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "사용 가능한 명령어\n"
        "\n"
        "/help - 명령어 목록 (이 메시지)\n"
        "/report - 일일 리포트 이메일 전송\n"
        "/dashboard - 대시보드 데이터 갱신\n"
        "/cleanup - 다운로드 폴더 정리 (중복 제거 + 분류)\n"
        "/weather - 현재 날씨 확인 (서울)\n"
        "/summary - 학습 요약 PDF 생성 후 Gmail 전송\n"
        "/file [파일명] - 해당 파일을 채팅으로 전송\n"
        "/list - 프로젝트 파일 목록\n"
        "\n"
        "파일을 이 채팅에 보내면 Downloads 폴더에 자동 저장됩니다."
    )
    await update.message.reply_text(text)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await cmd_help(update, context)

async def cmd_report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await run_script(update, context, 'daily_report.py', 'test')

async def cmd_dashboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await run_script(update, context, 'dashboard.py')

async def cmd_cleanup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await run_script(update, context, 'cleanup_downloads.py', 'run')

async def cmd_weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q=Seoul&appid={WEATHER_KEY}&units=metric&lang=kr"
        data = requests.get(url).json()
        desc = data['weather'][0]['description']
        temp = data['main']['temp']
        feels = data['main']['feels_like']
        humidity = data['main']['humidity']
        text = (
            f"서울 현재 날씨\n"
            f"날씨: {desc}\n"
            f"기온: {temp}°C (체감 {feels}°C)\n"
            f"습도: {humidity}%"
        )
        await update.message.reply_text(text)
    except Exception as e:
        await update.message.reply_text(f"날씨 조회 실패: {e}")

async def cmd_summary(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("PDF 생성 중...")
    try:
        result = subprocess.run(
            [sys.executable, str(PROJECT_DIR / 'send_summary.py')],
            capture_output=True, text=True, encoding='utf-8', cwd=str(PROJECT_DIR)
        )
        if result.returncode == 0:
            await update.message.reply_text("학습 요약 PDF를 Gmail로 전송했습니다.")
        else:
            await update.message.reply_text(f"오류:\n{(result.stderr or result.stdout)[:2000]}")
    except Exception as e:
        await update.message.reply_text(f"오류: {e}")

async def cmd_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("파일명을 입력하세요.\n예: /file dashboard.html")
        return
    filename = ' '.join(context.args)
    filepath = PROJECT_DIR / filename
    if not filepath.exists():
        matches = list(PROJECT_DIR.rglob(f'*{filename}*'))
        if not matches:
            await update.message.reply_text(f"파일을 찾을 수 없습니다: {filename}")
            return
        filepath = matches[0]
    try:
        await update.message.reply_document(document=open(filepath, 'rb'), filename=filepath.name)
    except Exception as e:
        await update.message.reply_text(f"오류: {e}")

async def cmd_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    files = sorted(f.name for f in PROJECT_DIR.iterdir() if f.is_file())
    await update.message.reply_text("프로젝트 파일 목록:\n" + '\n'.join(f"- {f}" for f in files))

async def receive_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    doc = update.message.document
    if not doc:
        return
    save_path = Path('C:/Users/a9144/Downloads') / doc.file_name
    file = await context.bot.get_file(doc.file_id)
    await file.download_to_drive(save_path)
    await update.message.reply_text(f"저장 완료: Downloads/{doc.file_name}")

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("모르는 명령이에요. /help 로 명령 목록 확인하세요.")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler('start', start))
app.add_handler(CommandHandler('help', cmd_help))
app.add_handler(CommandHandler('report', cmd_report))
app.add_handler(CommandHandler('dashboard', cmd_dashboard))
app.add_handler(CommandHandler('cleanup', cmd_cleanup))
app.add_handler(CommandHandler('weather', cmd_weather))
app.add_handler(CommandHandler('summary', cmd_summary))
app.add_handler(CommandHandler('file', cmd_file))
app.add_handler(CommandHandler('list', cmd_list))
app.add_handler(MessageHandler(filters.Document.ALL, receive_file))
app.add_handler(MessageHandler(filters.COMMAND, unknown))

if __name__ == '__main__':
    print("노트북 봇 시작...")
    app.run_polling()
