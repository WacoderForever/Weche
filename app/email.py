from threading import Thread
from flask_mail import Message
from flask import current_app, render_template
from .auth.oauth2 import get_authenticated_client
from googleapiclient.errors import HttpError
import base64

def send_async_email(app, message):
    with app.app_context():
        mail.send(message)

def send_email(to, subject, template, **kwargs):
    creds = get_authenticated_client()
    app = current_app._get_current_object()
    msg = Message(
        app.config['WECHE_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
        sender=app.config['WECHE_MAIL_SENDER'],
        recipients=[to]
    )
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)

    try:
        service = build('gmail', 'v1', credentials=creds)
        message_body = {
            'raw': base64.urlsafe_b64encode(msg.as_bytes()).decode('utf-8')
        }
        send_message = service.users().messages().send(userId="me", body=message_body).execute()
        print(f"Message Id: {send_message['id']}")
    except HttpError as error:
        print(f"An error occurred: {error}")
        return None

    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr
