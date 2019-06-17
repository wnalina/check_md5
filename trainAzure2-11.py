import cognitive_face as CF
import time
import sys
from termcolor import colored, cprint
import os, os.path
import cv2
from time import sleep

list =[['gene', 'c23fd3c5-ae04-4672-88a0-2927d34f32c0'],
       ['ice', '2d9111f8-0fa0-440b-af05-7a91ddc13e3f'],
       ['sprite', '2efc2b53-e2da-4276-a007-a1ed69ead0a6']]

functions = [{'describe': 'Open Camera', 'function_name': 'open_camera'},
             {'describe': 'Azure Camera', 'function_name': 'azure_camera'},
             {'describe': 'Create Group', 'function_name': 'createGroup'},
             {'describe': 'List Group', 'function_name': 'listGroups'},
             {'describe': 'Create Person', 'function_name': 'createPerson'},
             {'describe': 'List Person In Group', 'function_name': 'listPersonInGroup'},
             {'describe': 'Add Face Person In Group', 'function_name': 'addFacePerson'},
             {'describe': 'Delete Group', 'function_name': 'deleteGroup'},
             {'describe': 'Delete Person In Group', 'function_name': 'deletePerson'},
             {'describe': 'Detection', 'function_name': 'detection'},
             {'describe': 'List Function', 'function_name': 'listFunction'}]


SUBSCRIPTION_KEY = 'db816427ef814612975b8cb5479d3c8c'
BASE_URL = 'https://southeastasia.api.cognitive.microsoft.com/face/v1.0'
CF.BaseUrl.set(BASE_URL)
CF.Key.set(SUBSCRIPTION_KEY)

TIME_SLEEP = 5
text = '--------------------'



def open_camera():
    print("Starting...")
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
            minSize=(50, 50),
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
                print("casFound: " + str(allArrLastFound))

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            break
    # When everything done, release the capture
    return


def azure_camera():
    print("Starting...")
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
    group_id = 'myteams'

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
            minSize=(80, 100),
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
                    print("casFound: " + str(allArrLastFound))
                else:
                    print("casFound: " + str(allArrLastFound), end="\t")

                if int(allArrLastFound) >= 1:
                    file = "D:/image/img.jpg"
                    cv2.imwrite(file, frame)
                    img = file

                    azureDetect = CF.face.detect(img)
                    face_ids = [d['faceId'] for d in azureDetect]
                    azureFound = len(face_ids)

                    print("azureFound: " + str(azureFound))

                    if azureFound >= 1:
                        azure_identified_faces = CF.face.identify(face_ids, group_id)

                        left = azureFound
                        for count in range(azureFound):
                            candidate = azure_identified_faces[count]['candidates']
                            if not candidate:  # check empty list
                                cprint('\tname: unknown', 'red')
                                left -= 1
                            else:
                                candidate_personId = candidate[0]['personId']
                                candidate_confidence = candidate[0]['confidence']

                                for person in person_list:
                                    if candidate_personId == person['personId']:
                                        cprint('\tname: ' + person['personName'] + ', with confidence: ' + str(
                                            candidate_confidence), 'green')
                                        left -= 1

                        for k in range(left):
                            cprint('\tname: unknown', 'red')
                    print(text)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            break
    # When everything done, release the capture
    return


# -----------------------------------Create group-----------------------------------
def createGroup() :
    person_groups = CF.person_group.lists()
    group_name = input("\tEnter Group Name: ")
    group_id = input("\tEnter Group Id (must be lowercase): ")
    if any(person_group['personGroupId'] == group_id for person_group in person_groups):
        print("\t"+ group_name + " is already exist")
    #must be lowercase
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
    personName = input("\tEnter Person Name: ")
    if personName == 'q':
        return listFunction()
    groupId = input("\tEnter Group Id (must be lowercase): ")
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
        print("\tCreate " + personName, end='')
        print('\t({}'.format(personId) + ') => ', end='')
        cprint('\tCompleted!', 'green')
    print(text)
    return createPerson()

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
        print('\tPerson List: '+str(len(person_lists)))
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
def addFacePerson():
    groupId = input("\tEnter Group Id (must be lowercase): ")
    personId = input("\tEnter Person Id: ")
    folderName  =  input("\tEnter Folder Name: ")
    path = "D:/image/" + groupId + '/' + folderName + '/'
    lists = os.listdir(path)  # dir is your directory path
    # print(path)
    # print(list)
    number_files = len(lists)
    print('\t', end='')
    print(number_files)
    for list in lists:
        fileName = path + list
        print('\t' + fileName)
        CF.person.add_face(fileName, groupId, personId)
        CF.person_group.train(groupId)
        response = CF.person_group.get_status(groupId)
        status = response['status']
        cprint('\t' + status, 'green')


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
def detection():
    global person_list
    group_id = 'myteams'
    img_path = input("image name: ")
    if (img_path == 'q'):
        return listFunction()

    file_path = "D:/image/" + img_path + ".jpg"
    img = file_path

    azureDetect = CF.face.detect(img)
    print("\tazureDetect = " + str(len(azureDetect)))
    face_ids = [d['faceId'] for d in azureDetect]
    azure_identified_faces = CF.face.identify(face_ids, group_id)

    azureFound = len(face_ids)

    left = azureFound
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

    return detection()

    # for t in candidates :
    #     i = [d['confidence'] for d in t]
    #     print('Confidence: '+'{}'.format(i))


# # ---------------------------------List Function----------------------------------
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
        cprint("\t" + str(i + 1) + ". ", 'red',  end='')
        cprint(str(functions[i]['describe']), 'red')
    cprint(text, 'white')

def verify():
    global list
    # groupId = input("Enter Group Id (must be lowercase): ")
    response = CF.face.detect('D:/img/2person.jpg')
    test = CF.face.detect('D:/img/gene.jpg')
    test_faceId = test[0]['faceId']
    print(test_faceId)
    # print(response)
    face_ids = [d['faceId'] for d in response]
    # print('Face Id'+'{}'.format(face_ids))
    identified_faces = CF.face.identify(face_ids, 'myteams')
    for f in face_ids:
        r = CF.face.verify(f, test_faceId)
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
            print('\t'+str(number) + ". " + personName + ', ' + personId)
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

# #-------------------------------------main program---------------------------------------------
person_list = sync_person()
listFunction()
# print(list[0])
while (True):
    select = input('Select function: ')
    # select = int(input(print(colored('Select function: ', 'blue'), end=' ')))
    # text = colored('Hello, World!', 'red', attrs=['reverse', 'blink'])
    # print(text)
    # print(select)
    # if select == 1:
    #     createGroup()
    # elif select == 2:
    #     listGroups()
    # elif select == 3:
    #     createPerson()
    # elif select == 4:
    #     listPersonInGroup()
    # elif select == 5:
    #     addFacePerson()
    # elif select == 6:
    #     deleteGroup()
    # elif select == 7:
    #     deletePerson()
    # elif select == 8:
    #     detection()
    # elif select == 9:
    #     listFunction()
    # elif select == 10:
    #     verify()
    # else:
    #     print('This function does not exist. Please try again.')

    if str(select).isdigit() and int(select) >= 0 and int(select) <= len(functions):
        locals()[functions[int(select) - 1]['function_name']]()
    else:
        print("Please input number in range only")
        print(text)
