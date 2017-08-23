from breezycreate2 import Robot
import time
import os

robot = None

def moveForward(speed=200):
	return robot.moveForward(speed)

def moveBackward(speed=200):
	return robot.moveBackward(speed)

def moveDistance(meters, speed=200):
	return robot.moveDistance(meters, speed)

def moveDistanceSmart(meters, speed=200):
	robot.moveDistanceSmart(meters, speed)

def rotate(angle, speed=200):
	return robot.rotate(angle, speed)

def getBumpers():
	return robot.getBumpers()
    
def getWallSensor():
	return robot.getWallSensor()

def getWallSensors():
	return robot.getWallSensors()

def stop():
	return robot.stop()



# try:
# 	print 1
robot = Robot()
print 2
if not robot.isConnected():
	print "<span class='error'>Failed to connect to the iRobot</span>"
else:
	try:
REPLACETHISTEXTWITHCODE
	except Exception as e:
		if False:
			print ("<span class='error'>You have an error: " + str(e) + "</span>")
		else:
			print ("<span class='error'>" + str(e) + "</span>")
		robot.close()
# except Exception as e:
# 	print ("<span class='error'>Failed to connect to the iRobot: " + str(e)) + "</span>"

