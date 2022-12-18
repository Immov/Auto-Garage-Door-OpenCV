import cv2
import numpy as np

def merge_boxes(boxes, threshold):
    # Make a copy of the list of boxes
    boxes = boxes.copy()

    # Iterate over the list of boxes
    for i, box1 in enumerate(boxes):
        for j, box2 in enumerate(boxes[i+1:]):
            # Calculate the distance between the two boxes
            dist_x = abs(box1[0] - box2[0])
            dist_y = abs(box1[1] - box2[1])
            dist = (dist_x ** 2 + dist_y ** 2) ** 0.5

            # If the distance is less than the threshold, merge the boxes
            if dist < threshold:
                # Merge the boxes by taking the minimum and maximum values of the coordinates
                x1 = min(box1[0], box2[0])
                y1 = min(box1[1], box2[1])
                x2 = max(box1[0] + box1[2], box2[0] + box2[2])
                y2 = max(box1[1] + box1[3], box2[1] + box2[3])
                w = x2 - x1
                h = y2 - y1
                box1 = (x1, y1, w, h)

                # Remove the duplicated box from the list
                boxes.pop(i+j+1)

    # Return the list of merged boxes
    return boxes



boxes = [(133, 174, 20, 13), (132, 175, 20, 12), (157, 176, 19, 12), (133, 176, 18, 12), (132, 176, 19, 12), (132, 176, 19, 12), (160, 176, 15, 12), (158, 176, 18, 12), (366, 176, 30, 18), (366, 176, 30, 18), (366, 176, 30, 18), (367, 176, 28, 16), (367, 175, 28, 17), (367, 175, 28, 17), (391, 177, 45, 19), (391, 177, 45, 19), (392, 177, 44, 19), (90, 169, 45, 36), (204, 174, 45, 33), (204, 175, 45, 32), (204, 175, 45, 32), (389, 177, 45, 19), (390, 177, 45, 19), (390, 177, 46, 19), (462, 176, 67, 32), (205, 176, 46, 31), (508, 184, 74, 28), (576, 183, 63, 36), (576, 183, 63, 35), (577, 183, 62, 35), (84, 168, 51, 37), (84, 168, 51, 37), (204, 175, 45, 32), (363, 176, 32, 17), (392, 177, 46, 20), (390, 177, 47, 20), (464, 176, 62, 32), (465, 176, 62, 32), (511, 184, 69, 28), (512, 184, 68, 28), (85, 169, 51, 38), (204, 174, 46, 33), (204, 174, 46, 33), (465, 176, 62, 32), (511, 184, 69, 28), (512, 184, 68, 27), (511, 184, 70, 28), (511, 184, 70, 28), (510, 184, 71, 28), (577, 182, 62, 37), (577, 182, 62, 37), (577, 181, 62, 37), (577, 182, 62, 38), (577, 182, 62, 38), (577, 181, 62, 38), (577, 182, 62, 37)]
threshold = 25
merged_boxes = merge_boxes(boxes, threshold)
print(merged_boxes)

blank = np.zeros((500, 800), dtype='uint8')
# rect = cv2.rectangle(blank.copy(), (30,30), (370, 370), 255, thickness=-1)

i=0
for car in boxes:
	x, y, w, h = car
	cv2.rectangle(blank, (x, y), (x+w, y+h), 255, thickness=1)
	i+=1
print(i)

cv2.imshow("img", blank)
cv2.waitKey(0)
cv2.destroyAllWindows()