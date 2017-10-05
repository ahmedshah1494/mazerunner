import cv2
import pytesseract
from PIL import Image

import numpy as np

def image2text(image, isTag):

	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	gray =  cv2.bitwise_not(gray)
	gray = cv2.medianBlur(gray,3)
	_,gray = cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

	filename = "/root/server/irobot/static/snapshots/temp.png"
	cv2.imwrite(filename, gray)
		
	img = Image.open(filename)

	if isTag == 0:
		return pytesseract.image_to_string(img)
	else:
		text = pytesseract.image_to_string(img, config='-psm 9 -c tessedit_char_whitelist=ABCDEFX[]')
		if len(text) == 0:
			text = pytesseract.image_to_string(img, config='-c tessedit_char_whitelist=ABCDEFX[]')
		# print text
		return text

if __name__=='__main__':
	import photo
	from picamera import PiCamera
	camera = PiCamera()
	img = photo.get_image_from_picam(camera)
	cv2.imwrite('text_cam.png', img)
	print(image2text(img))
