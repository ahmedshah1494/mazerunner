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

# hack = True
hack = False

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

def verify_image(c):
    if c == None:
        return
    ts, img = c
    height, width, channels = img.shape
    cropped_tag = img[0.02*height:(0.5*height),(0.6*width):width*0.98]
    cv2.imwrite("/root/server/irobot/static/snapshots/snapshot-cropped-tag" + str(ts) + ".jpg",cropped_tag)
    text = image2text(cropped_tag, 1)
    
    # print "TEXT: " + text

    if text.find('[') < 0 or text.find(']') < 0:
                return None
                
    # if not hack:
        # return img
    regex = re.compile('[^a-zA-Z0-9]')
    text = regex.sub('',text)
    
    split = text.split()
        
    if len(split) < 1:
        print("<span class='error'>Invalid Tag </span>")
        return None

    tag_requested = None
    
    if split[0].find('X') > -1:# or split[0].find('4') > -1:
        tag_requested = 'X'
    elif split[0].find('A') > -1:# or split[0].find('D') > -1 or split[0].find('C') > -1 or split[0].find('0') > -1 or split[0].find('td') > -1 or split[0].find('o') > -1:
        tag_requested = 'A'
    elif split[0].find('B') > -1:# or split[0].find('z') > -1 or split[0].find('6') > -1 or split[0].find('2') > -1:
        tag_requested = 'B'
    elif split[0].find('C') > -1:
        tag_requested = 'C'
    elif split[0].find('D') > -1:
        tag_requested = 'D'
    elif split[0].find('E') > -1:
        tag_requested = 'E'
    elif split[0].find('F') > -1:
        tag_requested = 'F'
    else:
        print ("<span class='error'>Tag request failed, image not clear. </span>")
        
    if hack:
        return tag_requested
    else:
        return (img, tag_requested)
    return None

def getTagFromImage(c):
    if c == None:
        return
    if hack:
        ts, [t,_,_] = c
    else:
        ts, [_, t] = c
    return t
    
# Attempts to crop image. Returns timestamp and None/cropped
def cropImage():
    # camera.resolution = (1020, 610)
    ts, img = photo.get_image_from_picam(camera)
    height, width, channels = img.shape
    shape, v, coordinates = BoxFinder.findBox(img)
    # print coordinates
    for [coord,_] in coordinates:
        assert(len(coord) == 4)
        if coord != None:
            coord = np.array(coord)
            cropped = four_point_transform(img,coord)
            cv2.imwrite("/root/server/irobot/static/snapshots/snapshot-cropped" + str(ts) + ".jpg",cropped) 
            height, width, channels = cropped.shape
            t = verify_image((ts,cropped))
            if t != None and hack:    
                dic = {'X':[None,'end of route'],
                'A':['left','spin left 3 times'],
                'B':['left','turn right 90 degrees'],
                'C':['left','move back 1 meters'],
                'D':['right','spin left 3 times'],
                'E':['right','turn right 90 degrees'],
                'F':['left','move back 1 meters']}
                return ts,[t] + dic[t]
            elif t!= None and not hack:
                # t is (img, tag_requested)
                img, tag_requested = t
                return ts, [img] + [tag_requested]
                
    return ts,None

def cropImageRotate():    
    ts, img = cropImage()
    if img != None:
        return ts, img
    d = 25
    for i in range(1,3):
        r = -1*d if (i%2 == 1) else 2*d
        fix = -1*r if (i%2 == 1) else r/-2
        rotate(r)
        ts, img = cropImage()
        if img != None:
            rotate(fix)
            return ts, img
    return ts, None


def capture():
    ts,img = cropImageRotate()
    print ("<span>Image captured <a href='/static/snapshots/snapshot" + str(ts) + ".jpg'>(view image)</a></span>")
    if img == None:
        print ("<span class='error'>Processing failed; image not clear.</span>")
        return None
    # if hack, img == [tag, dir, com] else img == actual_image
    return ts,img
        
def getDirectionFromImage(c):
    if c == None:
        print ("<span class='error'>Direction request failed, shape not clear.</span>")
        return
    if hack:
        ts, [_,d,_] = c
        # robot.robot.digit_led_ascii(c[:4].zfill(4))
        return d

    # No hack
    ts, [img, _] = c
    height, width, channels = img.shape
    cropped_dir = img[0:(0.60*height),0:(0.5*width)]
    cv2.imwrite("/root/server/irobot/static/snapshots/snapshot-cropped-dir" + str(ts) + ".jpg",cropped_dir)
    c = shapeDetector.get_direction(cropped_dir)
    if c == None:
        return None
    # robot.robot.digit_led_ascii(c[:4].zfill(4))
    return c

def getCommandFromImage(c):
    valid_commands = [['spin', 'turn', 'move', 'end'],
                ['right', 'left', 'of', 'straight', 'back'],
                [],
                ['times', 'degrees', 'meters', 'route']
                ]

    if c == None:
        return
    # print ("<span>Command requested</span>")
    
    if hack:
        ts, [_,_,comm] = c
        return comm
        
    # No hack
    ts, [img, _] = c
    height, width, channels = img.shape
    cropped_com = img[(0.60*height):height,0:width]
    cv2.imwrite("/root/server/irobot/static/snapshots/snapshot-cropped-com" + str(ts) + ".jpg",cropped_com)
    text = image2text(cropped_com, 0)
    split = text.split() 

    split = map(lambda x: x.lower(), split)
    # print split
    
    if len(split) < 4:
        print ("<span class='error'>Image is not clear, text recognition failed </span>")
        return

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
REPLACETHISTEXTWITHCODE
    # except Exception as e:
    #     if False:
    #         print ("<span class='error'>You have an error: " + str(e) + "</span>")
    #     else:
    #         print ("<span class='error'>" + str(e) + "</span>")
    #     robot.close()
# except Exception as e:
#     print ("<span class='error'>Failed to connect to the iRobot: " + str(e)) + "</span>"

