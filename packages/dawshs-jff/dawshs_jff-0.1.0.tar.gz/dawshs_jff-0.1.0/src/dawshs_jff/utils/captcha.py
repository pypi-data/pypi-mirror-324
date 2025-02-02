import base64

import cv2
import time

import numpy as np
import pytesseract

t_end = time.time() + 30
count = 0


def solve_mng_captcha(b64_image: str):
    im_bytes = base64.b64decode(b64_image)
    im_arr = np.frombuffer(im_bytes, dtype=np.uint8)
    img = cv2.imdecode(im_arr, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(
        img, None, fx=10, fy=10, interpolation=cv2.INTER_LINEAR
    )
    img = cv2.medianBlur(img, 9)
    th, img = cv2.threshold(img, 120, 250, cv2.THRESH_BINARY)
    text = pytesseract.image_to_string(
        img,
        config="--psm 8 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ --dpi 70",
    )
    return text
