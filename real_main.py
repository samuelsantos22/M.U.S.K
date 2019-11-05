# -*- coding: utf-8 -*-

from datetime import datetime
import sqlite3
import time
import os
import commands
import threading

from sensor import sensor
import camera
import main
import server
import kivy_gui

tccCamera = camera.camera()


def thread_cam (data):
	print("entrou na thread")
	main.run(tccCamera)

t = threading.Thread(target=thread_cam,args=("show",))
t.start()

def thread_server (data):
	print("entrou na thread")
	server.run(tccCamera)

t = threading.Thread(target=thread_cam,args=("show",))
t.start()

def thread_gui (data):
	print("entrou na thread")
	kivy.run()

t = threading.Thread(target=thread_cam,args=("show",))
t.start()

def thread_voice (data):
	print("entrou na thread_voice")
	os.system("sudo bash try_bash_.sh")
    
t = threading.Thread(target=thread_voice,args=("show",))
t.start()
