import os, sys, json, urllib.request, requests
from datetime import datetime, timezone, timedelta
from pathlib import Path
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding='utf-8')
load_dotenv()

OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')
CANVAS_TOKEN = '7hNLvjKjgwKNrBVdS6B4a9dQsBLJEVxkCIPD7qHO9fppy76f2axw8suj2ipyjj1I'
CANVAS_COURSES = {
    71677: '스타트업경영',
    70421: 'AI and Business',
    70448: 'Consumer Behavior',
    70469: 'Elementary Business Statistics',
    70456: 'Financial Management',
}

OUTPUT = Path(__file__).parent / 'dashboard_data.json'

def get_weather():
    url = f"http://api.openweathermap.org/data/2.5/weather?q=Jongno-gu,Seoul,KR&appid={OPENWEATHER_API_KEY}&units=metric&lang=kr"
    res = requests.get(url).json()
    return {
        'temp': round(res['main']['temp']),
        'feels': round(res['main']['feels_like']),
        'desc': res['weather'][0]['description'],
        'humidity': res['main']['humidity'],
        'icon': res['weather'][0]['icon'],
    }

def canvas_api(path):
    req = urllib.request.Request(
        f'https://canvas.skku.edu/api/v1{path}',
        headers={'Authorization': f'Bearer {CANVAS_TOKEN}'}
    )
    return json.loads(urllib.request.urlopen(req).read())

def get_assignments():
    now = datetime.now(timezone.utc)
    today = now.date()
    due_today = []
    upcoming = []

    for course_id, course_name in CANVAS_COURSES.items():
        assignments = canvas_api(f'/courses/{course_id}/assignments?per_page=50&order_by=due_at')
        for a in assignments:
            if not a.get('due_at'):
                continue
            due = datetime.fromisoformat(a['due_at'].replace('Z', '+00:00'))
            if due < now:
                continue
            local_due = due.astimezone()
            item = {
                'course': course_name,
                'name': a['name'],
                'due': local_due.strftime('%m/%d %H:%M'),
                'due_date': local_due.date().isoformat(),
            }
            if local_due.date() == today:
                due_today.append(item)
            else:
                upcoming.append(item)

    upcoming.sort(key=lambda x: x['due_date'])
    return due_today, upcoming[:10]

def main():
    print("데이터 수집 중...")
    weather = get_weather()
    due_today, upcoming = get_assignments()

    data = {
        'updated': datetime.now().strftime('%Y-%m-%d %H:%M'),
        'weather': weather,
        'due_today': due_today,
        'upcoming': upcoming,
    }

    with open(OUTPUT, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"저장 완료: {OUTPUT}")

if __name__ == '__main__':
    main()
