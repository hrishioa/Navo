import RPi.GPIO as GPIO

#IO Setup
r2p1 = 4
r2p2 = 25
r1p1 = 23
r1p2 = 24

def relaysetup():
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(r1p1,GPIO.OUT)
        GPIO.setup(r1p2,GPIO.OUT)
        GPIO.setup(r2p1,GPIO.OUT)
        GPIO.setup(r2p2,GPIO.OUT)

def relay1(status):
        GPIO.output(r1p1,status)
        GPIO.output(r1p2,status)

def relay2(status):
        GPIO.output(r2p1,status)
        GPIO.output(r2p2,status)

def on():
	relay1(True)
	relay2(True)

def off():
	relay1(False)
	relay2(False)
