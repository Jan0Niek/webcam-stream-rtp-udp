import cv2
# import time

cap = cv2.VideoCapture(0)
for _ in range(10):
    r, frame = cap.read()
    # _, buffer = cv2.imencode(".png", frame)
    # cv2.imshow("bam!", buffer)
    cv2.imshow("Stream", frame)
    cv2.waitKey(1)  # waarom?!?!?
