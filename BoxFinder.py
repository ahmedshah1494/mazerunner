import cv2
import imutils
import numpy as np
from photo import get_image_from_picam

# Class for finding the box in our image

class BoxFinder:
	def __init__(self):
		pass
	def detect(self,c):
		shape='unidentified'
		peri = cv2.arcLength(c,True)
		approx = cv2.approxPolyDP(c,0.05*peri,True)
		# if the shape is a triangle, it will have 3 vertices
		if len(approx) == 3:
			shape = "triangle"
 
		# if the shape has 4 vertices, it is either a square or
		# a rectangle
		elif len(approx) == 4:
			# compute the bounding box of the contour and use the
			# bounding box to compute the aspect ratio
			(x, y, w, h) = cv2.boundingRect(approx)
			ar = w / float(h)
			# a square will have an aspect ratio that is approximately
			# equal to one, otherwise, the shape is a rectangle
			shape = "square" if ar >= 0.95 and ar <= 1.05 else "rectangle"
 
		# if the shape is a pentagon, it will have 5 vertices
		elif len(approx) == 5:
			shape = "pentagon"
 
		# otherwise, we assume the shape is a circle
		else:
			shape = "circle"
 
		# return the name of the shape
		return shape,approx

		
# Takes a snapshot and returns the coordinates of the box 
# Coordinates are based on the box occupying 
# an area of around 10% of image.
# This function draws a white border on the box after retrieval

def findBox(image):

	cv2.imwrite('/root/server/irobot/static/iimg.png',image)
	colors = ['blue','green', 'red']

	resized = image
	ratio  = 1.0
	 
	# convert the resized image to grayscale, blur it slightly,
	# and threshold it
	gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
	inv = cv2.bitwise_not(gray)
	blur = cv2.GaussianBlur(inv, (5, 5), 0)
	
	thresh = cv2.Canny(blur,100,300,apertureSize = 3)

	cv2.imwrite('/root/server/irobot/static/iimg-thresh.png',thresh)
	cnts = cv2.findContours(thresh.copy(), cv2.RETR_LIST,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if imutils.is_cv2() else cnts[1]
	sd = BoxFinder()

	# loop over the contours
	my_shape = None
	max_area = -1
	my_V = None
	final_list = []
	coordinates = None
	height, width, channels = image.shape
	
	for c in cnts:
		# compute the center of the contour, then detect the name of the
		# shape using only the contour
		M = cv2.moments(c)
		cX = int((M["m10"] / (M["m00"] + 1e-6)) * ratio)
		cY = int((M["m01"] / (M["m00"] + 1e-6)) * ratio)
		shape, V = sd.detect(c)
		# multiply the contour (x, y)-coordinates by the resize ratio,
		# then draw the contours and the name of the shape on the image
		c = c.astype("float")
		c = c.astype("int")

	 	if shape == 'rectangle' or shape == 'square':
	 		area = cv2.contourArea(c)

			if area > (width*height*0.03) and area < (width*height*0.75):

				cv2.drawContours(resized, [c], -1, (255, 255, 255), 20)
				
				my_shape = c
				max_area = area
				my_V = V

				x,y,w,h = cv2.boundingRect(c)

				final_list.append([[x,y,w,h], area])

	final_list.sort(myCompare)
	final_list = [x for x in final_list if x[1] > (width*height*.10)]
	
	print final_list
	
	# If box is found, since the border is thick, they appear as two boxes
	# that are extremely close in area
	if len(final_list) >= 2 and final_list[0][1] - final_list[1][1] < 10:
		coordinates = final_list[0][0]
		cv2.imwrite('/root/server/irobot/static/iimg-thresh.png',resized)

	return my_shape, my_V, coordinates

		
# Takes a snapshot and returns the coordinates of the box 
# Coordinates are based on the box occupying 
# an area of around 10% of image.
# This function does not draw a white border on the box after retrieval

def findBoxWOL(image):

	cv2.imwrite('/root/server/irobot/static/iimg.png',image)
	colors = ['blue','green', 'red']

	resized = image
	ratio  = 1.0
	 
	# convert the resized image to grayscale, blur it slightly,
	# and threshold it
	gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
	inv = cv2.bitwise_not(gray)
	blur = cv2.GaussianBlur(inv, (5, 5), 0)
	
	thresh = cv2.Canny(blur,100,300,apertureSize = 3)

	cv2.imwrite('/root/server/irobot/static/iimg-thresh.png',thresh)
	cnts = cv2.findContours(thresh.copy(), cv2.RETR_LIST,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if imutils.is_cv2() else cnts[1]
	sd = BoxFinder()

	# loop over the contours
	my_shape = None
	max_area = -1
	my_V = None
	final_list = []
	coordinates = None
	height, width, channels = image.shape
	
	for c in cnts:
		# compute the center of the contour, then detect the name of the
		# shape using only the contour
		M = cv2.moments(c)
		cX = int((M["m10"] / (M["m00"] + 1e-6)) * ratio)
		cY = int((M["m01"] / (M["m00"] + 1e-6)) * ratio)
		shape, V = sd.detect(c)
		# multiply the contour (x, y)-coordinates by the resize ratio,
		# then draw the contours and the name of the shape on the image
		c = c.astype("float")
		c = c.astype("int")

	 	if shape == 'rectangle' or shape == 'square':
	 		area = cv2.contourArea(c)

			if area > (width*height*0.03) and area < (width*height*0.75):
			
				my_shape = c
				max_area = area
				my_V = V

				x,y,w,h = cv2.boundingRect(c)

				final_list.append([[x,y,w,h], area])

	final_list.sort(myCompare)
	final_list = [x for x in final_list if x[1] > (width*height*.10)]

	# If box is found, since the border is thick, they appear as two boxes
	# that are extremely close in area
	if len(final_list) >= 2 and final_list[0][1] - final_list[1][1] < 10:
		coordinates = final_list[0][0]
		cv2.imwrite('/root/server/irobot/static/iimg-thresh.png',resized)

	return my_shape, my_V, coordinates

# Compare function used to find largest box

def myCompare(a,b):
    if a[1] > b[1]:
        return -1
    elif a[1] == b[1]:
        if a[0] > b[0]:
            return -1
        else:
            return 1
    else:
        return 1
		
