import cognitive_face as CF
from threading import Thread
from termcolor import colored, cprint
import os, os.path
import cv2
from time import sleep
# from PIL import Image, ImageDraw
import numpy as np
from flask import Flask, render_template, Response
import socket
from subprocess import check_output

cap = cv2.VideoCapture(0)
cascPath = "/home/pi/project/haarcascades_cuda/haarcascade_frontalface_default.xml"
video_flask = None

list = [['gene', 'c23fd3c5-ae04-4672-88a0-2927d34f32c0'],
        ['ice', '2d9111f8-0fa0-440b-af05-7a91ddc13e3f'],
        ['sprite', '2efc2b53-e2da-4276-a007-a1ed69ead0a6']]

functions = [{'describe': 'Open Camera', 'function_name': 'open_camera'},
             {'describe': 'Azure Camera', 'function_name': 'azure_camera'},
             {'describe': 'Create Group', 'function_name': 'createGroup'},
             {'describe': 'List Group', 'function_name': 'listGroups'},
             {'describe': 'Create Person', 'function_name': 'createPerson'},
             {'describe': 'List Person In Group', 'function_name': 'listPersonInGroup'},
             {'describe': 'Add Person In Group', 'function_name': 'addPersonInGroup'},
             {'describe': 'Delete Group', 'function_name': 'deleteGroup'},
             {'describe': 'Delete Person In Group', 'function_name': 'deletePerson'},
             {'describe': 'Detection', 'function_name': 'detection'},
             {'describe': 'List Function', 'function_name': 'listFunction'},
             {'describe': 'Verify', 'function_name': 'verify'},
             {'describe': 'Check Running', 'function_name': 'check_running'},
             {'describe': 'Start Preview On Browser', 'function_name': 'start_preview'},
             {'describe': 'Stop Preview On Browser', 'function_name': 'stop_preview'}]

SUBSCRIPTION_KEY = 'ce5f9a111c7a4a26b8fd0f88ab2fe47a'
BASE_URL = 'https://southeastasia.api.cognitive.microsoft.com/face/v1.0'
CF.BaseUrl.set(BASE_URL)
CF.Key.set(SUBSCRIPTION_KEY)

TIME_SLEEP = 5
text = '--------------------'

azure_call = False

class myThread(Thread):
    def __init__(self, thread_id, func_name):
        Thread.__init__(self)
        self.thread_id = thread_id
        self.function = func_name

    def run(self):
        print("Starting " + self.name)
        self.function()
        print("Exiting " + self.name)

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
        transac_count = 0
        c = 0
        count_person = []

        while True:
            if azure_call:
                azure_call = False

                file = "/home/pi/project/img/img.jpg"
                img = file

                if transac_count < 20:
                    azureDetect = CF.face.detect(img)
                    transac_count += 1

                    face_ids = [d['faceId'] for d in azureDetect]
                    azureFound = len(face_ids)

                    print("azureFound: " + str(azureFound))

                    if azureFound >= 1:
                        azure_identified_faces = CF.face.identify(face_ids, group_id)
                        transac_count += 1

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
                                        # count_person.append(person['personName'])
                                        # print('couunt_person: ' + count_person)
                                        c += 1
                                # for x in count_person:
                                #     print(x)

                        for k in range(found):
                            cprint('\tname: unknown', 'red')
                else:
                    print("Transaction:\tOver!!")

            else:
                sleep(1)


# class VideoCamera(object):
#     def __init__(self):
#         # Using OpenCV to capture from device 0. If you have trouble capturing
#         # from a webcam, comment the line below out and use a video file
#         # instead.
#         self.video = cv2.VideoCapture(0)
#         # If you decide to use video.mp4, you must have this file in the folder
#         # as the main.py.
#         # self.video = cv2.VideoCapture('video.mp4')
#
#     def __del__(self):
#         self.video.release()
#
#     def get_frame(self):
#         success, image = self.video.read()
#         # We are using Motion JPEG, but OpenCV defaults to capture raw images,
#         # so we must encode it into JPEG in order to correctly display the
#         # video stream.
#         ret, jpeg = cv2.imencode('.jpg', image)
#         return jpeg.tobytes()


