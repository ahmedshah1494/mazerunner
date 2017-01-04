import iRobot

robot = None
VELOCITYCHANGE = 0.2
ROTATIONCHANGE = 0.3

def goForwardInTime(s, v = VELOCITYCHANGE):
	global robot
	robot.goForwardInTime(s, v * 1000.0)
def goForward(d, v = VELOCITYCHANGE):
	global robot
	robot.goForward(d, v * 1000.0)
def goForwardUntilBump(d, v = VELOCITYCHANGE):
	global robot
	return robot.goForwardUntilBump(d, v * 1000.0)
def stopMoving():
	global robot
	robot.stopMoving()
def goBackward(d, v = VELOCITYCHANGE):
	global robot
	robot.goBackward(d, v * 1000.0)
def goBackwardInTime(s, v = VELOCITYCHANGE):
	global robot
	robot.goBackwardInTime(s, v * 1000.0)
def turnLeft(deg, r = ROTATIONCHANGE):
	global robot
	robot.turnLeft(deg, r * 1000.0)
def turnRight(deg, r = ROTATIONCHANGE):
	global robot
	robot.turnRight(deg, r * 1000.0)

try:
	robot = iRobot.iRobotInterface()
	if not robot.is_connected():
		print "<span class='error'>Failed to connect to the iRobot</span>"
	else:
		try:
REPLACETHISTEXTWITHCODE
		except Exception as e:
			if False:
				print ("<span class='error'>You have an error: " + str(e) + "</span>")
			else:
				print ("<span class='error'>" + str(e) + "</span>")
			robot.stopMoving()
except Exception as e:
	print ("<span class='error'>Failed to connect to the iRobot: " + str(e)) + "</span>"

