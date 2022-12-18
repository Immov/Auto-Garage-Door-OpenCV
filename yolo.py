import cv2
import numpy as np

# # Yolo v3-tiny
# yolo_weights = "yolov3-tiny.weights"
# yolo_cfg = "yolov3-tiny.cfg"

# # Yolo v2-tiny
# yolo_weights = "yolov2-tiny.weights"
# yolo_cfg = "yolov2-tiny.cfg"

# # Yolo v3
# yolo_weights = "yolov3.weights"
# yolo_cfg = "yolov3.cfg"

# Yolo v7-tiny
yolo_weights = "yolov7-tiny.weights"
yolo_cfg = "yolov7-tiny.cfg"



def get_output_layers(net):
	layer_names = net.getLayerNames()
	try:
		output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
	except:
		output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
	return output_layers

def detect_cars(image, frame_num):
	# load our yolov7 model
	net = cv2.dnn.readNet("yolov7-tiny.weights", "yolov7-tiny.cfg")
	# get the image height, width and shape
	height, width, channels = image.shape
	# create a blob from the image
	blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
	# set the input to the network
	net.setInput(blob)
	# run the forward pass
	outs = net.forward(get_output_layers(net))
	# initialize the list of detected cars
	detected_cars = []
	# loop over the detections
	for out in outs:
		# loop over each detection
		for detection in out:
			# get the score and class
			scores = detection[5:]
			class_id = np.argmax(scores)
			# ignore everything except cars
			if class_id == 2: #2 == cars
				# get the confidence and center coordinates
				confidence = float(scores[class_id])
				x = int(detection[0] * width)
				y = int(detection[1] * height)
				w = int(detection[2] * width)
				h = int(detection[3] * height)

				center_x = int(detection[0] * width)
				center_y = int(detection[1] * height)
				w = int(detection[2] * width)
				h = int(detection[3] * height)
				# Add to list of bounding boxes
				x = int(center_x - w / 2)
				y = int(center_y - h / 2)

				detected_cars.append((x, y, w, h))

	print(detected_cars)

	# Export each cars
	i=0
	for car in detected_cars:
		x, y, w, h = car
		cv2.imwrite(f'Images/Result/{frame_num}-CAR-{i}-X{x}.Y{y}-.jpg', image[y:y+h, x:x+w])
		i+=1

	# draw the bounding boxes on the image
	i = 0
	for car in detected_cars:
		x, y, w, h = car
		cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 1)
		i+=1
	if(i!=0):
		print(f"{i} Car feature is detected!")
	else:
		print("No car is detected")