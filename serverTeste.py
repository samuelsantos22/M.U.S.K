def run(tccCam):

	from flask import Flask, render_template, Response, request, url_for, abort, redirect
	from flask_sqlalchemy import SQLAlchemy
	from datetime import datetime
	import sqlite3
	import os

	from sensor import sensor

	tccCamera = tccCam;

	def generateVideo(cam):
		while True:
			frame = cam.sendVideo()
			yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


	# Starting Flask Server and Sqlite3
	app = Flask(__name__)

	app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/pi/Desktop/tcc_files/opencv_aws/todo.db'
	db = SQLAlchemy(app)

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


