from threading import Thread
from . import mail
from flask_mail import Message
from flask import current_app,render_template
from .auth.oauth2 import get_authenticated_client

def send_async_email(app,message):
    with app.app_context():
        mail.send(message)

def send_email(to,subject,template,**kwargs):
    creds = get_authenticated_client()
    app=current_app._get_current_object()
    msg=Message(app.config['WECHE_MAIL_SUBJECT_PREFIX'] + ' '+ subject,
                sender=app.config['WECHE_MAIL_SENDER'],recipients=[to])
    msg.body=render_template(template +'.txt',**kwargs)
    msg.html=render_template(template + '.html',**kwargs)
    thr=Thread(target=send_async_email,args=[app,msg])
    thr.start()
    return thr