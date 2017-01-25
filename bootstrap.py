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



try:
	robot = Robot()
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
except Exception as e:
	print ("<span class='error'>Failed to connect to the iRobot: " + str(e)) + "</span>"




# robot = None
# VELOCITYCHANGE = 0.2
# ROTATIONCHANGE = 0.3

# def goForwardInTime(s, v = VELOCITYCHANGE):
# 	global robot
# 	robot.goForwardInTime(s, v * 1000.0)
# def goForward(d, v = VELOCITYCHANGE):
# 	global robot
# 	robot.goForward(d, v * 1000.0)
# def goForwardUntilBump(d, v = VELOCITYCHANGE):
# 	global robot
# 	return robot.goForwardUntilBump(d, v * 1000.0)
# def stopMoving():
# 	global robot
# 	robot.stopMoving()
# def goBackward(d, v = VELOCITYCHANGE):
# 	global robot
# 	robot.goBackward(d, v * 1000.0)
# def goBackwardInTime(s, v = VELOCITYCHANGE):
# 	global robot
# 	robot.goBackwardInTime(s, v * 1000.0)
# def turnLeft(deg, r = ROTATIONCHANGE):
# 	global robot
# 	robot.turnLeft(deg, r * 1000.0)
# def turnRight(deg, r = ROTATIONCHANGE):
# 	global robot
# 	robot.turnRight(deg, r * 1000.0)