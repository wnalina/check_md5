import io
import socket
import cv2
from flask import Flask, render_template, Response

server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 8000))
server_socket.listen(0)

cam = cv2.VideoCapture(0)
cam.set(3,640)
cam.set(4,480)

connection = server_socket.accept()[0].makefile('wb')
print("Connecting")

try:
    stream = io.BytesIO()
    camera.capture(stream, 'jpeg')
    stream.seek(0)
    connection.write(stream.read())
    stream.seek(0)
    stream.truncate()

finally:
    connection.close()
    server_socket.close()
    camera.stop_preview()
    print("Connection closed")