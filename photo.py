import cv2
print cv2.__version__
from picamera.array import PiRGBArray
import time

def get_image_from_picam(camera):
	rawCapture = PiRGBArray(camera)
 
	# allow the camera to warmup
	time.sleep(0.1)
 
	# grab an image from the camera
	camera.capture(rawCapture, format="bgr")
	image = rawCapture.array
#	image = cv2.flip( image, 0 )
	return image
def get_image(dev_id):

	cap = cv2.VideoCapture(dev_id)
	print cap.set(cv2.CAP_PROP_BRIGHTNESS, 120)
	# print cap.set(cv2.CAP_PROP_GAIN, 0)

	test = cap.get(cv2.CAP_PROP_POS_MSEC)
	ratio = cap.get(cv2.CAP_PROP_POS_AVI_RATIO)
	frame_rate = cap.get(cv2.CAP_PROP_FPS)
	width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
	height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
	brightness = cap.get(cv2.CAP_PROP_BRIGHTNESS)
	contrast = cap.get(cv2.CAP_PROP_CONTRAST)
	saturation = cap.get(cv2.CAP_PROP_SATURATION)
	hue = cap.get(cv2.CAP_PROP_HUE)
	gain = cap.get(cv2.CAP_PROP_GAIN)
	exposure = cap.get(cv2.CAP_PROP_EXPOSURE)
	autoexp = cap.get(cv2.CAP_PROP_AUTO_EXPOSURE)
	print("Test: ", test)
	print("Ratio: ", ratio)
	print("Frame Rate: ", frame_rate)
	print("Height: ", height)
	print("Width: ", width)
	print("Brightness: ", brightness)
	print("Contrast: ", contrast)
	print("Saturation: ", saturation)
	print("Hue: ", hue)
	print("Gain: ", gain)
	print("Exposure: ", exposure)
	print("Auto Exposure", autoexp)
	r, img = cap.read()
	return img
# cv2.imshow('',get_image(1))
# cv2.waitKey(0)
