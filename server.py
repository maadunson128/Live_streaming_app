### Local streaming Web app

#importing modules, functions
from flask import Flask, render_template, Response, url_for
import cv2

#creating object of Flask
app = Flask(__name__)

#creating decorator for index page
@app.route('/')
def index():
    return render_template('index.html')

#creating decorator for 'frame' function called in index.html
@app.route('/frames')
def frames():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace ; boundary = frame')

#Function that generate images in bytes stream
def generate_frames():
    camera = cv2.VideoCapture(0)
    while True:
        success, image = camera.read()
        if not success:
            break
        else: 
            ret, buffer = cv2.imencode('.jpg', image)
            frame = buffer.tobytes()
        yield(b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')



#Running the flask server
if __name__ == "__main__":
    app.run(debug = True)