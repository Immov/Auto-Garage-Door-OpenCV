# Apa yang dibutuhkan

- [Python](https://www.python.org/downloads/)
- Open CV `pip install opencv-python`
- Tesseract `pip install pytesseract` and [Tesseract OCR Executables (Required)](https://tesseract-ocr.github.io/tessdoc/Downloads.html
)
- imutils `pip install imutils`
- YOLO [Weights and config](https://github.com/pjreddie/darknet/issues/2557)


# Source Used
- https://github.com/AlexeyAB/darknet

# Flow
1. Fetch a video feed from esp32
2. Detect cars using YOLOv7
3. YOLO script executute car detection
4. Error is reduced by merging duplicated boxes
5. Largest car is then parsed and expored with respective frame number
6. Execute number Plate detection using OCR
7. Numberplate storing and matching
8. If match, send a trigger to ESP32-CAM

# Progres

- [x] Live Video feed
- [x] Yolo Car Detection
- [x] Reduce duplicated boxes
- [x] Car parsing
- [ ] Number plate OCR
- [ ] Number plate store and matching
- [ ] Sending Trigger

