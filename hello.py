from flask import Flask,render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime

app=Flask(__name__)
bootstrap=Bootstrap(app)
moment=Moment(app)

app.config['DEBUG']=True

@app.route('/')
def main():
    return render_template('index.html',current_time=datetime.utcnow(),_external=True)

@app.route('/user/<string:name>')
def user(name):
    return render_template('user.html',name=name,_external=True)

@app.route('/invalid')
def not_found():
    return render_template('404.html',_external=True)

if __name__=='__main__':
    app.run(port=5015)