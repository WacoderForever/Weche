from flask import Flask,render_template
from flask_bootstrap import Bootstrap

app=Flask(__name__)
bootstrap=Bootstrap(app)

app.config['DEBUG']=True

@app.route('/')
def main():
    return render_template('index.html')
@app.route('/user/<string:name>')
def user(name):
    return render_template('user.html',name=name)
@app.route('/invalid')
def not_found():
    return render_template('404.html')

if __name__=='__main__':
    app.run(port=5010)