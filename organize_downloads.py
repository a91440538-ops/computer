import os, shutil, sys
from pathlib import Path

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

def get_category(ext):
    for category, exts in CATEGORIES.items():
        if ext.lower() in exts:
            return category
    return '기타'

def organize(dry_run=True):
    moved = []
    for f in DOWNLOADS.iterdir():
        if f.is_dir():
            continue
        category = get_category(f.suffix)
        dest_dir = DOWNLOADS / category
        dest = dest_dir / f.name

        if dry_run:
            print(f"{f.name} → {category}/")
        else:
            dest_dir.mkdir(exist_ok=True)
            if dest.exists():
                dest = dest_dir / (f.stem + '_dup' + f.suffix)
            shutil.move(str(f), str(dest))
            moved.append(f.name)

    if dry_run:
        print(f"\n총 {len(list(DOWNLOADS.iterdir()))}개 파일 이동 예정")
    else:
        print(f"\n완료! {len(moved)}개 파일 정리됨")

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'run':
        print("정리 시작...")
        organize(dry_run=False)
    else:
        print("=== 미리보기 (실제로 이동 안 함) ===\n")
        organize(dry_run=True)
        print("\n실제로 정리하려면: python organize_downloads.py run")
