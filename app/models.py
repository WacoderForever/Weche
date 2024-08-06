from datetime import datetime,timedelta
from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
from flask import current_app
import jwt

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    default=db.Column(db.Boolean,default=False,index=True)
    permissions=db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name

class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email=db.Column(db.String,unique=True,index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    password_hash=db.Column(db.String(128))
    confirmed=db.Column(db.Boolean,default=False)

    def generate_confirmation_token(self):
        payload={'confirm':self.id,
                'exp':datetime.now()+timedelta(minutes=4)}
        key=current_app.config['SECRET_KEY']
        algorithm='HS256'

        token=jwt.encode(payload=payload,key=key,algorithm=algorithm)
        return token

    def confirm(self,token):
        algorithm='HS256'
        key=current_app.config['SECRET_KEY']

        try:
            data=jwt.decode(token,key=key,leeway=datetime.timedelta(seconds=10),algorithms=algorithm)
        except:
            return False

        if data.get('confirm') != self.id:
            return False
        self.confirm=True
        db.session.add(self)
        return True

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self,password):
        self.password_hash=generate_password_hash(password)
    
    def verify_password(self,password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username
