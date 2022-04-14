import json
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from .email_template import html_email_template


FROM_EMAIL = os.environ['FROM_EMAIL']
PASSWORD = os.environ['FROM_EMAIL_PASSWORD']


def create_message(data):
    msg = MIMEMultipart()
    msg["Subject"] = "[Team schedule] - Email confirmation"

    message = html_email_template.format(name=data['login'], confirmation_link=data['link'])
    msg.attach(MIMEText(message, 'html'))
    return msg


def send_email(ch, method, properties, body):
    email_data = json.loads(body.decode())
    msg = create_message(email_data)
    to_email = email_data['email']

    server = smtplib.SMTP('smtp.gmail.com: 587')
    server.starttls()
    server.login(FROM_EMAIL, PASSWORD)

    server.sendmail(FROM_EMAIL, to_email, msg.as_string())
    server.quit()

    # mark message as processed
    ch.basic_ack(delivery_tag=method.delivery_tag)
