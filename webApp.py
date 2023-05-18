from flask import * # type: ignore
from flask import render_template
import datetime as dt
from flask import url_for


app = Flask(__name__)
app.config['SECRET_KEY'] = f'yesla%%@#!$DDD DROP database;; setmean;;;'
app.config["PERMANENT_SESSION_LIFETIME"] = dt.timedelta(minutes=60)


def ifLogin():
    if 'user' in session:
        return True
    return False


@app.route('/')
def index():
    return redirect(url_for('main'))


@app.route('/main')
def main():
    if ifLogin():
        return render_template('main.html',maincsspath='../static/css/main.css')
    return redirect(url_for('login'))



@app.route('/login')
def login():
    if ifLogin():
        return redirect(url_for('main'))
    return render_template('login.html',logincsspath='../static/css/login.css')


@app.route('/loginpost',methods=['POST','GET']) #type:ignore
def loginPost():
    if request.method == 'POST':
        username = request.form.get('userName')
        userPassword = request.form.get('userPassword')
        
        
        if username == 'admin' and userPassword == 'admin':
            session['user'] = username
            return redirect(url_for('main'))
        
        
        return redirect(url_for('main'))
    elif request.method == 'GET':
        return redirect(url_for('main'))
        pass
    pass

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('main'))


PORT=5001
isDebugMode = True
if __name__ == '__main__':
   app.run(debug=isDebugMode, host='0.0.0.0',port=PORT)
