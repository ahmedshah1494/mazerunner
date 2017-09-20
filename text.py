import cv2
import pytesseract
from PIL import Image

def image2text(image):
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	gray =  cv2.bitwise_not(gray)
	gray = cv2.threshold(gray, 200, 255,
			cv2.THRESH_BINARY)[1]
	gray = cv2.medianBlur(gray, 3)
	filename = "temp.png"
	cv2.imwrite(filename, gray)
	img = Image.open("temp.png")
	text = pytesseract.image_to_string(img)
	return text

if __name__=='__main__':
	import photo
	from picamera import PiCamera
	camera = PiCamera()
	img = photo.get_image_from_picam(camera)
	cv2.imwrite('text_cam.png', img)
	print(image2text(img))
