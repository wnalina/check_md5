import cv2
import cognitive_face as CF
import os, os.path
from termcolor import colored, cprint


cascPath = "C:\opencv-master\data\haarcascades_cuda\haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)

SUBSCRIPTION_KEY = 'db816427ef814612975b8cb5479d3c8c'
BASE_URL = 'https://southeastasia.api.cognitive.microsoft.com/face/v1.0'
CF.BaseUrl.set(BASE_URL)
CF.Key.set(SUBSCRIPTION_KEY)

filename = 'D:/image/pcy/crop/img000.jpg'
# W = 1000.
oriimg = cv2.imread(filename)
gray = cv2.cvtColor(oriimg, cv2.COLOR_BGR2GRAY)
faces = faceCascade.detectMultiScale(
    gray,
    scaleFactor=1.1,
    minNeighbors=5,
    minSize=(30, 30),
    flags=0
)

# for (x, y, w, h) in faces:
#     cv2.rectangle(oriimg, (x, y), (x + w, y + h), (0, 255, 0), 2)
#     crop_img = oriimg[y:y + h, x:x + w]
#     file = "D:/image/pcy/img003.jpg"
#     cv2.imwrite(file, crop_img)

#
# img = cv2.imread('D:/image/pcy/crop/img003.jpg')
# newimg = cv2.resize(img,(int(41),int(41)))
# cv2.imwrite('D:/image/pcy/test3/img9.jpg',newimg)
# cprint('resize complete', 'green')

def getRectangle(faceDictionary):
    rect = faceDictionary['faceRectangle']
    left = rect['left']
    top = rect['top']
    bottom = left + rect['height']
    right = top + rect['width']
    return ((left, top), (bottom, right))

path = 'D:/image/pcy/test3/'
lists = os.listdir(path)
for i in lists:
    fileName = path + i
    print(fileName)
    detection = CF.face.detect(fileName)
    print(detection)

    im = cv2.imread(fileName)
    for face in detection:
        # print(face['faceId'])
        rec = getRectangle(face)
        crop_img = im[rec[0][1]:rec[1][1], rec[0][0]:rec[1][0]]
        cv2.imwrite(path + 'azure' + i + '.jpg', crop_img)

