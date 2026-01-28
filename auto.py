import time as t
import socket
import cv2

running = True
port = 5000
left_counter = 0
right_counter = 0
then = t.time()
now = 0
sock: socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind("0.0.0.0", port)
_, addr = sock.recvfrom(100)


def send_cam():
    global running
    cap = cv2.VideoCapture(0)
    while running:
        _, frame = cap.read()
        _, buffer = cv2.imencode(".webp", frame,
                                 (cv2.IMWRITE_WEBP_QUALITY, 70))
        buffer = buffer.tobytes()
        sock.sendto(buffer, addr)


def receive():
    global running
    while running:
        buffer, _ = sock.recvfrom(1)
        buffer = buffer.decode()
        if buffer == "l":
            left_counter = 1.1
        elif buffer == "r":
            right_counter = 1.1
        elif buffer == "q":
            running = False



while True:
    pass
