from flask import render_template,redirect,url_for,flash,request,current_user
from flask_login import login_user,logout_user,login_required
from . import auth
from app.main.forms import LoginForm
from app.models import User
from .forms import RegistrationForm
from app import db
from app.email import send_email

@auth.route('/login',methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user,form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Incorrect email or password')

    return render_template('auth/login.html',form=form)

@auth.route('/logout')
def logout():
    logout_user()
    flash("You have been logged out")
    return redirect(url_for('main.index'))

@auth.route('/register',methods=['GET','POST'])
def register():
    form=RegistrationForm()
    if form.validate_on_submit():
        user=User(email=form.email.data,username=form.username.data,password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token=user.generate_confirmation_token()
        send_email(user.email,"Confirm Your Account",'auth/email/confirm',user=user,token=token)
        flash("A confirmation email has been sent to your email")
        return redirect(url_for('main.index'))

    return render_template('auth/register.html',form=form)

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash("You have confirmed your account. Thanks")
    else:
        flash("The link is invalid or expired")
    
    return redirect(url_for('main.index'))