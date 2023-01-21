import cv2
import pytesseract


# Read the image
image = cv2.imread('resource/images/plate/plat1.jpg')
# image = rescaleFrame(image, .5)

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Run OCR using Tesseract
text = pytesseract.image_to_string(gray)
cv2.imshow('Image', image)
print(text)
cv2.waitKey(0)
