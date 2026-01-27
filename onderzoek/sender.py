import socket
import cv2

port = 5000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", port))

cap = cv2.VideoCapture(0)

_, addr = sock.recvfrom(100)
while True:
    _, frame = cap.read()
    _, buffer = cv2.imencode(".webp", frame, (cv2.IMWRITE_WEBP_QUALITY, 70))
    buffer = buffer.tobytes()
    sock.sendto(buffer, addr)

