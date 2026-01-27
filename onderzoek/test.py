import cv2
import t

start = 0
cap = cv2.VideoCapture(0)
while cv2.waitKey(1) != ord('q'):
    start = t.perf_counter()
    _, frame = cap.read()
    # _, b = cv2.imencode(".webp", frame, (cv2.IMWRITE_WEBP_QUALITY, 50))
    _, b = cv2.imencode(".jpg", frame, (cv2.IMWRITE_JPEG_QUALITY, 50))
    print(len(b), t.perf_counter() - start)
    cv2.imshow("dikke", cv2.imdecode(b, cv2.IMREAD_COLOR))
