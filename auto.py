import RPi.GPIO as GPIO
import time
import serial
import threading
import socket
import cv2

running = True
#       lv  la  rv  ra
PINS = [27, 17, 22, 23]
counters = [0.0] * 4
port = 5000

for pin in PINS:
    GPIO.setup(pin, GPIO.OUT)
sock: socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind("0.0.0.0", port)
_, addr = sock.recvfrom(100)


def send_cam():
    """verstuurt camerabeelden naar de client"""
    global running
    cap = cv2.VideoCapture(0)
    while running:
        _, frame = cap.read()
        _, buffer = cv2.imencode(".webp", frame,
                                 (cv2.IMWRITE_WEBP_QUALITY, 70))
        buffer = buffer.tobytes()
        sock.sendto(buffer, addr)


def receiver():
    """ontvangt alle requests en zet counter en GPIO voor de wielen"""
    global running, counters
    while running:
        buffer, _ = sock.recvfrom(1)  # we hebben maar 1 byte nodig
        buffer = int.from_bytes(buffer)
        if (buffer << 5) & 1 == 1:
            running = False
            return

        for i in range(4):  # 4, ofwel len(counter)
            is_on = (buffer >> i) & 1 == 1  # checkt of de bit bij i 1 is
            if is_on and counters[i] <= 0:
                GPIO.output(PINS[i], GPIO.HIGH)
            elif not is_on and counters[i] > 0:
                GPIO.output(PINS[i], GPIO.LOW)
            counters[i] = 1.1 if is_on else 0


def check_batery():
    """leest usb en sluit computer af als de accu bijna leeg is"""
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.reset_input_buffer()
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            print(line)  # TODO: dit moet nog daadwerkelijk de pi uitzetten


threads = [threading.Thread(target=f)
           for f in [send_cam, receiver, check_batery]]
for thread in threads:
    thread.start()

# vanaf hier de main thread:
# hier worden counters geteld en wielen uitgezet na genoeg tijd

lEFT_FORWARD = 27
LEFT_BACKWARD = 17
RIGHT_FORWARD = 22
RIGHT_BACKWARD = 23

then = time.time()
now = then
dt = 0
while True:
    now = time.time()
    dt = now - then
    then = now
    for i in range(4):  # 4, ofwel len(counters)
        if counters[i] > 0:
            counters[i] -= dt
            if counters[i] < 0:
                GPIO.output(PINS[i], GPIO.LOW)  # TODO: hier ook effe checken
