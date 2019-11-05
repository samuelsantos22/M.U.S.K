from flask import Flask, render_template, Response, request, url_for, abort, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import sqlite3
import os
#import _thread
import threading
from sensor import sensor
import camera
import main
import servoMotor

tccCamera = camera.camera()
tccMotor = servoMotor.servoMotor()
tccMotor.runConfiguration()

# Running main code in a new thread
#def mainThread(data1, data2):
#	return os.system("sudo python3 main.py")

#_thread.start_new_thread(mainThread, ("null", "null"))

def thread_cam (data):
	print("entrou na thread")
	main.run(tccCamera)

t = threading.Thread(target=thread_cam,args=("null",))
t.start()

def thread_voice (data):
	print("entrou na thread_voice")
	os.system("sudo bash try_bash_.sh")

t = threading.Thread(target=thread_voice,args=("null",))
t.start()

def thread_kivy(data):
        print("entrou na thread kivy")
        os.system("sudo python kivy_gui.py")

t = threading.Thread(target=thread_kivy,args=("null",))
t.start()


def generateVideo(cam):
	while True:
		frame = cam.sendVideo()
		yield (b'--frame\r\n'
			b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


# Starting Flask Server and Sqlite3
app = Flask(__name__)
#conn = sqlite3.connect('todo.db')
#c = conn.cursor()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/pi/Desktop/tcc_files/opencv_aws/todo.db'
db = SQLAlchemy(app)

#c.execute("CREATE TABLE IF NOT EXISTS Todo(id INTEGER, title TEXT, start DATETIME, complete NUMERIC)")
#c.execute("INSERT INTO Todo VALUES(145, 'TesteTask' ,'2016-01-11 13:53:39', 1)")
#conn.commit()
#c.close()
#conn.close()

class Todo(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(200))
	start = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	complete = db.Column(db.Boolean)


@app.route("/")
def index():
	return render_template('home_entry.html')

@app.route('/inside')
def index2():
	return render_template('home_inside.html')

@app.route('/contact_pag')
def contact():
	return redirect(url_for('index'))

@app.route('/camera')
def camera():
	return render_template('camera.html')

@app.route('/cameraview')
def cameraview():
	return Response(generateVideo(tccCamera), mimetype='multipart/x-mixed-replace; boundary=frame')
#	return redirect(url_for('camera.html'))

@app.route('/panleft')
def move2():
        tccMotor.servo_position(0,-1)
        return redirect(url_for('camera.html'))


@app.route('/panright')
def move3():
        tccMotor.servo_position(0,1)
        return redirect(url_for('camera.html'))

@app.route('/temperatura')
def temp():
	umidade, temperatura = sensor.readDht11();
	templateData = {'umid': "10", 'temp': "10"}
	return render_template('temperaturahtml.html', **templateData)

@app.route('/agenda_pag')
def agenda():
	todos = Todo.query.all()
	incomplete = Todo.query.filter_by(complete=False).all()
	complete = Todo.query.filter_by(complete=True).all()
	return render_template('Agenda.html', incomplete=incomplete, complete=complete)

@app.route('/add', methods=['POST'])
def add():
	#return '<h1>{} </h1>'.format(request.form['todoitem']) # teste de entrada
	todo = Todo(title=request.form['todoitem'], start=datetime.strptime(request.form['date'], '%Y-%m-%d'),complete=False)
	db.session.add(todo)
	db.session.commit()
	return redirect(url_for('agenda'))

@app.route('/complete/<id>')
def complete(id):
	print("id obtido: " + str(id))
	todo = Todo.query.filter_by(id=int(id)).first()
	todo.complete = True
	db.session.commit()
	return redirect(url_for('agenda'))


if __name__ == "__main__":
	app.run(host='0.0.0.0', port=3000, debug=False)


