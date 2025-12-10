import socket
import cv2

port = 5000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", port))

cap = cv2.VideoCapture(0)
frame = None

while True:
    data, addr = sock.recvfrom(1024)
    for _ in range(10):
        _, frame = cap.read()
        cv2.imshow("Stream", frame)
    print(data.decode())
    sock.sendto("bam!".encode(), addr)
