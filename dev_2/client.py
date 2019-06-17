import cv2
import io
import socket
import struct
import time
import pickle
import zlib
from subprocess import check_output

# ip = check_output(['hostname', '-I'])
# ip_de = ip.decode("utf-8")
ip_de = '192.168.137.166'


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((ip_de, 8485))
connection = client_socket.makefile('wb')

while True:
    data = client_socket.recv(1024).decode()
    print(data)
# data = b""
# payload_size = struct.calcsize(">L")
# print("payload_size: {}".format(payload_size))
# while True:
#     while len(data) < payload_size:
#         print("Recv: {}".format(len(data)))
#         data += client_socket.recv(4096)
#
#     print("Done Recv: {}".format(len(data)))
#     packed_msg_size = data[:payload_size]
#     data = data[payload_size:]
#     msg_size = struct.unpack(">L", packed_msg_size)[0]
#     print("msg_size: {}".format(msg_size))
#     while len(data) < msg_size:
#         data += client_socket.recv(4096)
#     frame_data = data[:msg_size]
#     data = data[msg_size:]
#
#     frame=pickle.loads(frame_data, fix_imports=True, encoding="bytes")
#     frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
#     cv2.imshow('ImageWindow',frame)
#     cv2.waitKey(1)



# cam = cv2.VideoCapture(0)
#
# cam.set(3, 640)
# cam.set(4, 480)
#
# img_counter = 0
#
# encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
#
# while True:
#     ret, frame = cam.read()
#     result, frame = cv2.imencode('.jpg', frame, encode_param)
# #    data = zlib.compress(pickle.dumps(frame, 0))
#     data = pickle.dumps(frame, 0)
#     size = len(data)
#
#
#     print("{}: {}".format(img_counter, size))
#     client_socket.sendall(struct.pack(">L", size) + data)
#     img_counter += 1
#
# cam.release()