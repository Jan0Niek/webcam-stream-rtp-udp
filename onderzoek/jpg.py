import cv2
import time
import turbojpeg
import json

tjpg = turbojpeg.TurboJPEG()
start, t = 0, 0
cap = cv2.VideoCapture(0)
result = [[0] * 10 for _ in range(95)]
for i in range(95):
    for j in range(10):
        start = time.perf_counter()
        _, frame = cap.read()
        _, b = cv2.imencode(".jpg", frame, (cv2.IMWRITE_JPEG_QUALITY, i + 1))
        # b = tjpg.encode(frame, quality=i)
        t = time.perf_counter() - start
        size = len(b)
        result[i][j] = (t, size)
        print(f"{i}: {t}, {size}")

with open("jpg.json", "w") as f:
    json.dump(result, f)
