def run(tccCam):
	print("entrou na main")
	import numpy as np
	import cv2
	import time
	import json
	import personaVerification
	import awsConnection
	import sensor
	import security
	import camera

	#[default - OPENCV]
	#line_rect = 2;
	#color_rect = (0, 255,0)

	# Creating objects
	tccAws = awsConnection.awsConnection()
	tccPersona = personaVerification.personaVerification()
	tccSensor = sensor.sensor()
	tccSecurity = security.security()
	print("antes do cv2")
	tccCamera = tccCam
	print("depois do cv2")

	# Connecting to AWS Rekognition
	tccAws.getRekognitionClient()

	# Motion callback function
	def motionCallback(channel):
		print("[+]Motion detected")
		return tccSecurity.sendEmail()

	# Starting sensors
	tccSensor.runConfiguration(motionCallback)

	# Starting OpenCV
	#cap = cv2.VideoCapture(0)
	#face_cascade = cv2.CascadeClassifier('cascade/data/haarcascade_frontalface_default.xml')


	#while(True):
	#	faces, frame, gray_frame = tccCamera.runFaceDetector()
	#	for (x,y,w,h) in faces:
	#		print(x,y,w,h)
	#		#Cords
	#		end_cord_x = x+w+50;  end_cord_y = y+h+50;
	#		ini_cord_x = x-25; ini_cord_y = y-25;
	#		#roi - region of interest
	#		roi_gray = gray_frame[ini_cord_y:end_cord_y, ini_cord_x:end_cord_x]
	#		roi_color = frame[ini_cord_y:end_cord_y, ini_cord_x:end_cord_x]
	#		roi_gray_res = cv2.resize(roi_gray, dsize=(420, 420), interpolation=cv2.INTER_CUBIC)
	#		cv2.imwrite("img1.jpg", roi_gray_res)
	#		cv2.rectangle(frame,(x,y), (end_cord_x,end_cord_y), tccCamera.colorRect,tccCamera.lineRect)
	#
	#		tccPersona.faceMatch(tccAws.awsRekognitionClient)
	#
	#	#cv2.imshow('frame',frame)
	#
	#	#stop when 'q' is pressed
	#	if cv2.waitKey(20) & 0xFF == ord('q'):
	#		break


	while(True):
		frame = tccCamera.runFaceDetector()
		if(tccCamera.flag):
			tccPersona.faceMatch(tccAws.awsRekognitionClient)
		cv2.imshow('frame', frame)

		#stop when 'q' is pressed
		if cv2.waitKey(20) & 0xFF == ord('q'):
			break

	#release the capture on the end
	cap.release()
	cv2.destroyAllWindows()
	tccSensor.cleanSensorPorts()

