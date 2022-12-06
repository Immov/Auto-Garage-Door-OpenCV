import cv2

cap = cv2.VideoCapture('http://192.168.1.51:4747/video')

cv2.namedWindow('live cam', cv2.WINDOW_NORMAL)

while(True):
    ret, frame = cap.read()
    #img_resize = cv2.resize(frame, (960, 540))
    cv2.imshow('live cam', frame)
    if cv2.waitKey(50) & 0xFF == ord('q'):
        break

cv2.waitKey(0)
cv2.destroyAllWindows()