def browser():
    # browser_thread()
    app = Flask(__name__)
    # hostname = socket.gethostname()
    # IPAddr = socket.gethostbyname(hostname)
    global cap
    ip = check_output(['hostname', '-I'])
    ip_de = ip.decode("utf-8")

    @app.route('/')
    def index():
        return render_template('home.html')

    def gen():
        # success, image = cap.video.read()
        # # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # # so we must encode it into JPEG in order to correctly display the
        # # video stream.
        # ret, jpeg = cv2.imencode('.jpg', image)
        # # return jpeg.tobytes()
        while True:
            success, image = cap.read()
            # if image.any:
            # if image == None:
            #     continue
            # if not np.sum(image) == 0:
            ret, jpeg = cv2.imencode('.jpg', image)
            frame = jpeg.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break
            #     cap.release()
            #     cv2.destroyAllWindows()

    @app.route('/video_feed')
    def video_feed():
        return Response(gen(),
                        mimetype='multipart/x-mixed-replace; boundary=frame')

    app.run(host=ip_de)


def open_camera():
    global cap
    global cascPath
    print("Starting...")
    MAX_CHECK_FRAME = 3
    width = 640
    height = 480
    allArrLastFound = 0
    currentFound = 0
    c_img = 0

    # cap = cv2.VideoCapture(0)
    cap.set(3, width)  # set Width
    cap.set(4, height)  # set Height

    # Get user supplied values
    # cascPath = "C:\opencv343\opencv\sources\data\haarcascades_cuda\haarcascade_frontalface_default.xml"
    # cascPath = "C:\opencv\sources\data\haarcascades_cuda\haarcascade_frontalface_default.xml"
    # cascPath = "C:\opencv-master\data\haarcascades_cuda\haarcascade_frontalface_default.xml"

    # Create the haar cascade
    faceCascade = cv2.CascadeClassifier(cascPath)

    frameCount = -1
    frameArr = [None] * MAX_CHECK_FRAME
    faceFoundArr = [None] * MAX_CHECK_FRAME
    confirmFound = 0
    allArrLastFound = 0

    while (True):
        # sleep(0.2)

        ret, frame = cap.read()
        # if not np.sum(frame) == 0:
        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # file = "D:/image/run/img" + str(c_img) + ".jpg"
        # cv2.imwrite(file, frame)
        # c_img += 1

        frameArr[frameCount] = frame
        frameCount += 1
        if frameCount == 3:
            frameCount = 0

        faces = faceCascade.detectMultiScale(
            frame,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(50, 50),
            flags=1
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
                print("casFound: " + str(allArrLastFound))

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # cv2.imshow('frame', frame)
        #
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     cap.release()
        #     cv2.destroyAllWindows()
        #     break
    # When everything done, release the capture
    return


def azure_camera():
    global cap
    global cascPath
    print("Starting...")
    azure_Thread()

    MAX_CHECK_FRAME = 3
    width = 640
    height = 480
    allArrLastFound = 0
    currentFound = 0

    # cap = cv2.VideoCapture(0)
    cap.set(3, width)  # set Width
    cap.set(4, height)  # set Height

    # Get user supplied values
    # cascPath = "C:\opencv343\opencv\sources\data\haarcascades_cuda\haarcascade_frontalface_default.xml"
    # cascPath = "C:\opencv-master\data\haarcascades_cuda\haarcascade_frontalface_default.xml"

    # Create the haar cascade
    faceCascade = cv2.CascadeClassifier(cascPath)

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
        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        frameCount += 1
        if frameCount == 3:
            frameCount = -1

        frameArr[frameCount] = frame

        faces = faceCascade.detectMultiScale(
            frame,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(120, 120),  # 1.5 m
            flags=0
        )

        if hasattr(faces, 'shape'):
            currentFound = faces.shape[0]
        else:
            currentFound = 0

        faceFoundArr[frameCount] = currentFound
        if len(set(faceFoundArr)) <= 1:
            confirmFound = faceFoundArr[2]
            # print(str(faceFoundArr) + " => " + str(all(faceFoundArr)))

            if confirmFound != allArrLastFound:
                allArrLastFound = confirmFound
                print("casFound: " + str(allArrLastFound))

                if (allArrLastFound == 0):
                    # print("casFound: " + str(allArrLastFound))
                    print()
                # else:
                # print("casFound: " + str(allArrLastFound), end="\t")

                if int(allArrLastFound) >= 1:
                    print('Checking...')
                    file = "/home/pi/project/img/img.jpg"
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

        # cv2.imshow('frame', frame)
        #
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     cap.release()
        #     cv2.destroyAllWindows()
        #     break
    # When everything done, release the capture
    return


# -----------------------------------Create group-----------------------------------
def createGroup():
    person_groups = CF.person_group.lists()
    group_name = input("\tEnter Group Name: ")
    group_id = input("\tEnter Group Id (must be lowercase): ")
    if any(person_group['personGroupId'] == group_id for person_group in person_groups):
        print("\t" + group_name + " is already exist")
    # must be lowercase
    else:
        CF.person_group.create(group_id, group_name)
        person_groups = CF.person_group.lists()
        if any(person_group['personGroupId'] == group_id for person_group in person_groups):
            print("\tCreate " + group_name + " => ", end='')
            cprint('Completed', 'green')
        else:
            print("\tCreate Group => Failed")
    print(text)


# -----------------------------------List group-----------------------------------
def listGroups():
    global personGroups
    groups = CF.person_group.lists()
    # time.sleep(TIME_SLEEP)
    print('Total Group List: ' + str(len(groups)))
    i = 1
    for group in groups:
        groupId = group['personGroupId']
        groupName = group['name']
        # CF.person_group.delete(person_group_id)
        print('\t{}'.format(i), end=' ')
        print('ID: ' + '{}'.format(groupId) + ' ,NAME: {}'.format(groupName))
        i += 1
        # time.sleep(TIME_SLEEP)
    print(text)


# # ---------------------------------Create person in group list----------------------------------
def createPerson(groupId, folderName):
    # personName = input("\tEnter Person Name: ")
    # if personName == 'q':
    #     return listFunction()
    # groupId = input("\tEnter Group Id (must be lowercase): ")
    # print('Select Group Id: ')
    # groups = CF.person_group.lists()
    # for group in groups:
    #     groupId = group['personGroupId']
    #     groupName = group['name']
    #     print('\t{}'.format(i), end=' ')
    #     print('ID: ' + '{}'.format(groupId) + ' ,NAME: {}'.format(groupName))
    res = CF.person.create(groupId, folderName)
    personId = ""
    if res:
        personId = res['personId']
        print("\tCreate " + folderName, end='')
        print('\t({}'.format(personId) + ') => ', end='')
        cprint('\tCompleted!', 'green')
    print(text)
    return personId


# # # ------------------------------------List person id in group------------------------------------
def listPersonInGroup():
    person_groups = CF.person_group.lists()
    group_id = input("\tselect group: ")
    # groupId = input("Enter Group Id (must be lowercase): ")
    if group_id == 'q':
        return listFunction()

    if any(person_group['personGroupId'] == group_id for person_group in person_groups):
        person_lists = CF.person.lists(group_id)
        # time.sleep(TIME_SLEEP)
        print('\tPerson List: ' + str(len(person_lists)))
        i = 0
        for person in person_lists:
            i += 1
            personName = str(person['name'])
            personId = str(person['personId'])
            print('\t' + str(i) + ". " + personName + ', ' + personId)
            # personIds.append({'personName': personName, 'personId': personId})
            # print(person)
    else:
        print('\tgroup ' + group_id + " doesn't exist!!")
    print(text)
    return listPersonInGroup()


# # ---------------------------------Add face person in group----------------------------------
def addPersonInGroup():
    global person_list

    groupId = input("\tEnter Group Id (must be lowercase): ")
    # personId = input("\tEnter Person Id: ")
    # folder = input("\tEnter Folder Name: ")

    allFolder = os.listdir("D:/image/" + str(groupId))
    leftPerson = allFolder.copy()
    print(allFolder)
    for aFolder in allFolder:
        # print('aFolder = ' + str(aFolder))
        for bPerson in person_list:
            if bPerson['personName'] == aFolder:
                print(str(aFolder) + " => OK")
                leftPerson.remove(aFolder)
                break

    # print('leftperson = '+str(leftPerson))
    for aPerson in leftPerson:
        path = "D:/image/" + groupId + '/' + aPerson + '/'
        lists = os.listdir(path)  # dir is your directory path
        number_files = len(lists)
        print('\t', end='')
        print('Create new person: ' + str(aPerson))
        print('\tnumber_files = ' + str(number_files))
        personId = createPerson(groupId, aPerson)
        for list in lists:
            fileName = path + list
            print('\t' + fileName)
            CF.person.add_face(fileName, groupId, personId)
            CF.person_group.train(groupId)
            response = CF.person_group.get_status(groupId)
            status = response['status']
            cprint('\t' + status, 'green')

    person_list = sync_person()


# # ---------------------------------Delete group----------------------------------
def deleteGroup():
    groupId = input("Enter Group Id (must be lowercase): ")
    CF.person_group.delete(groupId)
    cprint('Success!', 'green')
    print(text)


# # ---------------------------------Delete person in group----------------------------------
def deletePerson():
    global person_list
    groupId = input("Enter Group Id (must be lowercase): ")
    personId = input("Enter Person Id: ")
    CF.person.delete(groupId, personId)
    cprint('Success!', 'green')
    print(text)
    person_list = sync_person()


# # ---------------------------------Detection and identify----------------------------------
def detection():
    global person_list
    group_id = 'myteams'
    img_path = input("image name: ")
    if (img_path == 'q'):
        return listFunction()

    file_path = "D:/image/" + img_path + ".jpg"
    img = file_path

    azureDetect = CF.face.detect(img)

    im = Image.open(img).convert('RGBA')
    draw = ImageDraw.Draw(im)

    print('Azure Detect = ' + str(len(azureDetect)))
    if azureDetect:
        for face in azureDetect:
            # print("\t", end="")
            # print(getRectangle(face))
            draw.rectangle(getRectangle(face), outline='green')

        cascPath = "C:\opencv\sources\data\haarcascades_cuda\haarcascade_frontalface_default.xml"
        faceCascade = cv2.CascadeClassifier(cascPath)
        gray = cv2.imread(img)

        # print("\tazureDetect = " + str(len(azureDetect)))
        face_ids = [d['faceId'] for d in azureDetect]
        azure_identified_faces = CF.face.identify(face_ids, group_id)

        azureFound = len(face_ids)
        left = azureFound
        # print(azureFound)
        for count in range(azureFound):
            candidate = azure_identified_faces[count]['candidates']
            if not candidate:  # check empty list
                print('\tname: unknown')
                left -= 1
            else:
                candidate_personId = candidate[0]['personId']
                candidate_confidence = candidate[0]['confidence']

                for person in person_list:
                    if candidate_personId == person['personId']:
                        print('\tname: ' + person['personName'] + ', with confidence: ' + str(candidate_confidence))
                        left -= 1

        # print("left = " + str(left))
        for k in range(left):
            print('\tname: ever known')

        im.show()

    # facesCas = faceCascade.detectMultiScale(
    #     gray,
    #     scaleFactor=1.5,
    #     minNeighbors=5,
    #     minSize=(50, 50),
    #     flags=0
    # )
    # print("######")
    # print(facesCas)
    # for (x, y, w, h) in facesCas:
    #     cv2.rectangle(gray, (x, y), (x + w, y + h), (255, 0, 0), 2)
    # print("\t", end="")
    # print("x = " + str(x), end=", ")
    # print("y = " + str(y), end=", ")
    # print("w = " + str(w), end=", ")
    # print("h = " + str(h), end=", ")
    # print()


# # ---------------------------------List Function----------------------------------

def getRectangle(faceDictionary):
    rect = faceDictionary['faceRectangle']
    left = rect['left']
    top = rect['top']
    bottom = left + rect['height']
    right = top + rect['width']

    # print("left = " + str(rect['left']), end=", ")
    # print("top = " + str(rect['top']), end=", ")
    # print("height = " + str(rect['height']), end=", ")
    # print("width = " + str(rect['width']), end=", ")
    # print()
    return ((left, top), (bottom, right))


def getRectangle2(faceDictionary):
    rect = faceDictionary['faceRectangle']
    left = rect['left']
    top = rect['top']
    bottom = left + rect['height']
    right = top + rect['width']
    return ((left, top), (bottom, right))


def listFunction():
    global functions
    # functions = [{'describe': 'Create Group', 'function_name': 'createGroup'},
    #              {'describe': 'List Group', 'function_name': 'listGroup'},
    #              {'describe': 'Create Person', 'function_name': 'createPerson'},
    #              {'describe': 'List Person In Group', 'function_name': 'listPersonInGroup'},
    #              {'describe': 'Add Face Person In Group', 'function_name': 'addFacePerson'},
    #              {'describe': 'Delete Group', 'function_name': 'deleteGroup'},
    #              {'describe': 'Delete Person In Group', 'function_name': 'deletePerson'},
    #              {'describe': 'Detection', 'function_name': 'detection'},
    #              {'describe': 'List Function', 'function_name': 'listFunction'}]

    cprint('List Function', 'blue')
    for i in range(len(functions)):
        cprint("\t" + str(i + 1) + ". ", 'red', end='')
        cprint(str(functions[i]['describe']), 'red')
    cprint(text, 'white')


def verify():
    global list
    # groupId = input("Enter Group Id (must be lowercase): ")
    response = CF.face.detect('D:/image/geneGolf.jpg')
    test = CF.face.detect('D:/image/geneGolf.jpg')
    # test_faceId = test[0]['faceId']
    test_faceId = [d['faceId'] for d in test]
    print(test_faceId)
    # print(response)
    face_ids = [d['faceId'] for d in response]
    # print('Face Id'+'{}'.format(face_ids))
    identified_faces = CF.face.identify(face_ids, 'myteams')
    print(face_ids)
    for id in test_faceId:
        for f in face_ids:
            r = CF.face.verify(f, id)
            print(f, end='')
            cprint(r, 'red')


def sync_person():
    # list_group()
    person_groups = CF.person_group.lists()
    # group_name = input("select group: ")
    personIds = []

    group_name = 'myteams'
    if any(person_group['personGroupId'] == group_name for person_group in person_groups):
        person_lists = CF.person.lists(group_name)

        number = 0
        for person in person_lists:
            number += 1
            personName = str(person['name'])
            personId = str(person['personId'])
            print('\t' + str(number) + ". " + personName + ', ' + personId)
            personIds.append({'personName': personName, 'personId': personId})
            # print(person)

        # print(person_lists)
    else:
        print(group_name + " group doesn't exist!!")

    print('sync ' + str(len(personIds)) + ' persons')

    return personIds


def quit():
    print("Quit")
    exit(0)

def start_preview():
    global video_flask
    if video_flask == None:
        video_flask = myThread(1, browser)
        video_flask.start()

def stop_preview():
    global video_flask
    if video_flask != None:
        video_flask = myThread(1, browser)
        video_flask._stop()
        video_flask = None

# #-------------------------------------main program---------------------------------------------


sleep(3)
person_list = sync_person()
listFunction()
while (True):
    select = input('Select function: ')


    if str(select).isdigit() and int(select) >= 0 and int(select) <= len(functions):
        locals()[functions[int(select) - 1]['function_name']]()
    else:
        print("Please input number in range only")
        print(text)

