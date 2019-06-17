import socket
import sys
import cv2
import pickle
import numpy as np
import struct ## new
import zlib
from subprocess import check_output

# ip = check_output(['hostname', '-I'])
# ip_de = ip.decode("utf-8")

def server_program():
    # get the hostname
    host = socket.gethostname()
    print("hostname" + host)
    port = 5000  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together
    connection = server_socket.makefile('wb')
    cam = cv2.VideoCapture(0)

    cam.set(3, 640)
    cam.set(4, 480)

    img_counter = 0

    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]


    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    while(True):
        conn, address = server_socket.accept()  # accept new connection

        print("Connection from: " + str(address))

        # while conn:
        while True:
            try:

                ret, frame = cam.read()
                result, frame = cv2.imencode('.jpg', frame, encode_param)
                #    data = zlib.compress(pickle.dumps(frame, 0))
                data = pickle.dumps(frame, 0)
                size = len(data)

                # print("{}: {}".format(img_counter, size))
                conn.sendall(struct.pack(">L", size) + data)
                img_counter += 1
            except:
                break

        cam.release()

            # print("from connected user: " + str(data))
            # data = input(' -> ')
            # conn.send(data.encode())  # send data to the client


        # conn.close()  # close the connection


if __name__ == '__main__':
    server_program()