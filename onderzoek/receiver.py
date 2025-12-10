# import cv2
import socket
# import pickle
# import numpy as np
import time

host = "127.0.0.1"
port = 5000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

start = time.perf_counter()

sock.sendto("boem".encode(), (host, port))
data, addr = sock.recvfrom(1024)
print(data.decode())

end = time.perf_counter()

print(f"dat duurde {end-start} seconden")
