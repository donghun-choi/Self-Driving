from flask import * # type: ignore
import datetime as dt
import cv2
import time
from werkzeug.serving import WSGIRequestHandler
import numpy as np
app = Flask(__name__)
app.config['SECRET_KEY'] = f'yesla%%@#!$DDD DROP database;; setmean;;;'
app.config["PERMANENT_SESSION_LIFETIME"] = dt.timedelta(minutes=60)

camera = cv2.VideoCapture(0)
frame_delay = 1 / 30  # Delay for 30 FPS

from car import Car
Yesla = Car()

print("waiting for sensors")
time.sleep(1)


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


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/datatrans')
def asdf():
    info = Yesla.getInfo()
    # return Response(generate_data(), mimetype='text/plain')
    return Response(str(info['steeringAngleDeg']), mimetype='text/plain')


def gen_frames():
    prev_frame_time = time.time()
    
    while True:
        success, frame = camera.read()
        if not success:
            break
        
        else:
            frame = cv2.resize(frame, (320, 240))  # 원하는 해상도로 크기 조정
            frame = cv2.GaussianBlur(frame, (15, 15), 0)
            # frame = cv2.Canny(frame,threshold1=3,threshold2=64)
            # frame = cv2.cvtColor(frame,cv2.COLOR_RGB2HSV)
            ret, buffer = cv2.imencode('.jpeg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        # Delay to achieve the desired frame rate
        curr_frame_time = time.time()
        time_diff = curr_frame_time - prev_frame_time
        if time_diff < frame_delay:
            time.sleep(frame_delay - time_diff)
        prev_frame_time = curr_frame_time


# WSGIRequestHandler.protocol_version = "HTTP/1.1"
PORT=5001
isDebugMode = True
if __name__ == '__main__':
   app.run(debug=isDebugMode, host='0.0.0.0',port=PORT)
