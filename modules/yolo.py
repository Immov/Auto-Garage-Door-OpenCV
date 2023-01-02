import cv2
import numpy as np
import time
from modules import tesseract_ocr as ocr
from modules import boxes

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
yolo_weights = "YOLO\yolov7-tiny.weights"
yolo_cfg = "YOLO\yolov7-tiny.cfg"


def get_output_layers(net):
	layer_names = net.getLayerNames()
	try:
		output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
	except:
		output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
	return output_layers

def detect_cars(img, frame_num, path):
	image = img.copy()
	net = cv2.dnn.readNet(yolo_weights, yolo_cfg)
	height, width, channels = image.shape
	blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
	net.setInput(blob)
	outs = net.forward(get_output_layers(net))
	detected_cars = []
	# loop over the detections
	start_time = time.time()
	for out in outs:
		# loop over each detection
		for detection in out:
			# get the score and class
			scores = detection[5:]
			class_id = np.argmax(scores)
			if class_id == 2: #2 == cars
				# get the confidence and center coordinates
				confidence = float(scores[class_id])
				# x = int(detection[0] * width)
				# y = int(detection[1] * height)
				# w = int(detection[2] * width)
				# h = int(detection[3] * height)

				center_x = int(detection[0] * width)
				center_y = int(detection[1] * height)
				w = int(detection[2] * width)
				h = int(detection[3] * height)
				# Add to list of bounding boxes
				x = int(center_x - w / 2)
				y = int(center_y - h / 2)

				detected_cars.append((x, y, w, h))
	end_time = time.time()

	elapsed_time = end_time - start_time
	# print(f'Yolo detecting for {elapsed_time:.6f} seconds')
	detected_cars = boxes.merge_boxes(detected_cars, 10)

	''' Every 5 seconds
	i=0
	if(frame_num%150==0):
		# Export each cars
		for car in detected_cars:
			x, y, w, h = car
			if(x<0):
				x=0
			if(y<0):
				y=0
			cv2.imwrite(f'Images/Result/FRAME{frame_num}-CAR{i}.jpg', image[y:y+h, x:x+w])
			i+=1
		print(f'{i} IMAGES at FRAME {frame_num} EXPORTED...')
	'''

	if len(detected_cars)>0:
		largest = boxes.find_largest_box(detected_cars)
		if(frame_num%90==0): # every 3 seconds
			x, y, w, h = largest
			if(x<0):
				x=0
			if(y<0):
				y=0
			cropped = image[y:y+h, x:x+w]
			cv2.imwrite(f'{path}/FRAME{frame_num}-LARGEST.jpg', cropped)
			print(f'LARGEST CAR AT FRAME {frame_num} EXPORTED...')
			number = ocr.OCR(cropped)
			print(f'Detected Text: {number}')
	else:
		print("No detected")

	# draw the bounding boxes on the image
	i = 0
	for car in detected_cars:
		x, y, w, h = car
		cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)
		i+=1
	if(i!=0):
		print(f"{i} Car feature is detected!")
	else:
		print("No car is detected")

	return image