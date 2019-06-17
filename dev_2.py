import socket
import cv2

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = IPAddr
port =5000
s.connect((host,port))

def ts(str):
   s.send('e'.encode())
   data = ''
   data = s.recv(1024).decode()
   cv2.imshow('frame', data)
   print (data)

while 2:
   r = input('enter')
   ts(s)

s.close ()