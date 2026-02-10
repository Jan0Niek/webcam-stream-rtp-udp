import socket
import keyboard
import threading
import cv2

port = 5000
batPort = port + 1 #zelfde comment als in auto.py zeg maar

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
addr = socket.gethostbyname('autootje')

sock.bind((addr, port))
sock.sendto("zinloze data".encode(), addr)

batSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
batSock.bind((addr, batPort))

running = True

def send_input():
    """verstuurt de inputs als 4 bits in één byte naar de auto"""
    # TODO: verstuur ook (in aparte functie) de (PWM-dutycycle)snelheid waarmee je PER WIEL de snelheid bepalen kan 
    inputs = 0
    while running:
        inputs = sum(1 << i for i, keyBtn in enumerate("qaed")
                     if keyboard.is_pressed(keyBtn))
        buffer = inputs.to_bytes()
        sock.sendto(buffer, addr)
    print('programma is gestopt')


def receive_footage():
    """ontvangt camerabeelden en pleurt ze in een cv2 display window ter weergave"""
    global running
    while cv2.waitKey(1) != ord('l'):
        buffer, _ = sock.recvfrom(1024)
        buffer = buffer.decode()
        cv2.imshow(str(batPercentage), cv2.imdecode(buffer, cv2.IMREAD_COLOR))
    sock.sendto(b'\x10', addr) # stuurt de quit-bit
    sock.close()
    running = False

# TODO: maak aparte functie (op aparte socketverbinding en -poort?) die accupercentage ontvangt
def receive_batPercentage():
    global batPercentage
    while running:
        buffer, _ = batSock.recvfrom(1024)
        batPercentage = buffer.decode()



threads = [threading.Thread(target=x)
           for x in [send_input, receive_footage, receive_batPercentage]]
for thread in threads:
    thread.start()

print('programma is gestart')