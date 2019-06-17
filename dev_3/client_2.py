import cv2
import io
import socket
import struct
import time
import pickle
import zlib


def client_program():
    host = socket.gethostname()  # as both code is running on same pc
    port = 5000  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    # message = input(" -> ")  # take input
    data = b""
    payload_size = struct.calcsize(">L")
    # print("payload_size: {}".format(payload_size))
    # if client_socket.recv(4096):
    #     print('Recive from server')
    while True:
        client_socket.send('hi'.encode())
        while len(data) < payload_size:
            # print("Recv: {}".format(len(data)))
            data += client_socket.recv(4096)

        # print("Done Recv: {}".format(len(data)))
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack(">L", packed_msg_size)[0]
        # print("msg_size: {}".format(msg_size))

        while len(data) < msg_size:
            data += client_socket.recv(4096)
        frame_data = data[:msg_size]
        data = data[msg_size:]

        frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
        frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
        cv2.imshow('ImageWindow', frame)
        cv2.waitKey(1)
    client_socket.close()


if __name__ == '__main__':
    client_program()