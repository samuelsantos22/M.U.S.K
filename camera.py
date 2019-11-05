import numpy as np
import cv2


class camera():
	def __init__(self):
		self.lineRect = 2
		self.colorRect = (0,255,0)
		self.captureCamera = cv2.VideoCapture(0)
		self.faceCascade = cv2.CascadeClassifier('cascade/data/haarcascade_frontalface_default.xml')
		self.faces = 0
		self.gray_frame = 0
		self.frame = 0
		self.flag = False

	def getFrame(self):
		#capture frame
		return self.captureCamera.read()

	def destroy(self):
		return self.captureCamera.release()

	def getImage(self):
		for (x,y,w,h) in self.faces:
			print(x,y,w,h)
			#Cords
			end_cord_x = x+w+50;  end_cord_y = y+h+50;
			ini_cord_x = x-25; ini_cord_y = y-25;
			#roi - region of interest
			roi_gray = self.gray_frame[ini_cord_y:end_cord_y, ini_cord_x:end_cord_x]
			roi_color = self.frame[ini_cord_y:end_cord_y, ini_cord_x:end_cord_x]
			roi_gray_res = cv2.resize(roi_gray, dsize=(420, 420), interpolation=cv2.INTER_CUBIC)
			cv2.imwrite("img1.jpg", roi_gray_res)
			cv2.rectangle(self.frame,(x,y), (end_cord_x,end_cord_y), self.colorRect, self.lineRect)
			self.flag = True

	def runFaceDetector(self):
		self.flag = False
		ret, self.frame = self.getFrame();
		#turn into gray
		self.gray_frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
		self.faces = self.faceCascade.detectMultiScale(self.gray_frame, scaleFactor=1.5, minNeighbors=8)
		self.getImage();
		return self.frame

	def sendVideo(self):
		success, image = self.getFrame()
		ret, jpg = cv2.imencode('.jpg', image)
		return jpg.tobytes()

