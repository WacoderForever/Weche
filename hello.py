from flask import Flask,render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import validators,PasswordField,StringField,SubmitField,BooleanField,IntegerField,DateField,DateTimeField

app=Flask(__name__)
bootstrap=Bootstrap(app)
moment=Moment(app)

app.config['DEBUG']=True
app.config["WTF_CSRF_ENABLED"]=False

class NameForm(FlaskForm):
    name=StringField("What is your name?:",[validators.DataRequired(),validators.Length(min=2,max=20)])
    submit=SubmitField("Submit")

@app.route('/',methods=['GET','POST'])
def main():
    name=''
    form=NameForm()

    if form.validate():
        name=form.name.data

    return render_template('index.html',current_time=datetime.utcnow(),_external=True,name=name,form=form)

@app.route('/user/<string:name>')
def user(name):
    return render_template('user.html',name=name,_external=True)

@app.route('/invalid')
def not_found():
    return render_template('404.html',_external=True)

if __name__=='__main__':
    app.run(port=5015)