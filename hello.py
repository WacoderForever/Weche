import os
from dotenv import load_dotenv
from flask import Flask, render_template, url_for, redirect, session
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired,Length
from flask_wtf.csrf import CSRFProtect

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY','default_secret_key')
app.config['DEBUG'] = True
csrf = CSRFProtect(app)
bootstrap = Bootstrap(app)
moment = Moment(app)

class NameForm(FlaskForm):
    name = StringField("What is your name?",validators=[DataRequired(),Length(min=2,max=20)])
    submit = SubmitField("Submit")

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        return redirect(url_for('index'))
    else:
        session['name']=session.get('name','')

    return render_template('index.html', current_time=datetime.utcnow(), name=session.get('name'), form=form)

@app.route('/user/<string:name>')
def user(name):
    return render_template('user.html', name=name)

@app.route('/invalid')
def not_found():
    return render_template('404.html')

if __name__ == '__main__':
    app.run(port=5027)
