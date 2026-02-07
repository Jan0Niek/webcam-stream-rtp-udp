import RPi.GPIO as GPIO
import time
import serial
import threading
import socket
import cv2

running = True
#       lv  la  rv  ra
PINS = [27, 17, 22, 23]
counters = [0, 0, 0, 0]
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
        buffer, _ = sock.recvfrom(1)
        buffer = buffer.decode()
        if buffer == "q":
            running = False
            return
        if len(buffer) < 3:
            print(f"buffer te kort: {buffer}")
            return
        index = 0 if buffer[0] == "l" else 2
        index += 1 if buffer[1] == "b" else 0
        stop = buffer[2] == "s"
        GPIO.output(PINS[index],
                    GPIO.LOW if stop else GPIO.HIGH)
        counters[i] = 0 if stop else 1.1  # TODO: check of dit allemaal klopt


def check_batery():
    """leest usb en sluit computer af als de accu bijna leeg is"""
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.reset_input_buffer()
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            print(line)  # TODO: dit moet nog daadwerkelijk de pi uitzetten


threads = [threading.Thread(target=x)
           for x in [send_cam, receiver, check_batery]]
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
    for i in range(len(counters)):
        if counters[i] > 0:
            counters[i] -= dt
            if counters[i] < 0:
                GPIO.output(PINS[i], GPIO.LOW)  # TODO: hier ook effe checken
