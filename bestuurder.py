import socket
import keyboard
import threading
import cv2

port = 5000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
addr = socket.gethostbyname('autootje')

sock.bind((addr, port))
sock.sendto("zinloze data".encode(), addr)


def send_input():
    """verstuurt de inputs als 4 bits in één byte naar de auto"""
    # TODO: verstuur ook (in aparte functie) de (PWM-dutycycle)snelheid waarmee je PER WIEL de snelheid bepalen kan
    inputs = 0
    while True:
        inputs = sum(1 << i for i, keyBtn in enumerate("qaed")
                     if keyboard.is_pressed(keyBtn))
        buffer = inputs.to_bytes()
        sock.sendto(buffer, addr)


def receive_footage():
    """ontvangt camerabeelden en pleurt ze in een cv2 display window ter weergave"""
    while cv2.waitKey(1) != ord('l'):
        buffer, _ = sock.recvfrom(1024)
        buffer = buffer.decode()
        cv2.imshow("accuPercentage hier?", cv2.imdecode(buffer, cv2.IMREAD_COLOR))
    sock.sendto(b'\x10', addr) # stuurt de quit-bit

# TODO: maak aparte functie (op aparte socketverbinding en -poort?) die accupercentage ontvangt


threads = [threading.Thread(target=x)
           for x in [send_input, receive_footage]]
for thread in threads:
    thread.start()
