# Find largest box
def find_largest_box(boxes):
  largest_box = None
  largest_area = 0
  for box in boxes:
    x, y, w, h = box
    area = w * h
    if area > largest_area:
      largest_area = area
      largest_box = box
  return largest_box

# Removes duplicated boxes
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
