import dweepy
import math
import numpy as np

accelScale = 2

def accelConv(accelVal):
	return (accelVal/(32768.0/2.0))*9.81

lastTime = None
g=None
curSpeed=None

def dweet_add(add='hrishiopo',dw=None):
	global lastTime
	global g
	global curSpeed

	if(dw==None):
		dweet = dweepy.get_latest_dweet_for(add)[0]
	else:
		dweet=dw

	try:
		#print dweet

		a = (accelConv(float(dweet['content']['ax'])),accelConv(float(dweet['content']['ay']))\
			,accelConv(float(dweet['content']['az'])))

		if(not g):
			g = (accelConv(float(dweet['content']['xg'])),accelConv(float(dweet['content']['yg']))\
			,accelConv(float(dweet['content']['zg'])))

		# Correct for gravity

		a = np.subtract(a,g)

		#Get current time using regex shenanigans
		timelist = dweet['created'].split('T')[1].split('Z')[0].split(':')
		tsecs = 0.0

		for i in range(0,len(timelist)):
			tsecs+=float(timelist[i])*(60**(2-i))

		if(lastTime==None):
			lastTime=tsecs
			curSpeed=(0.0,0.0,0.0)
			return

		iA = a*(tsecs-lastTime)

		if(curSpeed==None):
			curSpeed = iA
			return

		curSpeed+=iA

		print "%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f" % (curSpeed[0],curSpeed[1],curSpeed[2],iA[0],iA[1],iA[2],a[0],a[1],a[2],g[0],g[1],g[2],tsecs)
	
	except (KeyError, TypeError):
		return


def main():
#	for dweet in dweepy.listen_for_dweets_from('hrishiopo'):
	for i in range(0,1000):
		dweet_add()

if __name__ == '__main__':
	main()