import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import MAIL_FROM, MAIL_TO, SMTP, SMTP_PORT, PASSWORD


def send_mail():
    with open('mail.html', 'r', encoding='utf-8') as f:
        email_content = f.read()

        msg = MIMEMultipart('alternative')  # Создаем сообщение
        msg['From'] = MAIL_FROM  # Адресат
        msg['To'] = MAIL_TO  # Получатель
        msg['Subject'] = 'Заказы к сборке Wildberries'  # Тема сообщения

        msg.attach(MIMEText(email_content, 'html'))  # Добавляем в сообщение HTML-фрагмент

        server = smtplib.SMTP(SMTP, SMTP_PORT)  # Создаем объект SMTP
        server.starttls()
        server.login(MAIL_FROM, PASSWORD)
        server.send_message(msg)
        server.quit()
