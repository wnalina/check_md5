import socket
from threading import *
import cv2
import numpy


cap = cv2.VideoCapture(0)

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = IPAddr
port = 5000
print (host)
print (port)
serversocket.bind((host, port))

class client(Thread):
    global  frame
    def __init__(self, socket, address):
        Thread.__init__(self)
        self.sock = socket
        self.addr = address
        self.start()

    def run(self):
        while True:
            print('Client sent:', self.sock.recv(1024).decode())
            # self.sock.send(b'Oi you sent something to me')
            self.sock.send(frame)

serversocket.listen(5)
print ('server started and listening')
while True:
    ret, frame = cap.read()
    # cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break
    clientsocket, address = serversocket.accept()
    client(clientsocket, address)

