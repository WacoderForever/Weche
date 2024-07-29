from threading import Thread
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from flask import current_app, render_template
from .auth.oauth2 import build_service
import base64
from email.mime.text import MIMEText

def send_async_email(app, message):
    with app.app_context():
        mail.send(message)

def send_email(to, subject, template, **kwargs):
    service = build_service()
    app = current_app._get_current_object()
    msg = MIMEText(render_template(template + '.html', **kwargs), 'html')
    msg['to'] = to
    msg['from'] = app.config['WECHE_MAIL_SENDER']
    msg['subject'] = app.config['WECHE_MAIL_SUBJECT_PREFIX'] + ' ' + subject
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    raw_message = {'raw': raw}
    try:
        send_message(service, 'me', raw_message)
    except HttpError as error:
        print(f'An error occurred: {error}')
        raise Exception(f'An error occurred: {error}')

def send_message(service, user_id, message):
    try:
        message = service.users().messages().send(userId=user_id, body=message).execute()
        print(f'Message Id: {message["id"]}')
        return message
    except HttpError as error:
        print(f'An error occurred: {error}')
        raise Exception(f'An error occurred: {error}')
