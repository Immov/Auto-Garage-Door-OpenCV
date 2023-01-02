# https://unydevelopernetwork.com/index.php/2021/05/03/membuat-deteksi-plat-nomer-kendaraan-sederhana-dengan-opencv-python/

import cv2 as cv
import imutils as im

path = 'resource/images/1.jpg' # too large
path = 'resource/images/Plate/plat2.jpg' #working
image = cv.imread(path)
image = im.resize(image, width=500)

gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
blur = cv.bilateralFilter(gray, 11, 17, 17)
edgeDet = cv.Canny(blur, 170, 200)
(cnts, _) = cv.findContours(edgeDet.copy(), cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
cnts = sorted(cnts, key = cv.contourArea, reverse = True)[:30]
NumberPlateCnt = None

count = 0
for c in cnts:
        peri = cv.arcLength(c, True)
        approx = cv.approxPolyDP(c, 0.02 * peri, True)
        if len(approx) == 4:
            NumberPlateCnt = approx
            break

cv.drawContours(image, [NumberPlateCnt], -1, (0,255,0), 3)
# cv.imwrite('hasildeteksi.jpg', image)
cv.imshow("Plat Nomer Yang Terdeteksi", image)

cv.waitKey(0)
cv.destroyAllWindows()