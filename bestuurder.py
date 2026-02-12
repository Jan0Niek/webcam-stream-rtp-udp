import numpy as np
import time
import socket
import keyboard
import threading
import cv2

port = 5000
batPort = port + 1  # zelfde comment als in auto.py zeg maar

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
addr = (socket.gethostbyname('autootje'), port)
batAdrr = ("0.0.0.0", batPort)
# addr = ("127.0.0.1", port)
print(addr)

sock.sendto("zinloze data".encode(), addr)

batSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
batSock.bind(batAdrr)

running = True
batPercentage = 999999


def send_input():
    """verstuurt de inputs als 4 (+ 1) bits in één byte naar de auto"""
    # TODO: verstuur ook (in aparte functie) de (PWM-dutycycle)snelheid waarmee je PER WIEL de snelheid bepalen kan
    inputs = 0
    while running:
        inputs = sum(1 << i for i, keyBtn in enumerate("qaed")
                     if keyboard.is_pressed(keyBtn))
        buffer = inputs.to_bytes()
        sock.sendto(buffer, addr)
        time.sleep(0.05)  # geloof het of niet, dit maakt het sneller
    sock.sendto((1 << 5).to_bytes(), addr)  # stuurt de quit-bit
    sock.close()
    print('programma is gestopt')


def receive_footage():
    """ontvangt camerabeelden en pleurt ze in een cv2 display window ter weergave"""
    global running
    while cv2.waitKey(1) != ord('l'):
        buffer, _ = sock.recvfrom(65540)
        # buffer = buffer.decode()
        frame = np.frombuffer(buffer, dtype=np.uint8)
        frame = frame.reshape(frame.shape[0], 1)
        cv2.imshow("gaming", cv2.imdecode(frame, cv2.IMREAD_COLOR))
    running = False
    cv2.destroyAllWindows()


# TODO: maak aparte functie (op aparte socketverbinding en -poort?) die accupercentage ontvangt
def receive_batPercentage():
    global batPercentage
    while running:
        buffer, _ = batSock.recvfrom(1024)
        batPercentage = int.from_bytes(buffer)
        print(batPercentage, end="\r")


threads = [threading.Thread(target=x)
           for x in [send_input, receive_footage, receive_batPercentage]]
for thread in threads:
    thread.start()

print('programma is gestart')

for thread in threads:
    thread.join()
