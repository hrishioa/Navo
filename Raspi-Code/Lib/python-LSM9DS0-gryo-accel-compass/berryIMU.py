from sys import argv

import smbus
import dweepy
import time
import math
import RPi.GPIO as GPIO
from LSM9DS0 import *
import datetime
bus = smbus.SMBus(1)

RAD_TO_DEG = 57.29578
M_PI = 3.14159265358979323846
G_GAIN = 0.070  # [deg/s/LSB]  If you change the dps for gyro, you need to update this value accordingly
LP = 0.041    	# Loop period = 41ms.   This needs to match the time it takes each loop to run
AA =  0.80      # Complementary filter constant

script,filename = argv

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

tspeedx=0.0
tspeedy=0.0
tspeedz=0.0
g  = None

def get_dweet(add='hrishiopo'):
	global tspeedx,tspeedy,tspeedz,g
	try:
		dweet = dweepy.get_latest_dweet_for(add)[0]
		ax = float(dweet['content']['ax'])
                ay = float(dweet['content']['ay'])
                az = float(dweet['content']['az'])
		
		if(not g):
			g = (float(dweet['content']['xg']),float(dweet['content']['yg']),float(dweet['content']['zg']))
		ax-=g[0]
		ay-=g[1]
		az-=g[2]
	except (KeyError, TypeError):
		return


def writeACC(register,value):
        bus.write_byte_data(ACC_ADDRESS , register, value)
        return -1

def writeMAG(register,value):
        bus.write_byte_data(MAG_ADDRESS, register, value)
        return -1

def writeGRY(register,value):
        bus.write_byte_data(GYR_ADDRESS, register, value)
        return -1



def readACCx():
        acc_l = bus.read_byte_data(ACC_ADDRESS, OUT_X_L_A)
        acc_h = bus.read_byte_data(ACC_ADDRESS, OUT_X_H_A)
	acc_combined = (acc_l | acc_h <<8)

	return acc_combined  if acc_combined < 32768 else acc_combined - 65536


def readACCy():
        acc_l = bus.read_byte_data(ACC_ADDRESS, OUT_Y_L_A)
        acc_h = bus.read_byte_data(ACC_ADDRESS, OUT_Y_H_A)
	acc_combined = (acc_l | acc_h <<8)

	return acc_combined  if acc_combined < 32768 else acc_combined - 65536


def readACCz():
        acc_l = bus.read_byte_data(ACC_ADDRESS, OUT_Z_L_A)
        acc_h = bus.read_byte_data(ACC_ADDRESS, OUT_Z_H_A)
	acc_combined = (acc_l | acc_h <<8)

	return acc_combined  if acc_combined < 32768 else acc_combined - 65536


def readMAGx():
        mag_l = bus.read_byte_data(MAG_ADDRESS, OUT_X_L_M)
        mag_h = bus.read_byte_data(MAG_ADDRESS, OUT_X_H_M)
        mag_combined = (mag_l | mag_h <<8)

        return mag_combined  if mag_combined < 32768 else mag_combined - 65536


def readMAGy():
        mag_l = bus.read_byte_data(MAG_ADDRESS, OUT_Y_L_M)
        mag_h = bus.read_byte_data(MAG_ADDRESS, OUT_Y_H_M)
        mag_combined = (mag_l | mag_h <<8)

        return mag_combined  if mag_combined < 32768 else mag_combined - 65536


def readMAGz():
        mag_l = bus.read_byte_data(MAG_ADDRESS, OUT_Z_L_M)
        mag_h = bus.read_byte_data(MAG_ADDRESS, OUT_Z_H_M)
        mag_combined = (mag_l | mag_h <<8)

        return mag_combined  if mag_combined < 32768 else mag_combined - 65536



def readGYRx():
        gyr_l = bus.read_byte_data(GYR_ADDRESS, OUT_X_L_G)
        gyr_h = bus.read_byte_data(GYR_ADDRESS, OUT_X_H_G)
        gyr_combined = (gyr_l | gyr_h <<8)

        return gyr_combined  if gyr_combined < 32768 else gyr_combined - 65536
  

def readGYRy():
        gyr_l = bus.read_byte_data(GYR_ADDRESS, OUT_Y_L_G)
        gyr_h = bus.read_byte_data(GYR_ADDRESS, OUT_Y_H_G)
        gyr_combined = (gyr_l | gyr_h <<8)

        return gyr_combined  if gyr_combined < 32768 else gyr_combined - 65536

def readGYRz():
        gyr_l = bus.read_byte_data(GYR_ADDRESS, OUT_Z_L_G)
        gyr_h = bus.read_byte_data(GYR_ADDRESS, OUT_Z_H_G)
        gyr_combined = (gyr_l | gyr_h <<8)

        return gyr_combined  if gyr_combined < 32768 else gyr_combined - 65536



	
#initialise the accelerometer
writeACC(CTRL_REG1_XM, 0b01100111) #z,y,x axis enabled, continuos update,  100Hz data rate
writeACC(CTRL_REG2_XM, 0b00100000) #+/- 16G full scale

#initialise the magnetometer
writeMAG(CTRL_REG5_XM, 0b11110000) #Temp enable, M data rate = 50Hz
writeMAG(CTRL_REG6_XM, 0b01100000) #+/-12gauss
writeMAG(CTRL_REG7_XM, 0b00000000) #Continuous-conversion mode

