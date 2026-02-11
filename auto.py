import RPi.GPIO as GPIO
# import pigpio
import time
import serial
import threading
import socket
import cv2

running = True

# lv= linksvoorwaarts
# la= linksachterwaarts
# rv= rechtsvoorwaarts
# ra= rechtsachterwaarts
#       lv  la  rv  ra
PINS = [27, 17, 22, 23]  # gpio nummers, niet board nummers
counters = [0.0] * 4
port = 5000
batPort = port + 1  # vreselijk, 2 configurable ports is beter

# pi = pigpio.pi()
# pi.hardware_PWM(12, 2000, 750000)
# pi.hardware_PWM(13, 2000, 750000)

GPIO.setmode(GPIO.BCM)
for pin in PINS:
    GPIO.setup(PINS, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(pin, GPIO.LOW)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", port))
_, addr = sock.recvfrom(1024) # dit wacht dus net zolang tot het een signaal ontvangt (signaal kleiner dan 1024 bits)
print("dingen gaan starten")

batSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # nog een socketverbinding op een aparte port omdat wij niksnutten zijn haha

batAddr = list(addr)
batAddr[1] = batPort
batAddr = tuple(batAddr)

batSock.bind(batAddr)  # zou niet nodig moeten zijn


def send_cam():
    """verstuurt camerabeelden naar de client"""
    global sock
    cap = cv2.VideoCapture(0)
    while running:
        _, frame = cap.read()
        _, buffer = cv2.imencode(".webp", frame,
                                 (cv2.IMWRITE_WEBP_QUALITY, 70))
        buffer = buffer.tobytes()
        sock.sendto(buffer, addr)


def receiver():
    """ontvangt alle requests en zet counters en GPIO voor de wielen"""
    global running, counters
    while running:
        buffer, _ = sock.recvfrom(1)  # we hebben maar 1 byte nodig
        buffer = int.from_bytes(buffer)
        if (buffer >> 5) & 1 == 1:
            running = False
            time.sleep(1)
            sock.close()
            return

        for i in range(4):  # 4, ofwel len(counter)
            is_on = (buffer >> i) & 1 == 1  # checkt of de bit bij i 1 is
            if is_on and counters[i] <= 0:
                GPIO.output(PINS[i], GPIO.HIGH)
            elif not is_on and counters[i] > 0:
                GPIO.output(PINS[i], GPIO.LOW)
            counters[i] = 1.1 if is_on else 0


def check_battery():
    """leest usb en sluit computer af als de accu bijna leeg is EN VERSTUURT HET NU?!"""
    global running
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1) # the arduino is in USB0, not AMC0 sooo yeah
    ser.reset_input_buffer()
    while running:
        if ser.in_waiting > 0:
            line = ser.readline().rstrip()
            # print(line)  # moet eigenlijk weg, gaat dan sneller
            # batteryPercentage = line
            batSock.sendto(int(line).to_bytes(), batAddr) # send battery percentage to the controlling party waarom engels opeens huh?!
            if int(line) <= 5: # under 5% (~9,1V) it should stop (and perhaps shut the Pi down?)
                GPIO.cleanup(PINS)
                # pi.stop()
                running = False
                # call('poweroff')
                # call('shutdown now')


threads = [threading.Thread(target=f)
           for f in [send_cam, receiver, check_battery]]
for thread in threads:
    thread.start()

# vanaf hier de main thread:
# hier worden counters geteld en wielen uitgezet na genoeg tijd

# lEFT_FORWARD = 27
# LEFT_BACKWARD = 17
# RIGHT_FORWARD = 22
# RIGHT_BACKWARD = 23  # deze worden nooit gebruikt, misschien ooit verwijderen

then = time.time()
now = then
dt = 0
while running:
    now = time.time()
    dt = now - then
    then = now
    for i in range(4):  # 4, ofwel len(counters)
        if counters[i] > 0:
            counters[i] -= dt
            if counters[i] < 0:
                GPIO.output(PINS[i], GPIO.LOW)

for thread in threads:
    thread.join()

GPIO.cleanup(PINS)
# pi.stop()
