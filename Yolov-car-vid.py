import cv2
import numpy as np
import yolo

def rescaleFrame(frame, scale=0.75):
	width = int(frame.shape[1] * scale)
	height = int(frame.shape[0] * scale)
	dimensions = (width, height)
	return cv2.resize(frame, dimensions, interpolation=cv2.INTER_AREA)

# cap = cv2.VideoCapture(0) # Webcam
# cap = cv2.VideoCapture('Videos/Small/Forza.mp4') # File
cap = cv2.VideoCapture('Videos/car.mp4') # File
# cap = cv2.VideoCapture('http://192.168.1.51:4747/video') # Network

fps = 30
framecount = 0
while True:
	success, frame = cap.read()
	frame = rescaleFrame(frame, .5)
	if(framecount%(fps/1)==0): #Detecting every 1 second
		print("Detecting...")
		yolo.detect_cars(frame)
	cv2.imshow('Video',frame)
	if cv2.waitKey(20) & 0xFF==ord('d'): # if d is pressed, then break
		break
	framecount+=1

cap.release()
cv2.destroyAllWindows()
cv2.waitKey(0)