import iRobot
from breezycreate2 import Robot

try:
	robot = Robot()
	if not robot.isConnected():
		print "<span class='error'>Failed to connect to the iRobot</span>"
	else:
		try:
			robot.setForwardSpeed(200)
			#robot.robot.stop()
		except Exception as e:
			if False:
				print ("<span class='error'>You have an error: " + str(e) + "</span>")
			else:
				print ("<span class='error'>" + str(e) + "</span>")
			robot.robot.stop()
except Exception as e:
	print ("<span class='error'>Failed to connect to the iRobot: " + str(e)) + "</span>"

