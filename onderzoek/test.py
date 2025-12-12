import cv2
import time

start, end = 0, 0
cap = cv2.VideoCapture(0)
for i in range(95):
    start = time.perf_counter()
    _, frame = cap.read()
    _, b = cv2.imencode(".jpg", frame, (cv2.IMWRITE_JPEG_QUALITY, i + 1))
    end = time.perf_counter()
    print(f"{i}: {end - start}, {len(b)}")
