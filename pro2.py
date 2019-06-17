import cognitive_face as CF
from time import sleep
from termcolor import cprint
import cv2

functions = ['open_camera', 'azure_camera', 'azure_image', 'list_group', 'list_person',
             'create_group', 'create_person_group', 'detection', 'sync_person', 'quit']

TIME_SLEEP = 0.5
KEY = 'db816427ef814612975b8cb5479d3c8c'                                    # Oil's key1
BASE_URL = 'https://southeastasia.api.cognitive.microsoft.com/face/v1.0'    # Replace with your regional Base URL

CF.Key.set(KEY)
CF.BaseUrl.set(BASE_URL)

# group id
group_id = 'myteams'

# person id

# Notification of wait.
MSG_WAIT = 'Wait for {} seconds so as to avoid exceeding free quote.'


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
    cascPath = "C:\opencv343\opencv\sources\data\haarcascades_cuda\haarcascade_frontalface_default.xml"

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
            minSize=(100, 100),
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

                        found = azureFound
                        for count in range(azureFound):
                            candidate = azure_identified_faces[count]['candidates']
                            if not candidate:  # check empty list
                                print('\tname: unknown')
                            else:
                                candidate_personId = candidate[0]['personId']
                                candidate_confidence = candidate[0]['confidence']

                                for person in person_list:
                                    if candidate_personId == person['personId']:
                                        print('\tname: ' + person['personName'] + ', with confidence: ' + str(
                                            candidate_confidence))
                                        found -= 1

                        for k in range(found):
                            print('\tname: unknown')

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            break
    # When everything done, release the capture
    return


def azure_image():
    img_path = input("image name: ")
    if(img_path == 'q'):
        return

    file_path = "D:/image/"+img_path+".jpg"
    img = file_path

    azureDetect = CF.face.detect(img)
    print("azureDetect = " + str(len(azureDetect)))
    face_ids = [d['faceId'] for d in azureDetect]
    azure_identified_faces = CF.face.identify(face_ids, group_id)

    azureFound = len(face_ids)


    left = azureFound
    for count in range(azureFound):
        candidate = azure_identified_faces[count]['candidates']
        if not candidate:                   # check empty list
            print('\tname: unknown')
            left -= 1
        else:
            candidate_personId = candidate[0]['personId']
            candidate_confidence = candidate[0]['confidence']

            for person in person_list:
                if candidate_personId == person['personId']:
                    print('\tname: ' + person['personName'] + ', with confidence: ' + str(candidate_confidence))
                    left -= 1

    print("left = " + str(left))
    for k in range(left):
        print('\tname: ever known')


    return azure_image()


def detection():
    global list
    # groupId = input("Enter Group Id (must be lowercase): ")
    response = CF.face.detect('D:/image/gene.jpg')
    print("detect")
    print(response)
    face_ids = [d['faceId'] for d in response]
    # print('Face Id'+'{}'.format(face_ids))
    identified_faces = CF.face.identify(face_ids, 'myteams')
    # print(identified_faces)
    for identified_face in identified_faces:
         print("identify")
         cprint(identified_face, "blue")
         candidates = identified_face['candidates']
         # print(candidates)

         if candidates :
             # cprint(candidates, "green")
             personId = identified_face['candidates'][0]['personId']
             confidence = identified_face['candidates'][0]['confidence']
             print('\tId: ', end='')
             cprint(personId, 'green')
             print('\tConfidence: ', end='')
             cprint(confidence, 'green')

             person_lists = list
             range = len(person_lists)
             # print(range)
             i = 0
             while i < range:
                 id = person_lists[i][1]
                 if  personId == id:
                     name = person_lists[i][0]
                     print('\tName: ', end='')
                     cprint(name, 'green')

                 i += 1
         else:
             cprint("\tnot found", "red")


def create_group():
    person_groups = CF.person_group.lists()
    group_name = input("\tGroup name: ")
    if any(person_group['personGroupId'] == group_name for person_group in person_groups):
        print("\t"+ group_name + " is already exist")
    else:
        CF.person_group.create(group_name, group_name)
        person_groups = CF.person_group.lists()
        if any(person_group['personGroupId'] == group_name for person_group in person_groups):
            print("\tCreate " + group_name + " => Completed")
        else:
            print("\tCreate Group => Failed")


def create_person_group():
    print("=> create_person_group: NEED TO IMPLEMENT ")


def list_group():
    person_groups = CF.person_group.lists()
    print('Person Group List: '+str(len(person_groups)))
    for person_group in person_groups:
        person_group_id = person_group['personGroupId']
        person_group_name = person_group['name']
        print('\tgroupId: ' + str(person_group_id) + '\t\tgroupName: ' + str(person_group_name))
        sleep(TIME_SLEEP)


def list_person():
    # list_group()
    person_groups = CF.person_group.lists()
    group_name = input("select group: ")
    personIds = [{}]

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
            sleep(TIME_SLEEP)

        # print(person_lists)
    else:
        print(group_name + " group doesn't exist!!")


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


# --------------------------------------------------------main-------------------------------------------------------- #
while True:
    print('---------------------------------------------')
    person_list = sync_person()
    # print("person_list = " + str(person_list))
    print("Function: ")
    for i in range(len(functions)):
        print("\t"+str(i+1)+". "+functions[i])

    select = input('Select: ')

    if str(select).isdigit() and int(select) >= 0 and int(select) <= len(functions):
        locals()[functions[int(select)-1]]()
    else:
        print("Please input number in range only")
