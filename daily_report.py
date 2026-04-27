import os, sys, base64, requests, schedule, time, urllib.request, json, pickle
from datetime import datetime, timezone, timedelta
from email.mime.text import MIMEText
from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding='utf-8')
load_dotenv()

OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')
MY_EMAIL = 'a91440538@gmail.com'
CANVAS_TOKEN = '7hNLvjKjgwKNrBVdS6B4a9dQsBLJEVxkCIPD7qHO9fppy76f2axw8suj2ipyjj1I'
CANVAS_COURSES = {
    71677: '스타트업경영',
    70421: 'AI and Business',
    70448: 'Consumer Behavior',
    70469: 'Elementary Business Statistics',
    70456: 'Financial Management',
}
SCOPES = [
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/calendar',
]

def get_google_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    gmail = build('gmail', 'v1', credentials=creds)
    calendar = build('calendar', 'v3', credentials=creds)
    return gmail, calendar

def get_weather():
    url = f"http://api.openweathermap.org/data/2.5/weather?q=Jongno-gu,Seoul,KR&appid={OPENWEATHER_API_KEY}&units=metric&lang=kr"
    res = requests.get(url).json()
    return {
        'temp': round(res['main']['temp']),
        'feels': round(res['main']['feels_like']),
        'desc': res['weather'][0]['description'],
        'humidity': res['main']['humidity']
    }

def canvas_api(path):
    req = urllib.request.Request(
        f'https://canvas.skku.edu/api/v1{path}',
        headers={'Authorization': f'Bearer {CANVAS_TOKEN}'}
    )
    return json.loads(urllib.request.urlopen(req).read())

def get_todays_assignments():
    today = datetime.now(timezone.utc).date()
    due_today = []
    for course_id, course_name in CANVAS_COURSES.items():
        assignments = canvas_api(f'/courses/{course_id}/assignments?per_page=50&order_by=due_at')
        for a in assignments:
            if not a.get('due_at'):
                continue
            due = datetime.fromisoformat(a['due_at'].replace('Z', '+00:00'))
            if due.astimezone().date() == today:
                due_today.append(f"[{course_name}] {a['name']} ({due.astimezone().strftime('%H:%M')} 마감)")
    return due_today

def sync_assignments_to_calendar(calendar_service):
    # Canvas에서 현재 유효한 과제 가져오기
    canvas_assignments = {}  # assignment_id -> (course_name, name, due)
    for course_id, course_name in CANVAS_COURSES.items():
        assignments = canvas_api(f'/courses/{course_id}/assignments?per_page=50&order_by=due_at')
        for a in assignments:
            if not a.get('due_at'):
                continue
            due = datetime.fromisoformat(a['due_at'].replace('Z', '+00:00'))
            if due > datetime.now(timezone.utc):
                canvas_assignments[a['id']] = (course_name, a['name'], due, a.get('html_url', ''))

    # 캘린더에서 Canvas 과제 이벤트 가져오기
    events_result = calendar_service.events().list(
        calendarId='primary',
        q='Canvas 과제 마감',
        timeMin=datetime.now(timezone.utc).isoformat(),
        maxResults=100,
        singleEvents=True
    ).execute()
    calendar_events = events_result.get('items', [])

    # 캘린더 이벤트를 assignment_id로 매핑
    cal_event_map = {}
    for e in calendar_events:
        desc = e.get('description', '')
        for aid in canvas_assignments:
            if str(aid) in desc:
                cal_event_map[aid] = e['id']

    added = []
    deleted = []

    # 캘린더에 있는데 Canvas에 없는 과제 삭제
    for aid, event_id in cal_event_map.items():
        if aid not in canvas_assignments:
            calendar_service.events().delete(calendarId='primary', eventId=event_id).execute()
            deleted.append(event_id)

    # Canvas에 있는데 캘린더에 없는 과제 추가
    for aid, (course_name, name, due, url) in canvas_assignments.items():
        if aid not in cal_event_map:
            event = {
                'summary': f"[{course_name}] {name}",
                'description': f"Canvas 과제 마감\nassignment_id:{aid}\n{url}",
                'start': {'dateTime': due.isoformat(), 'timeZone': 'Asia/Seoul'},
                'end': {'dateTime': (due + timedelta(hours=1)).isoformat(), 'timeZone': 'Asia/Seoul'},
                'reminders': {'useDefault': False, 'overrides': [
                    {'method': 'popup', 'minutes': 60},
                    {'method': 'popup', 'minutes': 1440},
                ]},
            }
            calendar_service.events().insert(calendarId='primary', body=event).execute()
            added.append(f"[{course_name}] {name}")

    return added, deleted

def send_report():
    today = datetime.now().strftime('%Y-%m-%d')
    gmail, calendar = get_google_service()

    weather = get_weather()
    due_today = get_todays_assignments()
    added, deleted = sync_assignments_to_calendar(calendar)

    body = f"""안녕하세요! 오늘의 일일 리포트입니다.

━━━━━━━━━━━━━━━━━━
오늘 날씨 (서울 종로구)
━━━━━━━━━━━━━━━━━━
기온: {weather['temp']}C (체감 {weather['feels']}C)
날씨: {weather['desc']}
습도: {weather['humidity']}%
"""

    if due_today:
        body += "\n━━━━━━━━━━━━━━━━━━\n오늘 마감 과제\n━━━━━━━━━━━━━━━━━━\n"
        body += '\n'.join(f"- {d}" for d in due_today)
        body += '\n'
    else:
        body += "\n오늘 마감 과제 없음\n"

    if added:
        body += "\n━━━━━━━━━━━━━━━━━━\n캘린더에 새로 추가된 과제\n━━━━━━━━━━━━━━━━━━\n"
        body += '\n'.join(f"- {e}" for e in added)
        body += '\n'

    if deleted:
        body += f"\n캘린더에서 삭제된 과제: {len(deleted)}개\n"

    body += "\n좋은 하루 되세요!"

    msg = MIMEText(body)
    msg['To'] = MY_EMAIL
    msg['From'] = MY_EMAIL
    msg['Subject'] = f'[일일 리포트] {today}'
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    gmail.users().messages().send(userId='me', body={'raw': raw}).execute()
    print(f"{today} 리포트 전송 완료")

schedule.every().day.at("09:00").do(send_report)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        print("테스트 전송 중...")
        send_report()
    else:
        print("일일 리포트 스케줄러 시작 (매일 09:00)")
        while True:
            schedule.run_pending()
            time.sleep(60)
