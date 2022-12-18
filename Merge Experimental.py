import cv2
import numpy as np

def merge_boxes(boxes, treshold):
    # Initialize empty list for merged boxes
    merged_boxes = []

    # Sort boxes by x-coordinate
    boxes.sort(key=lambda x: x[0])

    # Iterate over boxes and try to merge them
    while len(boxes) > 0:
        box = boxes.pop(0)
        merged = False
        for i, mbox in enumerate(merged_boxes):
            if abs(box[0] - mbox[0]) < treshold and abs(box[1] - mbox[1]) < treshold:
                # Merge boxes
                merged_boxes[i] = (min(box[0], mbox[0]), min(box[1], mbox[1]), max(box[2], mbox[2]), max(box[3], mbox[3]))
                merged = True
                break
        if not merged:
            merged_boxes.append(box)

    return merged_boxes


# Test the function with some example boxes

boxes = [(133, 174, 20, 13), (132, 175, 20, 12), (157, 176, 19, 12), (133, 176, 18, 12), (132, 176, 19, 12), (132, 176, 19, 12), (160, 176, 15, 12), (158, 176, 18, 12), (366, 176, 30, 18), (366, 176, 30, 18), (366, 176, 30, 18), (367, 176, 28, 16), (367, 175, 28, 17), (367, 175, 28, 17), (391, 177, 45, 19), (391, 177, 45, 19), (392, 177, 44, 19), (90, 169, 45, 36), (204, 174, 45, 33), (204, 175, 45, 32), (204, 175, 45, 32), (389, 177, 45, 19), (390, 177, 45, 19), (390, 177, 46, 19), (462, 176, 67, 32), (205, 176, 46, 31), (508, 184, 74, 28), (576, 183, 63, 36), (576, 183, 63, 35), (577, 183, 62, 35), (84, 168, 51, 37), (84, 168, 51, 37), (204, 175, 45, 32), (363, 176, 32, 17), (392, 177, 46, 20), (390, 177, 47, 20), (464, 176, 62, 32), (465, 176, 62, 32), (511, 184, 69, 28), (512, 184, 68, 28), (85, 169, 51, 38), (204, 174, 46, 33), (204, 174, 46, 33), (465, 176, 62, 32), (511, 184, 69, 28), (512, 184, 68, 27), (511, 184, 70, 28), (511, 184, 70, 28), (510, 184, 71, 28), (577, 182, 62, 37), (577, 182, 62, 37), (577, 181, 62, 37), (577, 182, 62, 38), (577, 182, 62, 38), (577, 181, 62, 38), (577, 182, 62, 37)]
tolerance = 10
merged_boxes = merge_boxes(boxes, tolerance)
print(merged_boxes)


blank = np.zeros((500, 800), dtype='uint8')
# rect = cv2.rectangle(blank.copy(), (30,30), (370, 370), 255, thickness=-1)

i=0
for car in merged_boxes:
	x, y, w, h = car
	cv2.rectangle(blank, (x, y), (x+w, y+h), 255, thickness=1)
	i+=1
print(i)

cv2.imshow("img", blank)
cv2.waitKey(0)
cv2.destroyAllWindows()