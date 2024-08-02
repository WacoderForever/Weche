from threading import Thread
from . import mail
from flask_mail import Message
from flask import current_app

def send_async_email(app,message):
    with app.app_context():
        mail.send(msg)

def send_email(to,subject,template,**kwargs):
    app=current_app._get_current_object()
    msg=Message(app.config['WECHE_MAIL_SUBJECT_PREFIX'] + ' '+ subject,
                sender=app.config['WECHE_MAIL_SENDER'])