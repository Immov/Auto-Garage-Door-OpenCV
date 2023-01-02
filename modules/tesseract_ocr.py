import cv2
import pytesseract

def rescaleFrame(frame, scale=0.75):
	width = int(frame.shape[1] * scale)
	height = int(frame.shape[0] * scale)
	dimensions = (width, height)
	return cv2.resize(frame, dimensions, interpolation=cv2.INTER_AREA)

def OCR(image):
	# Convert the image to grayscale
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	# Run OCR using Tesseract
	text = pytesseract.image_to_string(gray)
	return text

'''
# Read the image
image = cv2.imread('Videos/Capture/1.jpg')
# image = rescaleFrame(image, .5)

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Run OCR using Tesseract
text = pytesseract.image_to_string(gray)
cv2.imshow('Image', image)
print(text)
cv2.waitKey(0)
'''

