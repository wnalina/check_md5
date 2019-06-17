# PI
import socket
import cv2
import struct ## new
import pickle
from threading import Thread
from time import sleep
from subprocess import check_output

FRAME_BUFF = None
RET = None
cam = cv2.VideoCapture(0)

functions = [{'describe': 'Azure Camera', 'function_name': 'azure_camera'},
             {'describe': 'Server', 'function_name': 'server_program'}]
class myThread(Thread):
    def __init__(self, func_name):
        Thread.__init__(self)
        # self.thread_id = thread_id
        self.function = func_name

    def run(self):
        print("Starting " + self.name)
        self.function()
        print("Exiting " + self.name)

# class multiSocket(Thread):
#     def __init__(self, c, func_name):
#         Thread.__init__(self)
#         # self.thread_id = thread_id
#         self
#         self.function = func_name
#
#     def run(self):
#         print("Starting " + self.name)
#         self.function()
#         print("Exiting " + self.name)

def camera_reader():
    global FRAME_BUFF
    global cam
    # global RET
    # global cam
    # cam = cv2.VideoCapture(0)

    cam.set(3, 640)
    cam.set(4, 480)

    while True:
        FRAME_BUFF = cam.read()
        # FRAME_BUFF = frame

def my_imshow():
    global FRAME_BUFF
    global cam
    # cam.set(3, 640)
    # cam.set(4, 480)

    while True:
        if not FRAME_BUFF == None:
            ret, frame = FRAME_BUFF
            # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cam.release()
                cv2.destroyAllWindows()
                break


def server_program():
    global FRAME_BUFF
    global cam
    # cam = cv2.VideoCapture(0)
    #
    # cam.set(3, 640)
    # cam.set(4, 480)

    # img_counter = 0
    # encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    # ip = socket.gethostname()
    ip = check_output(['hostname', '-I'])
    HOST = ip.decode("utf-8")
    # HOST = socket.gethostname()
    PORT = 5000

    ## socket_code
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Socket created')

    server_socket.bind((HOST, PORT))
    print('Socket bind complete')
    server_socket.listen(2)
    print('Socket now listening')



    while True:
        conn, address = server_socket.accept()
        print('Connection from : ' + str(address))
        # print('Connection from : ' + str(conn.getsockname()))
        Thread(target=multi_client, args=(conn,address)).start()
        # while True:
        #     if not FRAME_BUFF == None:
        #         ret, frame = FRAME_BUFF
        #         result, frame = cv2.imencode('.jpg', frame, encode_param)
        #         #    data = zlib.compress(pickle.dumps(frame, 0))
        #         data = pickle.dumps(frame, 0)
        #         size = len(data)
        #
        #         # print("{}: {}".format(img_counter, size))
        #         try:
        #             conn.sendall(struct.pack(">L", size) + data)
        #         except:
        #             print("Socket is dead or Client closeed connection")
        #
        #             conn.close()  # close the connection
        #             print("conn.close():\tOK")
        #
        #             # cam.release()
        #             # print("cam.release():\tOK")
        #             #
        #             # cv2.destroyAllWindows()
        #             # print("cv2.destroyAllWindows():\tOK")
        #
        #             print("waiting for new client")
        #
        #             ## hard_code
        #             # server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #             # print('Socket created')
        #             #
        #             # server_socket.bind((HOST, PORT))
        #             # print('Socket bind complete')
        #             # server_socket.listen(2)
        #             # print('Socket now listening')
        #
        #             # cam = cv2.VideoCapture(0)
        #             #
        #             # cam.set(3, 640)
        #             # cam.set(4, 480)
        #
        #             # img_counter = 0
        #             # encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
        #             break
                # img_counter += 1

            # data = conn.recv(1024).decode()
            # if not data:
            #     # if data is not received break
            #     print("client send close request")
            #     break

def multi_client(conn, addr):
    global FRAME_BUFF
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    while True:
        if not FRAME_BUFF == None:
            ret, frame = FRAME_BUFF
            result, frame = cv2.imencode('.jpg', frame, encode_param)
            #    data = zlib.compress(pickle.dumps(frame, 0))
            data = pickle.dumps(frame, 0)
            size = len(data)

            # print("{}: {}".format(img_counter, size))
            try:
                conn.sendall(struct.pack(">L", size) + data)
            except:
                print("Socket is dead or Client closed connection from : " + str(addr))

                conn.close()  # close the connection
                print("conn.close():\tOK")

                # cam.release()
                # print("cam.release():\tOK")
                #
                # cv2.destroyAllWindows()
                # print("cv2.destroyAllWindows():\tOK")

                print("waiting for new client")

                break

if __name__ == '__main__':
    # server_program()
    # camera_reader = myThread(camera_reader)
    # camera_reader.start()
    #
    # my_imshow = myThread(my_imshow)
    # # my_imshow.start()
    #
    # server_program = myThread(server_program)
    # server_program.start()

    camera_reader = Thread(target=camera_reader, args=())
    camera_reader.start()

    my_imshow = Thread(target=my_imshow, args=())
    # my_imshow.start()

    server_program = Thread(target=server_program, args=())
    server_program.start()