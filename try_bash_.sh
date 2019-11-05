#!/bin/bash --rcfile

source /etc/bash.bashrc
source ~/.bashrc

cat /etc/aiyprojects.info

cd /home/pi/AIY-voice-kit-python
source env/bin/activate 
/home/pi/AIY-voice-kit-python/src/assistant_library_demo.py

