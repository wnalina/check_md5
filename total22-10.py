##--------------Azure---------------
import cognitive_face as CF
import time
import sys
from termcolor import colored, cprint
import os, os.path

##--------------OpenCV---------------
import cv2
from threading import Thread
from time import sleep
import datetime

##-----------------------------------------Azure----------------------------------------------
listPerson = [['gene', 'd30f428e-0a15-4eb5-9f07-d5886dd5a574'],
        ['ice', 'f29d819f-8b24-4bb6-bd17-055bc64ed32c'],
        ['oil', '41f3c76d-5bee-418b-8f65-5233b3521789'],
        ['sprite', '7f96cced-fe6c-4ed4-8332-33a0c36f6aeb'],
        ['golf', '506ec04e-8a43-4e44-9843-2a411ab36146']]

SUBSCRIPTION_KEY = 'db816427ef814612975b8cb5479d3c8c'
BASE_URL = 'https://southeastasia.api.cognitive.microsoft.com/face/v1.0'
CF.BaseUrl.set(BASE_URL)
CF.Key.set(SUBSCRIPTION_KEY)

TIME_SLEEP = 5
text = '--------------------'

##-------------------------------------OpenCV----------------------------------------------------
name = [0]
countName = 0
filename = None

# -----------------------------------Create group-----------------------------------
def createGroup() :
    groupName = input("Enter Group Name: ")
    #must be lowercase
    groupId = input("Enter Group Id (must be lowercase): ")
    CF.person_group.create(groupId, groupName)
    cprint('Success!', 'green')
    print(text)

# -----------------------------------List group-----------------------------------
def listGroups() :
    global personGroups
    groups = CF.person_group.lists()
    # time.sleep(TIME_SLEEP)
    print('Total Group List: '+str(len(groups)))
    i = 1
    for group in groups:
        groupId = group['personGroupId']
        groupName = group['name']
        #CF.person_group.delete(person_group_id)
        print('\t{}'.format(i), end=' ')
        print('ID: '+'{}'.format(groupId)+' ,NAME: {}'.format(groupName))
        i += 1
        # time.sleep(TIME_SLEEP)
    print(text)

# # ---------------------------------Create person in group list----------------------------------
def createPerson():
    personName = input("Enter Person Name: ")
    groupId = input("Enter Group Id (must be lowercase): ")
    # print('Select Group Id: ')
    # groups = CF.person_group.lists()
    # for group in groups:
    #     groupId = group['personGroupId']
    #     groupName = group['name']
    #     print('\t{}'.format(i), end=' ')
    #     print('ID: ' + '{}'.format(groupId) + ' ,NAME: {}'.format(groupName))
    res = CF.person.create(groupId, personName)
    if res :
        personId = res['personId']
        cprint('\tSuccess!', 'green')
        print('\tPerson Id: {}'.format(personId))
    print(text)

# # # ------------------------------------List person id in group------------------------------------
def listPersonInGroup():
    groupId = input("Enter Group Id (must be lowercase): ")
    person_lists = CF.person.lists(groupId)
    # time.sleep(TIME_SLEEP)
    print('Person List: '+str(len(person_lists)))
    i = 1
    for person in person_lists:
        name = person['name']
        cprint(name, "red")
        print('\t{}'.format(i), end=' ')
        print('{}'.format(person))
        i += 1
        # time.sleep(TIME_SLEEP)
    print(text)

# # ---------------------------------Add face person in group----------------------------------
def addFacePerson():
    groupId = input("Enter Group Id (must be lowercase): ")
    personId = input("Enter Person Id: ")
    folderName  =  input("Enter Folder Name: ")
    path = "D:/img/" + groupId + '/' + folderName + '/'
    lists = os.listdir(path)  # dir is your directory path
    # print(path)
    # print(list)
    number_files = len(lists)
    print(number_files)
    for list in lists:
        fileName = path + list
        print(fileName)
        CF.person.add_face(fileName, groupId, personId)
        CF.person_group.train(groupId)
        response = CF.person_group.get_status(groupId)
        status = response['status']
        cprint(status, 'green')


# # ---------------------------------Delete group----------------------------------
def deleteGroup():
    groupId = input("Enter Group Id (must be lowercase): ")
    CF.person_group.delete(groupId)
    cprint('Success!', 'green')
    print(text)

# # ---------------------------------Delete person in group----------------------------------
def deletePerson():
    groupId = input("Enter Group Id (must be lowercase): ")
    personId = input("Enter Person Id: ")
    CF.person.delete(groupId, personId)
    cprint('Success!', 'green')
    print(text)

