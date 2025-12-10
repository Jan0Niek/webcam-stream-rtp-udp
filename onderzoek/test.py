import cv2
import time

cap = cv2.VideoCapture(0)
while True:
    r, frame = cap.read()
    # _, buffer = cv2.imencode(".png", frame)
    # cv2.imshow("bam!", buffer)
    cv2.imshow("Stream", frame)
    time.sleep(0.0001)
input()
