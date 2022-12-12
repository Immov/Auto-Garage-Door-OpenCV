import io
import json
import cv2
import numpy as np
import requests
import os
from dotenv import load_dotenv # pip install python-dotenv

load_dotenv()
token = os.getenv('OCR_TOKEN')

image = cv2.imread("Images/plate.jpg")

def ocr_call(img):
	height, width, _ = img.shape
	# Ocr
	url_api = "https://api.ocr.space/parse/image"
	_, compressedimage = cv2.imencode(".jpg", img, [1, 90])
	file_bytes = io.BytesIO(compressedimage)
	result = requests.post(url_api,
				files = {"screenshot.jpg": file_bytes},
				data = {"apikey": token,
						"language": "eng"})

	result = result.content.decode()
	result = json.loads(result)
	parsed_results = result.get("ParsedResults")[0]
	text_detected = parsed_results.get("ParsedText")
	return text_detected

plat_nomor = ocr_call((image))

print(f'Text: {plat_nomor}')