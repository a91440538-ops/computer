import os
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.send']
MY_EMAIL = 'a91440538@gmail.com'

def get_service():
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
    return build('gmail', 'v1', credentials=creds)

def send_alert(subject, message):
    """알림/문장 보내기"""
    service = get_service()
    msg = MIMEText(message)
    msg['To'] = MY_EMAIL
    msg['From'] = MY_EMAIL
    msg['Subject'] = subject
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    service.users().messages().send(userId='me', body={'raw': raw}).execute()
    print(f"전송 완료: {subject}")

def send_with_file(subject, message, file_path):
    """문서 첨부해서 보내기"""
    service = get_service()
    msg = MIMEMultipart()
    msg['To'] = MY_EMAIL
    msg['From'] = MY_EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEText(message))
    with open(file_path, 'rb') as f:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(file_path)}')
        msg.attach(part)
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    service.users().messages().send(userId='me', body={'raw': raw}).execute()
    print(f"전송 완료 (첨부): {subject}")


# 사용 예시
if __name__ == '__main__':
    # 알림/문장 보내기
    send_alert("테스트 알림", "안녕하세요! 테스트 메일입니다.")

    # 문서 첨부해서 보내기 (파일 경로 바꿔서 사용)
    # send_with_file("문서 전송", "파일을 첨부합니다.", "C:/경로/파일명.pdf")
