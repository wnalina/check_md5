from http.server import BaseHTTPRequestHandler,HTTPServer
import cv2
import base64

def send_a_frame():
    capture = cv2.VideoCapture(0)
    frame = capture.read()[1]
    cnt = cv2.imencode('.png',frame)[1]
    b64 = base64.encodestring(cnt)
    html = "<html><img src='data:image/png;base64,"+b64 +"'></html"
    send(html)