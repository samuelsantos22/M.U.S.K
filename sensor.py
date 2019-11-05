import RPi.GPIO as GPIO
import Adafruit_DHT


#def testeCall(channel):
#	print("deu bom")

class sensor():
	def __init__(self):
		self.pinoMotion = 24
		self.pinoTemperature = 26
		self.sensorTemperatureType = Adafruit_DHT.DHT11

	def runConfiguration(self, motionFunction):
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(self.pinoMotion, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
		GPIO.add_event_detect(self.pinoMotion, GPIO.RISING, callback=motionFunction, bouncetime=300)
		print("[+]Sensors configured")

	def readDht11():
		#umidade, temperatura = Adafruit_DHT.read_retry(self.sensorTemperatureType, self.pinoTemperature)
		#return umidade, temperatura
		return "10", "10"

	def cleanSensorPorts(self):
		GPIO.cleanup()

