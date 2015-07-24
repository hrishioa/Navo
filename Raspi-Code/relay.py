import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT)
GPIO.setup(24,GPIO.OUT)
GPIO.setup(25,GPIO.OUT)
GPIO.setup(23,GPIO.OUT)
GPIO.setup(22,GPIO.IN)

for i in range(0,10):
        GPIO.output(4, True)
        GPIO.output(24,True)
	GPIO.output(25,False)
	GPIO.output(23,False)
	time.sleep(0.25)
	GPIO.output(4, False)
	GPIO.output(24,False)
        GPIO.output(25,True)
        GPIO.output(23,True)
	time.sleep(0.25)

previr=0


GPIO.cleanup()
