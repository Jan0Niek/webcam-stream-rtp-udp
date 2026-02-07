import RPi.GPIO as GPIO
import time

pins = [11, 13, 15, 16]

GPIO.setmode(GPIO.BCM)

for pin in pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(0.3)
    GPIO.output(pin, GPIO.LOW)
    time.sleep(0.3)
