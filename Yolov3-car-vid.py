import cv2
import numpy as np

def get_output_layers(net):
    layer_names = net.getLayerNames()
    try:
        output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
    except:
        output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    return output_layers

def yolov3car(gambar):
	# Load Yolo
	net = cv2.dnn.readNet("yolov3-tiny.weights", "yolov3-tiny.cfg") # get from https://pjreddie.com/darknet/yolo/
	# Name custom object
	classes = ["car"]
	# Create blob
	blob = cv2.dnn.blobFromImage(gambar, 1/255, (416, 416), (0, 0, 0), True, crop=False)
	Width = gambar.shape[1]
	Height = gambar.shape[0]
	# Set the input the the net
	net.setInput(blob)
	# Get the output layers
	outs = net.forward(get_output_layers(net))
	# Initialize list of detected bounding boxes
	bounding_boxes = []
	# Loop over the layers and get the detected bounding boxes
	for out in outs:
		for detection in out:
			# Get the score
			scores = detection[5:]
			class_id = np.argmax(scores)
			confidence = scores[class_id]
			# Get the bounding box
			if confidence > 0.7:
				# Rescale the bounding box
				center_x = int(detection[0] * Width)
				center_y = int(detection[1] * Height)
				w = int(detection[2] * Width)
				h = int(detection[3] * Height)
				# Add to list of bounding boxes
				x = int(center_x - w / 2)
				y = int(center_y - h / 2)
				bounding_boxes.append([x, y, w, h])
				# Draw rectangle
				cv2.rectangle(gambar, (x, y), (x + w, y + h), (0, 255, 0), 2)
	return gambar

def rescaleFrame(frame, scale=0.75):
	width = int(frame.shape[1] * scale)
	height = int(frame.shape[0] * scale)
	dimensions = (width, height)

	return cv2.resize(frame, dimensions, interpolation=cv2.INTER_AREA)

# cap = cv2.VideoCapture(0) # Webcam
# cap = cv2.VideoCapture('Videos/Small/Forza.mp4') # File
cap = cv2.VideoCapture('Videos/car.mp4') # File
# cap = cv2.VideoCapture('http://192.168.1.51:4747/Video') # Network

# FPS Limiter
fps = 30
target_fps = 5
fps_timer = fps/target_fps
start_frame_number = 0


while True:
	cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame_number)
	success, frame = cap.read()
	# frame = rescaleFrame(frame, scale=.4)
	frame = yolov3car(frame)
	cv2.imshow('Video', frame)
	if cv2.waitKey(20) & 0xFF==ord('d'): # if d is pressed, then break
		break
	start_frame_number+=fps_timer


cap.release()
cv2.destroyAllWindows()

cv2.waitKey(0)