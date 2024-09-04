from flask import Flask, render_template, Response, request,session, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import bcrypt
# Required to run the YOLOv8 model
import cv2

# YOLO_Video is the python file which contains the code for our object detection model
#Video Detection is the Function which performs Object Detection on Input Video
from yolo_video import video_detection 
from text_detection import text_detection1



app = Flask(__name__)
cap = None
app.config['SECRET_KEY'] = 'muhammadmoin'

# SQLite database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
app.secret_key = 'secret_key'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True , nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __init__(self,email,password,name):
        self.name =  name
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self,password):
        return bcrypt.checkpw(password.encode('utf-8'),self.password.encode('utf-8'))

#create table
with app.app_context():
    db.create_all()

#function for showing model
def generate_frames_web(path_x):
    yolo_output = video_detection(path_x)
    for detection_ in yolo_output:
        ref,buffer=cv2.imencode('.jpg',detection_)

        frame=buffer.tobytes()
        yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame +b'\r\n')
        
#function for text detection live feed
def text_detection(ocr_path):

    output = text_detection1()
    for a_ in output:
        ref,buffer=cv2.imencode('.jpg',a_)

        frame=buffer.tobytes()
        yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame +b'\r\n')    
        
def release_camera():
   global cap
   if cap is not None:
        cap.release()
        cv2.destroyAllWindows()
        cap = None            

#@app.route('/video')
#def video():
    #return Response(generate_frames(path_x='static/files/bikes.mp4'), mimetype='multipart/x-mixed-replace; boundary=frame')
    #return Response(generate_frames(path_x = session.get('video_path', None)),mimetype='multipart/x-mixed-replace; boundary=frame')



@app.route("/")
def main():
    session.clear()
    return render_template('index.html')


@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        # handle request
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        try:
          new_user = User(name=name,email=email,password=password)
          db.session.add(new_user)
          db.session.commit()
          return redirect(('/login'))
        except IntegrityError:
            db.session.rollback()
            return render_template('register.html', error="Username already exists")
    
    return render_template('register.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            session['email'] = user.email
            return redirect('/dashboard')
        else:
            return render_template('login.html',error='Invalid user')

    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    if session['email']:
        user = User.query.filter_by(email=session['email']).first()
        return render_template('dashboard1.html',user=user)
    
    return redirect('/login')

@app.route('/home')
def home():
    session.clear()
    return render_template('dashboard1.html')

@app.route('/logout')
def logout():
    session.pop('email',None)
    return redirect('/login')

@app.route('/features')
def features():
    
    return render_template('/features.html')




# To display the Output Video on Webcam page
@app.route("/webcam", methods=['GET','POST'])

def webcam():
    session.clear()
    return render_template('object-detection.html')


@app.route('/webapp')
def webapp():
    #return Response(generate_frames(path_x = '../videos/testvideo.mp4'), mimetype='multipart/x-mixed-replace; boundary=frame')
     return Response(generate_frames_web(path_x=0), mimetype='multipart/x-mixed-replace; boundary=frame')
   
@app.route("/webOcr", methods=['GET','POST'])

def webocr():
    session.clear()
    return render_template('text-detection.html')   
@app.route('/ocr')
def ocr_txt():
    ##detect_from_webcam()
     return Response(text_detection(ocr_path=0), mimetype='multipart/x-mixed-replace; boundary=frame')

    #return  Response(text_detection(ocr_path=0), mimetype='multipart/x-mixed-replace; boundary=frame')
    
@app.route('/stop_camera' , methods=['GET'])
def stop_camera():
    release_camera()
    return  render_template('dashboard1.html')

if __name__ == "__main__":
    app.run(debug= True)
    