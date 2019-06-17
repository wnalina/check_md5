import cognitive_face as CF
import time
import sys
from termcolor import colored, cprint
import os, os.path

list =[['gene', 'd30f428e-0a15-4eb5-9f07-d5886dd5a574'],
       ['ice', 'f29d819f-8b24-4bb6-bd17-055bc64ed32c'],
       ['oil', '41f3c76d-5bee-418b-8f65-5233b3521789'],
       ['sprite', '7f96cced-fe6c-4ed4-8332-33a0c36f6aeb']]

SUBSCRIPTION_KEY = 'db816427ef814612975b8cb5479d3c8c'
BASE_URL = 'https://southeastasia.api.cognitive.microsoft.com/face/v1.0'
CF.BaseUrl.set(BASE_URL)
CF.Key.set(SUBSCRIPTION_KEY)

TIME_SLEEP = 5
text = '--------------------'



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
def detection():
    global list
    # groupId = input("Enter Group Id (must be lowercase): ")
    response = CF.face.detect('D:/img/gene.jpg')
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

    # for t in candidates :
    #     i = [d['confidence'] for d in t]
    #     print('Confidence: '+'{}'.format(i))


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
             "List Function"]
    i = 1
    cprint('List Function', 'blue')
    for list in lists:
        cprint('\t{} '.format(i) + '{}'.format(list), 'red')
        # print(colored(i, 'red'), end=' ')
        # print(list)
        i += 1
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

# #-------------------------------------main program---------------------------------------------
listFunction()
# print(list[0])
while (True):
    select = int(input('Select function: '))
    # select = int(input(print(colored('Select function: ', 'blue'), end=' ')))
    # text = colored('Hello, World!', 'red', attrs=['reverse', 'blink'])
    # print(text)
    # print(select)
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
        detection()
    elif select == 9:
        listFunction()
    elif select == 10:
        verify()
    else:
        print('This function does not exist. Please try again.')
        print(text)
