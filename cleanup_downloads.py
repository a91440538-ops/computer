import sys, os, shutil, hashlib, schedule, time
from pathlib import Path
from collections import defaultdict

sys.stdout.reconfigure(encoding='utf-8')

DOWNLOADS = Path("C:/Users/a9144/Downloads")

CATEGORIES = {
    'PDF':   ['.pdf'],
    'PPT':   ['.ppt', '.pptx'],
    'Word':  ['.doc', '.docx'],
    'HWP':   ['.hwp', '.hwpx'],
    '이미지': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'],
    'Excel': ['.xls', '.xlsx'],
    '압축':  ['.zip', '.rar', '.7z'],
    '기타':  [],
}

def get_hash(filepath):
    h = hashlib.md5()
    with open(filepath, 'rb') as f:
        h.update(f.read())
    return h.hexdigest()

def get_category(ext):
    for category, exts in CATEGORIES.items():
        if ext.lower() in exts:
            return category
    return '기타'

def remove_duplicates():
    hash_map = defaultdict(list)
    for f in DOWNLOADS.rglob('*'):
        if f.is_file():
            try:
                hash_map[get_hash(f)].append(f)
            except:
                pass

    deleted = 0
    for files in hash_map.values():
        if len(files) > 1:
            for f in files[1:]:
                f.unlink()
                deleted += 1
    print(f"중복 삭제: {deleted}개")

def organize():
    moved = 0
    for f in DOWNLOADS.iterdir():
        if f.is_dir():
            continue
        category = get_category(f.suffix)
        dest_dir = DOWNLOADS / category
        dest_dir.mkdir(exist_ok=True)
        dest = dest_dir / f.name
        if dest.exists():
            dest = dest_dir / (f.stem + '_dup' + f.suffix)
        shutil.move(str(f), str(dest))
        moved += 1
    print(f"파일 정리: {moved}개")

def run():
    print(f"다운로드 폴더 정리 시작...")
    remove_duplicates()
    organize()
    print("완료!")

# 매일 자정에 자동 실행
schedule.every().day.at("00:00").do(run)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'run':
        run()
    else:
        print("자동 정리 스케줄러 시작 (매일 자정)")
        while True:
            schedule.run_pending()
            time.sleep(60)
