import cv2
import cognitive_face as CF
import numpy as np
from PIL import Image
from termcolor import colored, cprint
import os, os.path
from threading import Thread
import threading
import time
from time import sleep
from threading import Timer,Thread,Event

cascPath = "C:\opencv-master\data\haarcascades_cuda\haarcascade_frontalface_default.xml"

faceCascade = cv2.CascadeClassifier(cascPath)
font = cv2.FONT_HERSHEY_SIMPLEX
SUBSCRIPTION_KEY = 'db816427ef814612975b8cb5479d3c8c'
BASE_URL = 'https://southeastasia.api.cognitive.microsoft.com/face/v1.0'
CF.BaseUrl.set(BASE_URL)
CF.Key.set(SUBSCRIPTION_KEY)


i = 0
azure_call = False
# for (x, y, w, h) in faces:
#     cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
#     crop_img = img[y:y + h, x:x + w]
#     file = "D:/image/run/img"+str(i)+".jpg"
#     i += 1
#     cv2.imwrite(file, crop_img)
#     # cv2.imshow("cropped", crop_img)
#     print(x, y)
def verify():
    img = cv2.imread('D:/image/geneGolf.jpg')
    # detection = CF.face.detect('D:/img/myteams/oil/2.jpg')
    # print(detection)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=0
    )
    path = "D:/image/run/"
    lists = os.listdir(path)
    number_files = len(lists)
    images_list = []
    for list in lists:
        fileName = path + list
        images_list.append(fileName)
    print(images_list)

    # images_list = ['D:/image/run/img11.jpg', 'D:/image/run/img12.jpg']
    imgs = [Image.open(i) for i in images_list] #open img
    min_img_shape = sorted([(np.sum(i.size), i.size ) for i in imgs])[0][1] #find minsize
    img_merge = np.hstack((np.asarray(i.resize(min_img_shape, Image.ANTIALIAS)) for i in imgs)) #  resize
    img_merge = Image.fromarray(img_merge) #merge
    img_merge.save('D:/image/run/terracegarden_h.jpg') #save

    response = CF.face.detect('D:/image/geneGolf.jpg')
    test = CF.face.detect('D:/image/geneGolf.jpg')
    # test_faceId = test[0]['faceId']
    test_faceId = [d['faceId'] for d in test]
    print(test_faceId)
    # print(response)
    face_ids = [d['faceId'] for d in response]
    # print('Face Id'+'{}'.format(face_ids))
    print(face_ids)
    for id in test_faceId:
        for f in face_ids:
            r = CF.face.verify(f, id)
            print(id+'  '+f, end='')
            cprint(r, 'red')
            if r['isIdentical']:
                face_ids.remove(f)
                break


    # cv2.imshow('image', vis)
    # cv2.imshow('image', img)
    # cv2.waitKey(0)
    cv2.destroyAllWindows()
