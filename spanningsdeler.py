import serial
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
ser.reset_input_buffer()
time.sleep(10)  # conserve a little power maybe?
while running:
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').rstrip()
        print(line)  # moet eigenlijk weg, gaat dan sneller
# onzin