from threading import Thread
from flask import current_app, render_template
from .auth.oauth2 import get_authenticated_client
from googleapiclient.errors import HttpError
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_async_email(service, message):
    try:
        message = service.users().messages().send(userId="me", body=message).execute()
        print(f"Message Id: {message['id']}")
    except HttpError as error:
        print(f"An error occurred: {error}")

def create_message(sender, to, subject, body_text, body_html):
    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject

    msg_text = MIMEText(body_text, 'plain')
    msg_html = MIMEText(body_html, 'html')

    message.attach(msg_text)
    message.attach(msg_html)

    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
    return {'raw': raw_message}

def send_email(to, subject, template, **kwargs):
    # Get the authenticated Gmail client
    service = get_authenticated_client()

    # Build the email message
    sender = current_app.config['WECHE_MAIL_SENDER']
    subject = current_app.config['WECHE_MAIL_SUBJECT_PREFIX'] + ' ' + subject
    body_text = render_template(template + '.txt', **kwargs)
    body_html = render_template(template + '.html', **kwargs)
    
    message = create_message(sender, to, subject, body_text, body_html)
    
    # Send the email asynchronously
    thr = Thread(target=send_async_email, args=[service, message])
    thr.start()
    return thr