# # ---------------------------------Detection and identify----------------------------------
def detection(photoPath):
    global listPerson
    global name
    # groupId = input("Enter Group Id (must be lowercase): ")
    detection = CF.face.detect(photoPath)
    # print(response)
    face_ids = [d['faceId'] for d in detection]
    # print('Face Id'+'{}'.format(face_ids))
    identified_faces = CF.face.identify(face_ids, 'myteams')
    # print(identified_faces)
    for identified_face in identified_faces:
         cprint(identified_face, "blue")
         candidates = identified_face['candidates']
         # print(candidates)

         if candidates:
             # cprint(candidates, "green")
             personId = identified_face['candidates'][0]['personId']
             confidence = identified_face['candidates'][0]['confidence']
             print('\tId: ', end='')
             cprint(personId, 'green')
             print('\tConfidence: ', end='')
             cprint(confidence, 'green')

             person_lists = listPerson
             range = len(person_lists)
             # print(range)
             i = 0
             while i < range:
                 id = person_lists[i][1]
                 if personId == id:
                     name = person_lists[i][0]
                     print('\tName: ', end='')
                     cprint(name, 'green')

                 i += 1
         else:
             cprint("\tnot found", "red")
    return (name)
    # for t in candidates :
    #     i = [d['confidence'] for d in t]
    #     print('Confidence: '+'{}'.format(i))


# #------------------------------------OpenCV--------------------------------------------
def openCamera():
    MAX_FRAME_COUNT = 3

    imgCount = 0
    frameCount = 0

    width = 640
    height = 480

    cap = cv2.VideoCapture(0)
    cap.set(3, width)  # set Width
    cap.set(4, height)  # set Height

    frameCount = MAX_FRAME_COUNT
    frameArr = [None] * MAX_FRAME_COUNT
    faceFoundArr = [None] * MAX_FRAME_COUNT
    lastFrame = 0

    # Get user supplied values
    # cascPath = "C:\opencv343\opencv\sources\data\haarcascades_cuda\haarcascade_frontalface_default.xml"
    cascPath = "C:\opencv-master\data\haarcascades_cuda\haarcascade_frontalface_default.xml"

    # Create the haar cascade
    faceCascade = cv2.CascadeClassifier(cascPath)
    font = cv2.FONT_HERSHEY_SIMPLEX
    global name

    class FindFaceThread(Thread):
        global faces
        global checker
        global imgCount

        global left
        global top
        global bottom
        global right
        global name
        global identified_faces
        def __init__(self):
            Thread.__init__(self)
            self.daemon = True
            self.start()

        def run(self):
            global name
            countAzure = 0

            lastFaceFound = 0
            faceFound = 0
            while True:
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
                        filename = "D:/image/img.jpg"
                        cv2.imwrite(filename, frame)
                        # detected = CF.face.detect(filename)
                        detection(filename)
                        countAzure += 1


                        # cprint(name, 'green')
                        print("countAzure: ", end="")
                        print(countAzure)
                        print(text)

                        # for face in detected:
                        #     rect = face['faceRectangle']
                        #     left = rect['left']
                        #     top = rect['top']
                        #     bottom = left + rect['height']
                        #     right = top + rect['width']
                        #     # print(face)

    FindFaceThread()

    while (True):

        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        frameCount -= 1
        if (frameCount == -1):
            if (faceFoundArr[0] == faceFoundArr[1] and faceFoundArr[0] == faceFoundArr[2]):
                found = faceFoundArr[0]
                if lastFrame != found:
                    lastFrame = found
                    if found == 0:
                        cprint('Face not found', 'red')
                        print(text)
                        name = None
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
            rectangle = str(x) + ', ' + str(y) +  ', ' + str(w) +  ', ' + str(h)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # cv2.putText(frame, name[0], (x, y-10), font, 1, (255, 255, 255), 2)
            # cv2.putText(frame, rectangle, (x, y+h+25), font, 1, (255, 255, 255), 2)

        cv2.imshow('frame', frame)
        # cprint(name, 'blue')

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

# # ---------------------------------List Function----------------------------------
def listFunction():
    lists = ["Create Group",
             "List Group",
             "Create Person",
             "List Person In Group",
             "Add Face Person In Group",
             "Delete Group",
             "Delete Person In Group",
             "Detection",
             "Open Camera",
             "List Function"]
    i = 1
    cprint('List Function', 'blue')
    for l in lists:
        cprint('\t{} '.format(i) + '{}'.format(l), 'red')
        # print(colored(i, 'red'), end=' ')
        # print(list)
        i += 1
    cprint(text, 'white')



# #-------------------------------------main program---------------------------------------------
listFunction()
# print(list[0])
while (True):
    ##-------------------------------------------Azure-------------------------------------------
    select = int(input('Select function: '))
    # select = int(input(print(colored('Select function: ', 'blue'), end=' ')))
    # text = colored('Hello, World!', 'red', attrs=['reverse', 'blink'])
    # print(text)
    # print(select)
    try:
        if select == 1:
            createGroup()
        elif select == 2:
            listGroups()
        elif select == 3:
            createPerson()
        elif select == 4:
            listPersonInGroup()
        elif select == 5:
            addFacePerson()
        elif select == 6:
            deleteGroup()
        elif select == 7:
            deletePerson()
        elif select == 8:
            # detection()
            print("not available")
        elif select == 9:
            openCamera()
        elif select == 10:
            listFunction()
    except:
        print('This function does not exist. Please try again.')
        print(text)

