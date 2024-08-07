from datetime import datetime
from flask import render_template, session, redirect, url_for,flash,current_app
from . import main
from .forms import NameForm
from .. import db
from ..models import User

@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        user = User.query.filter_by(username=form.name.data).first()
        if old_name is not None and old_name != form.name.data:
            flash("Looks like you have changed your name!")

        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False

            if current_app.config['FLASKY_ADMIN']:
                send_mail(current_app.config['FLASKY_ADMIN'], 'New user', 'mail/new_user', user=user)
        else:
            session['known'] = True

        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('main.index'))
    else:
        session['name'] = session.get('name', '')

    return render_template('index.html', current_time=datetime.utcnow(), name=session.get('name'),
                           form=form, known=session.get('known', False))

@main.route('/user/<username>')
def user(username):
    user=User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    return render_template('user.html',user=user)