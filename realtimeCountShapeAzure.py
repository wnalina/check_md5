import datetime
from threading import Thread
import cognitive_face as CF
from time import sleep
from termcolor import colored, cprint

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

found = 0
lastFrame = 0

# Get user supplied values
# cascPath = "C:\opencv343\opencv\sources\data\haarcascades_cuda\haarcascade_frontalface_default.xml"
cascPath = "C:\opencv-master\data\haarcascades_cuda\haarcascade_frontalface_default.xml"


# Create the haar cascade
faceCascade = cv2.CascadeClassifier(cascPath)




class FindFaceThread(Thread):
    global faces
    global checker
    global imgCount

    global left
    global top
    global bottom
    global right


    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.start()

    def run(self):
        countAzure = 0

        lastFaceFound = 0
        faceFound = 0
        while True :
            sleep(1)

            # print(faces.shape)
            faceFound = found

            if faceFound != lastFaceFound:
                if faceFound == 0:
                    lastFaceFound = faceFound
                else:
                    now = datetime.datetime.now().strftime("%H:%M:%S")
                    lastFaceFound = faceFound

                    print(now + " Face Found: ", end="")
                    print(faceFound)

                    # imgCount = imgCount + 1
                    filename = "D:/img/img.jpg"
                    cv2.imwrite(filename, frame)
                    detected = CF.face.detect(filename)
                    countAzure += 1
                    print(detected)
                    print("countAzure: ", end="")
                    print(countAzure)

                    # for face in detected:
                    #     rect = face['faceRectangle']
                    #     left = rect['left']
                    #     top = rect['top']
                    #     bottom = left + rect['height']
                    #     right = top + rect['width']
                        # print(face)



FindFaceThread()

cap = cv2.VideoCapture(0)
cap.set(3,640) # set Width
cap.set(4,480) # set Height

KEY = "db816427ef814612975b8cb5479d3c8c"
CF.Key.set(KEY)
BASE_URL = 'https://southeastasia.api.cognitive.microsoft.com/face/v1.0'
CF.BaseUrl.set(BASE_URL)

while(True):

    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    frameCount -= 1
    if(frameCount == -1):
        if(faceFoundArr[0] == faceFoundArr[1] and faceFoundArr[0] == faceFoundArr[2]):
            found=faceFoundArr[0]
            if lastFrame != found:
                lastFrame = found
                if found == 0:
                    cprint('Face not found', 'red')
                # else:
                    # print("0: ", end="")
                    # print(faceFoundArr[0])
                    # print("1: ", end="")
                    # print(faceFoundArr[1])
                    # print("2: ", end="")
                    # print(faceFoundArr[2])
                    # print("found: ", end="")
                    # print(found)
        frameCount = MAX_FRAME_COUNT - 1
    frameArr[frameCount] = frame

    faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=0
    )

    try:
        faceFoundArr[frameCount] = faces.shape[0]
    except:
        faceFoundArr[frameCount] = 0
        # print('Face not found.')
    # print(frameCount)
    # print("Face Found" ": ", end="")
    # print(faceFoundArr[frameCount])



    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
