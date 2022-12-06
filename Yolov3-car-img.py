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
	net = cv2.dnn.readNet("yolov3-tiny.weights", "yolov3-tiny.cfg")
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
			if confidence > 0.5:
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

# Images path
image = cv2.imread("Images/red1.jpg")

image = yolov3car(image)

# Show the output image
cv2.imshow("object detection", image)
cv2.waitKey()
cv2.destroyAllWindows()