import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.OUT)
GPIO.setup(17, GPIO.OUT)

def Blink(numTimes, speed):
	for i in range(0, numTimes):
		print "Iteration "+str(i+1)
		GPIO.output(26,True)
		GPIO.output(17,True)
		time.sleep(speed)
		GPIO.output(26,False)
		GPIO.output(17,False)
		time.sleep(speed)
	print "Done"
	GPIO.cleanup()

iterations = raw_input("Enter number of times to blink: ")
speed = raw_input("Length of each blink in seconds: ")

Blink(int(iterations),float(speed))
