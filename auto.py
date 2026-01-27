import time as t
import socket

counter: int = 0
then: int = t.time()
t.sleep(1)
now: int
sock: socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


while counter < 1:
    now = t.time()
    counter += now - then
