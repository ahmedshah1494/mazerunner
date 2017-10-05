import BoxFinder
from breezycreate2 import Robot
import cv2
import time
import os
import photo
import shapeDetector
from picamera import PiCamera
from text import image2text
from difflib import SequenceMatcher
import re
import numpy as np
from pyimagesearch.transform import four_point_transform

def sim(a, b):
    return SequenceMatcher(None, a, b).ratio()

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

def _getTagFromImage(c):
	if c == None:
		return
	ts, img = c
	height, width, channels = img.shape
	cropped_tag = img[0.02*height:(0.5*height),(0.45*width):width*0.98]
	cv2.imwrite("/root/server/irobot/static/snapshots/snapshot-cropped-tag" + str(ts) + ".jpg",cropped_tag)
	text = image2text(cropped_tag, 1)
	
	print ("Text  " + text)
	if text.find('[') < 0 or text.find(']') < 0:
                return None
	regex = re.compile('[^a-zA-Z0-9]')
	text = regex.sub('',text)
	
	split = text.split()

	print  split
		
	if len(split) < 1:
		print("<span class='error'>Invalid Tag </span>")
		return None

	if split[0].find('X') > -1:# or split[0].find('4') > -1:
		return 'X'
	if split[0].find('A') > -1:# or split[0].find('D') > -1 or split[0].find('C') > -1 or split[0].find('0') > -1 or split[0].find('td') > -1 or split[0].find('o') > -1:
		return 'A'
	if split[0].find('B') > -1:# or split[0].find('z') > -1 or split[0].find('6') > -1 or split[0].find('2') > -1:
		return 'B'
	if split[0].find('C') > -1:
            return 'C'
	if split[0].find('D') > -1:
            return 'D'
	if split[0].find('E') > -1:
            return 'E'
	if split[0].find('F') > -1:
            return 'F'
        print ("<span class='error'>Tag request failed, image not clear. </span>")
	return None

def getTagFromImage(c):
	if c == None:
		return
	ts, [t,_,_] = c
	return t
# Attempts to crop image. Returns timestamp and None/cropped
def cropImage():
	camera.resolution = (2560, 1600)
	ts, img = photo.get_image_from_picam(camera)
	height, width, channels = img.shape
	shape, v, coordinates = BoxFinder.findBox(img)
	print coordinates
	for [coord,_] in coordinates:
		print "coord", coord
		assert(len(coord) == 4)
		if coord != None:
			# cropped = img[coord[1]:(coord[1]+coord[3]),coord[0]:(coord[0]+coord[2])]
			coord = np.array(coord)
			print coord
			cropped = four_point_transform(img,coord)
			cv2.imwrite("/root/server/irobot/static/snapshots/snapshot-cropped" + str(ts) + ".jpg",cropped) 
			height, width, channels = cropped.shape
			t = _getTagFromImage((ts,cropped))
			if t != None:	
				dic = {'X':[None,'end of route'],
				'A':['left','spin left 3 times'],
				'B':['left','turn right 90 degrees'],
				'C':['left','move back 1 meters'],
				'D':['right','spin left 3 times'],
				'E':['right','turn right 90 degrees'],
				'F':['left','move back 1 meters']}
				# print width
				# print height	
				return ts,[t] + dic[t]	
	return ts,None

def cropImageStableRotate():
    degree = 30
    l = [0, (-1*degree), (2*degree)]
    for i in [0, (-1*degree), (2*degree)]:    
#    for i in [0]:
        robot.rotate(i)
        ts, img = cropImageStable()
        if img != None:
            rotate(-1*i)
            return ts, img
    return ts, None

# Attempts to crop image 3 times. Returns cropped
def cropImageStable():
	for i in range (1,2):
		print("Try: " + str(i))
		ts, cropped = cropImage()
		if cropped != None:
			return ts, cropped
		time.sleep(1.0*i)
	return ts, None

def cropImageWOLStable():
	for i in range (1,2):
		print("Try: " + str(i))
		ts, cropped = cropImageWOL()
		if cropped != None:
			return ts, cropped
		time.sleep(1.0*i)
	return ts, None

		