class waiter(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.start()
    # def run(self):
    #     global i
        if i == 2:
            i=0
            print('sleep')
            sleep(10000)

class perpetualTimer():
   global i

   def __init__(self,t,hFunction):
      self.t=t
      self.hFunction = hFunction
      self.thread = Timer(self.t,self.handle_function)

   def handle_function(self):
      self.hFunction()
      self.thread = Timer(self.t,self.handle_function)
      self.thread.start()

   def start(self):
       self.thread.start()


   def cancel(self):
      self.thread.cancel()

def printer():
    global i
    print('ipsem lorem')
    i += 1
    print(i)
    if i == 3:
        i = 0
        sleep(60)

t = perpetualTimer(1,printer)
t.start()
# t.cancel()

def time():
    global i
    # j = 0
    threading.Timer(1.0, time).start()
    test = CF.face.detect('D:/image/gene2.jpg')
    print(test)
    # print("Hello, World!")
    i += 1
    print(i)
    # if i == 2:
    #     i = 0
    #     print('sleep')
    #     sleep(10000)
    # waiter()
    # if i == 3:
    #     print('Sleeping')
    #     time.sleep(60)


class azure_Thread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.start()
    def run(self):
        global frame
        global frame
        global person_list
        global azure_call
        group_id = 'myteams'
        c = 0
        count_person = []

        while True:
            if azure_call:
                azure_call = False

                file = "D:/image/img.jpg"
                img = file

                azureDetect = CF.face.detect(img)
                face_ids = [d['faceId'] for d in azureDetect]
                azureFound = len(face_ids)

                print("azureFound: " + str(azureFound))


                if azureFound >= 1:
                    azure_identified_faces = CF.face.identify(face_ids, group_id)

                    found = azureFound
                    for count in range(azureFound):
                        candidate = azure_identified_faces[count]['candidates']
                        if not candidate:  # check empty list
                            cprint('\tname: unknown', 'red')
                            found -= 1
                        else:
                            candidate_personId = candidate[0]['personId']
                            candidate_confidence = candidate[0]['confidence']

                            for person in person_list:
                                if candidate_personId == person['personId']:
                                    cprint('\tname: ' + person['personName'] + ', with confidence: ' + str(
                                        candidate_confidence), 'green')
                                    found -= 1
                                    # count_person = 'oil'
                                    count_person.append(person['personName'])
                                    # print('couunt_person: ' + count_person)
                                    c += 1
                            for x in count_person:
                                print(x)

                    for k in range(found):
                        cprint('\tname: unknown', 'red')
            else:
                sleep(1)

def azure_camera():
    print("Starting...")
    azure_Thread()

    MAX_CHECK_FRAME = 3
    width = 640
    height = 480
    allArrLastFound = 0
    currentFound = 0

    cap = cv2.VideoCapture(0)
    cap.set(3, width)  # set Width
    cap.set(4, height)  # set Height

    # Get user supplied values
    # cascPath = "C:\opencv343\opencv\sources\data\haarcascades_cuda\haarcascade_frontalface_default.xml"
    cascPath = "C:\opencv-master\data\haarcascades_cuda\haarcascade_frontalface_default.xml"

    # Create the haar cascade
    faceCascade = cv2.CascadeClassifier(cascPath)

    cap = cv2.VideoCapture(0)

    frameCount = -1
    frameArr = [None] * MAX_CHECK_FRAME
    faceFoundArr = [None] * MAX_CHECK_FRAME
    confirmFound = 0
    allArrLastFound = 0

    global person_list
    global azure_call

    while (True):
        # sleep(0.3)
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        frameArr[frameCount] = gray
        frameCount += 1
        if frameCount == 3:
            frameCount = 0

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(80, 80),
            flags=0
        )

        if hasattr(faces, 'shape'):
            currentFound = faces.shape[0]
        else:
            currentFound = 0

        faceFoundArr[frameCount] = currentFound

        if len(set(faceFoundArr)) <= 1:
            confirmFound = faceFoundArr[0]
            # print(str(faceFoundArr) + " => " + str(all(faceFoundArr)))

            if confirmFound != allArrLastFound:
                allArrLastFound = confirmFound

                if(allArrLastFound == 0):
                    print()
                # else:
                    # print("casFound: " + str(allArrLastFound), end="\t")


                if int(allArrLastFound) >= 1:
                    print('Checking...')
                    file = "D:/image/img.jpg"
                    cv2.imwrite(file, frame)
                    img = file
                    azure_call = True

                    # azureDetect = CF.face.detect(img)
                    # face_ids = [d['faceId'] for d in azureDetect]
                    # azureFound = len(face_ids)

                    # print("azureFound: " + str(azureFound))

                    # if azureFound >= 1:
                    #     azure_identified_faces = CF.face.identify(face_ids, group_id)
                    #
                    #     found = azureFound
                    #     for count in range(azureFound):
                    #         candidate = azure_identified_faces[count]['candidates']
                    #         if not candidate:  # check empty list
                    #             print('\tname: unknown')
                    #         else:
                    #             candidate_personId = candidate[0]['personId']
                    #             candidate_confidence = candidate[0]['confidence']
                    #
                    #             for person in person_list:
                    #                 if candidate_personId == person['personId']:
                    #                     print('\tname: ' + person['personName'] + ', with confidence: ' + str(
                    #                         candidate_confidence))
                    #                     found -= 1
                    #
                    #     for k in range(found):
                    #         print('\tname: unknown')

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            break
    # When everything done, release the capture
    return

# time()
# azure_camera()
verify()
exit(0)