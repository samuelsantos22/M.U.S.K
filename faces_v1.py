#Faces
#!/usr/bin/env python
#utf!=8# -*- coding: utf-8 -*-


#Last Update:18/05/2020

#Date: 18/05/2020
#Project:
#Ref: On ref

##################################################################
#[default - AWS ]
key_id = "AKIA2QDMHXIAOL7KQ4ZO"
secret_key = "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"

#[default - OPENCV]
line_rect = 2;
color_rect = (0, 255,0)



###################################################################
#imports

import numpy as np
import cv2

import boto3
import time
import json

#################################################################
# Settings

reko = boto3.client('rekognition', aws_access_key_id = key_id,
                                   aws_secret_access_key = secret_key,
                                   region_name = "us-west-2" )


def faceMatch(client, file, collection):
	face_matches = False
	with open(file, 'rb') as image:
		response = client.search_faces_by_image(CollectionId=collection, Image={'Bytes': image.read()}, MaxFaces=1, FaceMatchThreshold=95)
	if (not response['FaceMatches']):
		face_matches = False
	else:
		face_matches = True
	return face_matches, response

cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier('cascade/data/haarcascade_frontalface_default.xml')

while(True):

	#capture frame
	ret, frame = cap.read();
	#turn into gray
	gray_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.5, minNeighbors=8)

	for (x,y,w,h) in faces :
		print(x,y,w,h)

		#Cords
		end_cord_x = x+w+50;  end_cord_y = y+h+50;
		ini_cord_x = x-25; ini_cord_y = y-25;

		#roi - region of interest
		roi_gray = gray_frame[ini_cord_y:end_cord_y, ini_cord_x:end_cord_x]
		roi_color = frame[ini_cord_y:end_cord_y, ini_cord_x:end_cord_x]
		img_name = "img1.jpg"
		roi_gray_res = cv2.resize(roi_gray, dsize=(420, 420), interpolation=cv2.INTER_CUBIC)
		cv2.imwrite(img_name,roi_gray_res)
		cv2.rectangle(frame,(x,y), (end_cord_x,end_cord_y), color_rect,line_rect)

		resu, res = faceMatch(reko, 'img1.jpg', 'collectionTcc');
		if (resu):
			persona = res['FaceMatches'][0]['Face']['ExternalImageId']
			similaridade = res['FaceMatches'][0]['Similarity']
			confidence = res['FaceMatches'][0]['Face']['Confidence']
		else :
			persona = 'desconhecida'
			similaridade = 0
			confidence = 0
		print("Persona: " + str(persona));
		print("Similaridade: " + str(similaridade));
		print("Confidence: " + str(confidence));
		print(" ");
	#show img/vid on a box
	cv2.imshow('frame',frame)

	#stop when 'q' is pressed 
	if cv2.waitKey(20) & 0xFF == ord('q'):
		break


#release the capture on the end
cap.release()
cv2.destroyAllWindows()
