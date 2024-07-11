import os
from dotenv import load_dotenv
from flask import Flask, render_template, url_for, redirect, session ,flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired,Length
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY','default_secret_key')
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'

csrf = CSRFProtect(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
db=SQLAlchemy(app)

class Role(db.Model):
    __tablename__='role'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(20),unique=True)
    users=db.Relationship('User',backref='role',lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name

class User(db.Model):
    __tablename__='users'
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(64),unique=True,index=True)
    role_id=db.Column(db.Integer,db.ForeignKey('role.id'))

    def __repr(self):
        return '<User %r>' % self.username

class NameForm(FlaskForm):
    name = StringField("What is your name?",validators=[DataRequired(),Length(min=2,max=20)])
    submit = SubmitField("Submit")

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name=session.get('name')
        user=User.query.filter_by(username=form.name.data).first()
        if old_name is not None and old_name != form.name.data:
            flash("Looks like you have changed your name!")

        if user is None:
            user=User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known']=False
        else:
            session['known']=True

        session['name'] = form.name.data
        form.name.data=''
        return redirect(url_for('index'))
    else:
        session['name']=session.get('name','')

    return render_template('index.html', current_time=datetime.utcnow(), name=session.get('name'),
                            form=form,known=session.get('known',False))

@app.route('/user/<string:name>')
def user(name):
    return render_template('user.html', name=name)

@app.route('/invalid')
def not_found():
    return render_template('404.html')

if __name__ == '__main__':
    app.run(port=5001)
