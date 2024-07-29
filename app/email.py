from threading import Thread
from . import mail
from flask_mail import Message
from flask import current_app, render_template
from .auth.oauth2 import get_authenticated_client
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

def send_async_email(app, message):
    with app.app_context():
        mail.send(message)

def send_email(to, subject, template, **kwargs):
    creds = get_authenticated_client()
    app = current_app._get_current_object()
    msg = Message(app.config['WECHE_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                  sender=app.config['WECHE_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)

    # Build the Gmail service
    service = build('gmail', 'v1', credentials=creds)

    # Create a message object
    raw_message = create_message(app.config['WECHE_MAIL_SENDER'], to, subject, msg.html, msg.body)

    # Send the email using the Gmail API
    send_message(service, 'me', raw_message)

    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr

def create_message(sender, to, subject, html, text):
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    import base64

    message = MIMEMultipart('alternative')
    message['Subject'] = subject
    message['From'] = sender
    message['To'] = to

    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    message.attach(part1)
    message.attach(part2)

    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {'raw': raw_message}

def send_message(service, user_id, message):
    try:
        message = service.users().messages().send(userId=user_id, body=message).execute()
        print(f'Message Id: {message["id"]}')
        return message
    except Exception as error:
        print(f'An error occurred: {error}')
        raise