#initialise the gyroscope
writeGRY(CTRL_REG1_G, 0b00001111) #Normal power mode, all axes enabled
writeGRY(CTRL_REG4_G, 0b00110000) #Continuos update, 2000 dps full scale

gyroXangle = 0.0
gyroYangle = 0.0
gyroZangle = 0.0
CFangleX = 0.0
CFangleY = 0.0

count=0
countmax=500000
countgrav=50

gx=0.0
gy=0.0
gz=0.0

speedx=0.0
speedy=0.0
speedz=0.0

logfile = open(filename, 'w')
logfile.write("GX,GY,GZ,AX,AY,AZ,SX,SY,SZ,TA,TS\n")

speed=0

while True:
	a = datetime.datetime.now()

	count+=1

	if(count>countmax):
		count=countgrav
	
	#Read our accelerometer,gyroscope and magnetometer  values
	ACCx = readACCx()
	ACCy = readACCy()
	ACCz = readACCz()
	GYRx = readGYRx()
	GYRy = readGYRx()
	GYRz = readGYRx()
	MAGx = readMAGx()
	MAGy = readMAGy()
	MAGz = readMAGz()

	##Convert Accelerometer values to degrees
	AccXangle =  (math.atan2(ACCy,ACCz)+M_PI)*RAD_TO_DEG
	AccYangle =  (math.atan2(ACCz,ACCx)+M_PI)*RAD_TO_DEG



	#Convert Gyro raw to degrees per second
	rate_gyr_x =  GYRx * G_GAIN
	rate_gyr_y =  GYRy * G_GAIN
	rate_gyr_z =  GYRz * G_GAIN


	#Calculate the angles from the gyro. LP = loop period 
	gyroXangle+=rate_gyr_x*LP
	gyroYangle+=rate_gyr_y*LP
	gyroZangle+=rate_gyr_z*LP

        #Change the rotation value of the accelerometer to -/+ 180 and move the Y axis '0' point to up.
        #Two different pieces of code are used depending on how your IMU is mounted.
        #If IMU is upside down
	#
        #if AccXangle >180:
        #        AccXangle -= 360.0
        #AccYangle-=90
        #if (AccYangle >180):
        #        AccYangle -= 360.0
	

        #If IMU is up the correct way, use these lines
        AccXangle -= 180.0
	if AccYangle > 90:
	        AccYangle -= 270.0
	else:
		AccYangle += 90.0


        #Complementary filter used to combine the accelerometer and gyro values.
        CFangleX=AA*(CFangleX+rate_gyr_x*LP) +(1 - AA) * AccXangle
        CFangleY=AA*(CFangleY+rate_gyr_y*LP) +(1 - AA) * AccYangle



	#Calculate heading
	heading = 180 * math.atan2(MAGy,MAGx)/M_PI

	if heading < 0:
	 	heading += 360


	#Normalize accelerometer raw values.
        accXnorm = ACCx/math.sqrt(ACCx * ACCx + ACCy * ACCy + ACCz * ACCz)
	accYnorm = ACCy/math.sqrt(ACCx * ACCx + ACCy * ACCy + ACCz * ACCz)


	#Calculate pitch and roll
	pitch = math.asin(accXnorm)
	roll = -math.asin(accYnorm/math.cos(pitch))

	#Calculate the new tilt compensated values
	magXcomp = MAGx*math.cos(pitch)+MAGz*math.sin(pitch)
	magYcomp = MAGx*math.sin(roll)*math.sin(pitch)+MAGy*math.cos(roll)-MAGz*math.sin(roll)*math.cos(pitch)

	#Calculate tiles compensated heading
        tiltCompensatedHeading = 180 * math.atan2(magYcomp,magXcomp)/M_PI

        if tiltCompensatedHeading < 0:
                tiltCompensatedHeading += 360

 	print ("\033[1;34;40mACCX Angle %5.2f ACCY Angle %5.2f\033[1;31;40m\tGRYX Angle %5.2f  GYRY Angle %5.2f  GYRZ Angle %5.2f \033[1;35;40m    \tCFangleX Angle %5.2f \033[1;36;40m  CFangleY Angle %5.2f \33[1;32;40m  HEADING  %5.2f \33[1;37;40m tiltCompensatedHeading %5.2f\033[0m  " % (AccXangle, AccYangle,gyroXangle,gyroYangle,gyroZangle,CFangleX,CFangleY,heading,tiltCompensatedHeading))


        time.sleep(0.01)
	b = datetime.datetime.now()
	c = b - a

	print "Loop Time |",  c.microseconds/1000,"|",

	if(count<countgrav):
		print "Getting gravity..."
		gx = ((gx*count)+ACCx)/(count+1)
                gy = ((gy*count)+ACCy)/(count+1)
                gz = ((gz*count)+ACCz)/(count+1)

	ACCx2=float(ACCx-gx)
	ACCy2=float(ACCy-gy)
	ACCz2=float(ACCz-gz)

	speedx+=(ACCx2)*(c.microseconds/1000000.0)
        speedy+=(ACCy2)*(c.microseconds/1000000.0)
        speedz+=(ACCz2)*(c.microseconds/1000000.0)

	logfile.write("%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f\n" % (gx,gy,gz,ACCx,ACCy,ACCz,speedx,speedy,speedz,\
						math.sqrt(speedx*speedx+speedy*speedy+speedz*speedz),math.sqrt(ACCx2*ACCx2+ACCy2*ACCy2+ACCz2*ACCz2)))





	
