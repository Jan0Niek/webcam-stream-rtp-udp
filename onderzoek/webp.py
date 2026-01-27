import cv2
import time
import json

start, t = 0, 0
result = [[0] * 10 for _ in range(95)]
cap = cv2.VideoCapture(0)
for i in range(95):
    for j in range(10):
        start = time.perf_counter()
        _, frame = cap.read()
        _, b = cv2.imencode(".webp", frame, (cv2.IMWRITE_WEBP_QUALITY, i + 1))
        t = time.perf_counter() - start
        size = len(b)
        result[i][j] = (t, size)
        print(f"{i}: {t}, {size}")

with open("webp.json", "w") as f:
    json.dump(result, f)
