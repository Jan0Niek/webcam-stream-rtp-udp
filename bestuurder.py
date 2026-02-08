import socket
import keyboard
import threading
import cv2

port = 5000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
addr = socket.gethostbyname('autootje')

sock.bind(addr, port)
sock.sendto("zinloze data".encode(), addr)


def send_input():
    """verstuurt de inputs als 4 bits in één byte naar de auto"""
    inputs = 0
    while True:
        inputs = sum(1 << i for i, keyBtn in enumerate("qaed")
                     if keyboard.is_pressed(keyBtn))
        buffer = inputs.to_bytes()
        sock.sendto(buffer, addr)


def receive_footage():
    """ontvangt camerabeelden en pleurt ze in een cv2 display window ter weergave"""
    while True:
        buffer, _ = sock.recvfrom(1024)
        buffer = buffer.decode()
        cv2.imshow("accuPercentage hier?", cv2.imdecode(buffer, cv2.IMREAD_COLOR))


threads = [threading.Thread(target=x)
           for x in [send_input, receive_footage]]
for thread in threads:
    thread.start()
