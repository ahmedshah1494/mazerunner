import cv2
import imutils
import numpy as np
from photo import get_image_from_picam
class ShapeDetector:
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
def get_perp_dist(v1,v2):
	c = v2 - v1
	return np.linalg.norm(c)**2 - (v1 / np.linalg.norm(v1)).dot(c)**2

def get_direction(img):
	_,V = process_image(img)
        if len(V) != 3:
                return None
        V = map(lambda x: x.flatten(), V)
	print V
	dist = 2**16	
	for i in range(3):
		for j in range(i,3):
			d = np.abs(V[i][1] - V[j][1])
			if d < dist:
				dist = d
				closest_pair = [i,j]
	print map(lambda x: V[x], closest_pair)
	tip = filter(lambda x: x not in closest_pair, range(len(V)))[0]
	tip = V[tip]
	if tip[1] < V[closest_pair[0]][0]:
		return 'left'
	else:
		return 'right'
	
def _get_direction(img):
	_,V = process_image(img)
	if len(V) != 3:
		return None
	V = map(lambda x: x.flatten(), V)
	print V
	a = V[0] - V[1]
	b = V[2] - V[1]
	c = V[2] - V[0]
	sides = [a,b,c]
	dist = 0
	max_perp =0 
	for i in range(len(sides)):
		for j in range(len(sides)):
			if i == j:
				continue
			v1 =sides[i]
			v2 = sides[j]
			dist = get_perp_dist(v1,v2)
                        print v1, v2, dist
                        if dist > max_perp:
                                max_perp = dist
                                if v2[0] > v1[0]:
                                        direction = 'right'
                                else:
                                        direction = 'left'
	return direction
			
def _get_direction(img):
	_,V = process_image(img)
	max_perp = 0
	for i in range(len(V)):
		for j in range(len(V)):
			v1 = V[i].flatten()
			v2 =V[j].flatten()
			if i == j:
				continue
			dist = get_perp_dist(v1,v2)
			print v1, v2, dist
			if dist > max_perp:
				max_perp = dist
				if v2[0] > v1[0]:
					direction = 'right'
				else:
					direction = 'left'
	return direction

def process_image(image):
	# cv2.imshow('', image)
	# cv2.waitKey(0)
	cv2.imwrite('img.png',image)
	colors = ['blue','green', 'red']
	# load the image and resize it to a smaller factor so that
	# the shapes can be approximated better
	# image = cv2.imread("green.jpg")
	# resized = imutils.resize(image, width=300)
	# ratio = image.shape[0] / float(resized.shape[0])
	resized = image
	ratio  = 1.0
	 
	# convert the resized image to grayscale, blur it slightly,
	# and threshold it
	gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
	inv = cv2.bitwise_not(gray)
	blur = cv2.GaussianBlur(inv, (5, 5), 0)
	_,thresh = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
#	cv2.imshow('Thresh', thresh) 
	# find contours in the thresholded image and initialize the
	# shape detector
	cv2.imwrite('img-thresh.png',thresh)
	cnts = cv2.findContours(thresh.copy(), cv2.RETR_LIST,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if imutils.is_cv2() else cnts[1]
	sd = ShapeDetector()

	# loop over the contours
	my_shape = None
	max_area = -1
	my_V = None
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
		# c *= ratio
		c = c.astype("int")
		# cv2.drawContours(resized, [c], -1, (0, 255, 0), 2)
		# cv2.putText(resized, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,
		# 	0.5, (255, 255, 255), 2)
		# cv2.imshow("Image", resized)
		# cv2.waitKey(0)
#		print shape
	 	if shape == 'triangle':
	 		area = cv2.contourArea(c)
			if area > max_area:
				cv2.drawContours(resized, [c], -1, (0, 255, 0), 2)
				cv2.putText(resized, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,
				0.5, (255, 255, 255), 2)
				
				my_shape = c
				max_area = area
				my_V = V
			# show the output image
#				cv2.imshow("Image", resized)
#				cv2.waitKey(0)
#				print shape,area
	return my_shape, my_V
def get_color(resized, my_V, my_shape):
	mask = np.zeros_like(resized)
	print my_V.shape
	cv2.drawContours(mask,[my_shape],-1,color=255,thickness=-1)
	cv2.fillPoly(mask,pts=np.int32([my_shape]),color=(255,255,255))
	cv2.imwrite('img-mask.png', mask)
#	cv2.waitKey(0)
	points = np.where(mask == 255)
#	print points[2]
	pixels = []
	for i in range(len(points[0])):
		pixel = (resized[points[0][i], points[1][i]])
		pixels.append(pixel)
	pixels = np.array(pixels)
	color = np.mean(pixels,axis=0)
#	print color
	return colors[np.argmax(color)]
#img = get_image_from_picam()
#img = get_image(0)
#img = cv2.imread("img.jpg")
#print get_direction(img)
