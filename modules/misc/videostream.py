import cv2
import numpy as np


def rescaleFrame(frame, scale=0.75):
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    dimensions = (width, height)
    return cv2.resize(frame, dimensions, interpolation=cv2.INTER_AREA)


path = 'http://192.168.1.8/mjpeg/1'
# File: 'Videos/car.mp4'
# Network: 'http://192.168.1.51:4747/video'

cap = cv2.VideoCapture(path)
# cap = cv2.VideoCapture(0) # Webcam

output = 'resource/results'

fps = 30
framecount = 0
while True:
    success, frame = cap.read()
    # frame = rescaleFrame(frame, .5)
    if (framecount % (fps/1) == 0):  # Detecting every 1 second
        cv2.imshow('Detect', frame)
    cv2.imshow('Video', frame)
    if cv2.waitKey(20) & 0xFF == ord('d'):  # if d is pressed, then break
        break
    framecount += 1

cap.release()
cv2.destroyAllWindows()
cv2.waitKey(0)
