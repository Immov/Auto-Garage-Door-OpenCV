# Automatic Garage Door

## Deskripsi
### Computer vision project menggunakan OpenCV

**Algoritma**: [Yolo](https://pjreddie.com/darknet/yolo/) (real-time object detection)<br>


## Instalasi

- [Python](https://www.python.org/downloads/)
- [Python pip](https://pip.pypa.io/en/stable/installation/)
- Open CV `pip install opencv-python`
- Tesseract `pip install pytesseract` and [Tesseract OCR Executables (Required)](https://tesseract-ocr.github.io/tessdoc/Downloads.html
)
- imutils `pip install imutils`
- YoloV7 [Weights and config](https://github.com/pjreddie/darknet/issues/2557)
- Aplikasi [DroidCam](https://play.google.com/store/apps/details?id=com.dev47apps.droidcam)

## Cara menggunakan
- Letakan [YoloV7 Weights and config](https://github.com/pjreddie/darknet/issues/2557) pada folder `/YOLO/`
- Letakan video pada folder `/resource/videos`
- Jalankan program menggunakan perintah `python main.py` pada terminal
- Ubah source feed pada kode
	```python
	path = 'resource/videos/lands1.mp4'
	# File: 'Videos/car.mp4' 
	# Network: 'http://192.168.1.51:4747/video'

	cap = cv2.VideoCapture(path)
	# cap = cv2.VideoCapture(0) # Webcam
	```
- Apabila menggunakan [DroidCam](https://play.google.com/store/apps/details?id=com.dev47apps.droidcam) sebagai sumber, ganti linknya sesuai network masing-masing
	![](https://i.imgur.com/7493bLr.jpeg)

## Flow
1. Fetch a video feed from esp32
2. Detect cars using YOLOv7
3. YOLO script executute car detection
4. Error is reduced by merging duplicated boxes
5. Largest car is then parsed and expored with respective frame number
1. Execute number Plate detection using OCR
7. Numberplate storing and matching
8. If match, send a trigger to ESP32-CAM

## Progress
- [x] Live Video feed
- [x] Yolo Car Detection
- [x] Reduce duplicated boxes
- [x] Car parsing
- [ ] Number plate OCR
- [ ] Number plate store and matching
- [ ] Sending Trigger


## Source Used
- https://github.com/AlexeyAB/darknet