from breezycreate2 import Robot
import time
import os
import photo
import shapeDetector

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

def getDirectionFromImage():
	img = photo.get_image_from_picam()
	c = shapeDetector.get_direction(img)
	robot.robot.digit_led_ascii(c[:4].zfill(4))
	return c

# try:
robot = Robot()
if not robot.isConnected():
	print "<span class='error'>Failed to connect to the iRobot</span>"
else:
	# try:
REPLACETHISTEXTWITHCODE
	# except Exception as e:
	# 	if False:
	# 		print ("<span class='error'>You have an error: " + str(e) + "</span>")
	# 	else:
	# 		print ("<span class='error'>" + str(e) + "</span>")
	# 	robot.close()
# except Exception as e:
# 	print ("<span class='error'>Failed to connect to the iRobot: " + str(e)) + "</span>"

