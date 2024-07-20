from flask import render_template,redirect,url_for,flash,request
from flask_login import login_user
from . import auth
from app.main.forms import LoginForm
from app.models import User

@auth.route('/login',methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user,form.remember_me.data)
            return redirect(request.args.get('next'),'main.index')
        flash('Incorrect email or password')

    return render_template('auth/login.html',form=form)