def cropImageWOL():
	camera.resolution = (2560, 1600)
	ts, img = photo.get_image_from_picam(camera)
	height, width, channels = img.shape
	# print width
	# print height
	shape, v, coord = BoxFinder.findBoxWOL(img)
	if coord != None:
		cropped = img[coord[1]:(coord[1]+coord[3]),coord[0]:(coord[0]+coord[2])]
		cv2.imwrite("/root/server/irobot/static/snapshots/snapshot-cropped" + str(ts) + ".jpg",cropped) 
		height, width, channels = cropped.shape	
		# print width
		# print height	
		return ts,cropped	
	return ts,None

def capture():
	ts,img = cropImageStableRotate()
	print ("<span>Image captured <a href='/static/snapshots/snapshot" + str(ts) + ".jpg'>(view image)</a></span>")
	if img == None:
		ts,img = cropImage()
		if img == None:
			print ("<span class='error'>Processing failed; image not clear.</span>")
			return None
	return ts,img
		
def getDirectionFromImage(c):
	if c == None:
		return
	ts, [_,d,_] = c
	return d
	height, width, channels = img.shape
	#shape, v, coord = BoxFinder.findBox(img)
	cropped_dir = img[0:(0.60*height),0:(0.65*width)]
	cv2.imwrite("/root/server/irobot/static/snapshots/snapshot-cropped-dir" + str(ts) + ".jpg",cropped_dir)
	c = shapeDetector.get_direction(cropped_dir)
	if c == None:
		print ("<span class='error'>Direction request failed, shape not clear.</span>")
		return None
	robot.robot.digit_led_ascii(c[:4].zfill(4))
	return c	 
	
def getCommandFromImage(c):
	valid_commands = [['spin', 'turn', 'move', 'end'],
				['right', 'left', 'of', 'straight', 'back'],
				[],
				['times', 'degrees', 'meters', 'route']
				]

				
	if c == None:
		return
	ts, [_,_,comm] = c
	return comm
	height, width, channels = img.shape
	cropped_com = img[(0.60*height):height,0:width]
        cv2.imwrite("/root/server/irobot/static/snapshots/snapshot-cropped-com" + str(ts) + ".jpg",cropped_com)
	text = image2text(cropped_com, 0)
	split = text.split() 
	
	split = map(lambda x: x.lower(), split)
	print split
	

	if len(split) < 4:
		print ("<span class='error'>Image is not clear, text recognition failed </span>")
		return

	print ("<span>Command requested</span>")

	cmd = []
	count = 0
	for i in range(len(split)):
		if count >= len(valid_commands):
			break
		if count == 2:
			if split[i] == 'the' or sim(split[i],'the')>0.80:
				cmd.append(split[i])
                                count += 1
				continue
			try:
				cmd.append(float(split[i]))
				count += 1
			except:
				continue
		elif is_in_list(split[i], valid_commands[count]) >= 0:
			cmd.append(valid_commands[count][is_in_list(split[i], valid_commands[count])])
			count += 1
	if len(cmd) < 4:
		print("<span class='error'>Invalid command: %s </span>" % str(cmd))
	return cmd
	
def is_in_list(word, l):
	regex = re.compile('[^a-zA-Z]')
	max = -1;
	ind = -1;
	for i in range(len(l)):
		find_sim = sim(regex.sub('',word),l[i])
		if  find_sim > max:
			max = find_sim
			ind = i
	if max > 0.7:
		return ind 
	else:
		return -1
	
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
	robot.robot.digit_led_ascii(str(pi_name)[0:4].zfill(4))
	robot.robot.safe()

	# except Exception as e:
	# 	if False:
	# 		print ("<span class='error'>You have an error: " + str(e) + "</span>")
	# 	else:
	# 		print ("<span class='error'>" + str(e) + "</span>")
	# 	robot.close()
# except Exception as e:
# 	print ("<span class='error'>Failed to connect to the iRobot: " + str(e)) + "</span>"

