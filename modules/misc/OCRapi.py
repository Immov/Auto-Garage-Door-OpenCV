import io
import json
import cv2
import numpy as np
import requests
import os
from dotenv import load_dotenv # pip install python-dotenv

def rescaleFrame(frame, scale=0.75):
	width = int(frame.shape[1] * scale)
	height = int(frame.shape[0] * scale)
	dimensions = (width, height)

	return cv2.resize(frame, dimensions, interpolation=cv2.INTER_AREA)

def grayscale(img): # BGR2GRAY
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	img = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
	return img

def draw_text(img, text,
          font=cv2.FONT_HERSHEY_PLAIN,
          pos=(0, 0),
          font_scale=3,
          font_thickness=2,
          text_color=(0, 255, 0),
          text_color_bg=(0, 0, 0)
          ):

    x, y = pos
    text_size, _ = cv2.getTextSize(text, font, font_scale, font_thickness)
    text_w, text_h = text_size
    cv2.rectangle(img, pos, (x + text_w, y + text_h), text_color_bg, -1)
    cv2.putText(img, text, (x, y + text_h + font_scale - 1), font, font_scale, text_color, font_thickness)

    return text_size

load_dotenv()
token = os.getenv('OCR_TOKEN')

image = cv2.imread("Videos/Capture/plat2.jpg")

# image = grayscale(image)
# image = rescaleFrame(image, .5)
height, width= image.shape[:2]


def ocr_call(img):
	height, width = img.shape[:2]
	# Ocr
	url_api = "https://api.ocr.space/parse/image"
	_, compressedimage = cv2.imencode(".jpg", img, [1, 90])
	file_bytes = io.BytesIO(compressedimage)
	result = requests.post(url_api,
				files = {"screenshot.jpg": file_bytes},
				data = {"apikey": token,
						"OCREngine": 1})

	result = result.content.decode()
	result = json.loads(result)
	print(result)
	parsed_results = result.get("ParsedResults")[0]
	text_detected = parsed_results.get("ParsedText")
	return text_detected

plat_nomor = ocr_call((image))

draw_text(image, str(plat_nomor))
cv2.imshow('plat', image)
cv2.waitKey(0)

print(f'Text: {plat_nomor}')