import serial

from time import sleep
import time

print "Running Program..."

ser = serial.Serial("COM3",115200,timeout=0)

timerec=time.time()
chars=0

while True:
	data=ser.read(1)
	chars+=1

	if len(data) > 0:
		pass
	else:
		continue

	if(data.find('n')!=-1):
		newt = time.time()
		print "Time: %f seconds, char = %d" % (newt-timerec,chars)
		timerec = newt

ser.close()
