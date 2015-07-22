import dweepy
import math

accelScale = 2

def dweet_add(add='hrishiopo'):
	dweet = dweepy.get_latest_dweet_for(add)[0]['content']
	ax = float(dweet['ax'])
	ay = float(dweet['ay'])
	az = float(dweet['az'])

	X = (ax/(32768.0/2.0))*9.81
	Y = (ay/(32768.0/2.0))*9.81
	Z = (az/(32768.0/2.0))*9.81

	print "%f,%f,%f - %f,%f,%f -> %f" % (ax,ay,az,X,Y,Z,math.sqrt(X*X+Y*Y+Z*Z))

def main():
	dweet_add()

if __name__ == '__main__':
	main()