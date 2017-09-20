from breezycreate2 import Robot
import time
import os
import photo
import shapeDetector
from picamera import PiCamera
from text import image2text

robot = None
camera = PiCamera()
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
	img = photo.get_image_from_picam(camera)
	c = shapeDetector.get_direction(img)
	robot.robot.digit_led_ascii(c[:4].zfill(4))
	return c

def getCommandFromImage():
	valid_commands = [['spin', 'turn', 'move'],
				['right', 'left', 'forward', 'backward'],
				[],
				['times', 'degrees', 'meters']
				]
	img = photo.get_image_from_picam(camera)
	text = image2text(img)
	split = text.split()
	split = map(lambda x: x.lower(), split)
	print split
	if len(split) < 4:
		print ("<span class='error'>Image is not clear, text recognition failed</span>")
		return
	cmd = []
	count = 0
	for i in range(len(split)):
		if count >= len(valid_commands):
			break
		if count == 2:
			try:
				cmd.append(float(split[i]))
				count += 1
			except:
				continue
		elif split[i] in valid_commands[count]:
			cmd.append(split[i])
			count += 1
	if len(cmd) < 4:
		print("<span class='error'>Invalid command: %s </span>" % str(cmd))
	return cmd
# try:
robot = Robot()
if not robot.isConnected():
	print "<span class='error'>Failed to connect to the iRobot</span>"
else:
	# try:
	f = os.popen('ifconfig  wlan0 | grep "inet addr:"| grep -v "127.0.0.1" | cut -d: -f2 | awk \'{ print $1}\'')
	myIP = f.read().strip()
	
	print myIP
	robot.robot.full()
	print "robot initalized"
	for i in range(20):
	
		ip = myIP
		for i in range(2):
			robot.robot.digit_led_ascii(str("Addr").zfill(4))
			time.sleep(0.5)
			robot.robot.digit_led_ascii(str("    ").zfill(4))
			time.sleep(0.5)
		
		while len(ip) >= 4:
			robot.robot.digit_led_ascii(str(ip[:4]).zfill(4))
			ip = ip[1:]
			time.sleep(0.4)
			
		time.sleep(1)
	
	pi_name = os.environ['RESIN_DEVICE_NAME_AT_INIT']
	print pi_name
	robot.robot.digit_led_ascii(str(pi_name).zfill(4))
	robot.robot.safe()

	# except Exception as e:
	# 	if False:
	# 		print ("<span class='error'>You have an error: " + str(e) + "</span>")
	# 	else:
	# 		print ("<span class='error'>" + str(e) + "</span>")
	# 	robot.close()
# except Exception as e:
# 	print ("<span class='error'>Failed to connect to the iRobot: " + str(e)) + "</span>"

