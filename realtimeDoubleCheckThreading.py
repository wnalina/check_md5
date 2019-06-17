import datetime
from threading import Thread
from time import sleep

import numpy as np
import cv2

MAX_FRAME_COUNT = 3

imgCount = 0
frameCount = 0

width = 640
height = 480

cap = cv2.VideoCapture(0)
cap.set(3, width)            # set Width
cap.set(4, height)           # set Height

frameCount = MAX_FRAME_COUNT
frameArr = [None] * MAX_FRAME_COUNT
faceFoundArr = [None] * MAX_FRAME_COUNT

# Get user supplied values
cascPath = "C:\opencv343\opencv\sources\data\haarcascades_cuda\haarcascade_frontalface_default.xml"

# Create the haar cascade
faceCascade = cv2.CascadeClassifier(cascPath)

class FindFaceThread(Thread):
    global faces
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.start()

    def run(self):
        # lastFaceFound = 0
        # while True:
        #     sleep(1)
        #     faceFound = 0
        #     equal = all(x == faceFoundArr[0] for x in faceFoundArr)
        #
        #     if equal:
        #         faceFound = faceFoundArr[0]
        #
        #     if faceFound != 0 and faceFound != lastFaceFound:
        #         now = datetime.datetime.now().strftime("%H:%M:%S")
        #         lastFaceFound = faceFound
        #
        #         print(now + " Face Found: ", end="")
        #         print(faceFound)
        #         print("NEED TO CALL AZURE")



            # equal = all(x == faceFoundArr[0] for x in faceFoundArr)
            # #print(equal)
            #
            # faceFound = faceFoundArr[0]
            # if not equal and faceFound and faceFound != lastFaceFound:
            #     now = datetime.datetime.now().strftime("%H:%M:%S")
            #     lastFaceFound = faceFound
            #
            #     print(now + " Face Found: ", end="")
            #     print(faceFound)





        lastFaceFound = 0
        faceFound = 0
        while True :
            sleep(1)

            # print(faces.shape)
            try:
                faceFound = faces.shape[0]
            except:
                print('Can not found face.')
                faceFound = 0

            if faceFound != lastFaceFound:
                if faceFound == 0:
                    lastFaceFound = faceFound
                else:
                    now = datetime.datetime.now().strftime("%H:%M:%S")
                    lastFaceFound = faceFound

                    print(now + " Face Found: ", end="")
                    print(faceFound)



FindFaceThread()
while(True):

    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # frameCount -= 1
    # if(frameCount == -1):
    #     frameCount = MAX_FRAME_COUNT - 1
    # frameArr[frameCount] = frame

    faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=0
    )

    # try:
    #     faceFoundArr[frameCount] = faces.shape[0]
    # except:
    #     print('Can not found.')
    # print(frameCount)



    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
