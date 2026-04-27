import pickle, base64, os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from googleapiclient.discovery import build

with open('C:/Users/a9144/Projects/gmail_token.pkl', 'rb') as f:
    creds = pickle.load(f)

service = build('gmail', 'v1', credentials=creds)

msg = MIMEMultipart()
msg['To'] = 'a91440538@gmail.com'
msg['From'] = 'a91440538@gmail.com'
msg['Subject'] = 'Unity 스크립트 코드 설명서'
msg.attach(MIMEText('Unity 코드 설명 PDF입니다.', 'plain', 'utf-8'))

pdf_path = 'C:/Users/a9144/Projects/computer/unity_code_explanation.pdf'
with open(pdf_path, 'rb') as f:
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(f.read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', 'attachment', filename='Unity_코드설명서.pdf')
msg.attach(part)

raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
service.users().messages().send(userId='me', body={'raw': raw}).execute()
print("전송 완료")
