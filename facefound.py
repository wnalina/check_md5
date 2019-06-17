import cv2

width = 640
height = 480

cap = cv2.VideoCapture(1)           # nb cam
cap.set(3, width)  # set Width
cap.set(4, height)  # set Height

# face_cascade_Path = "C:\opencv\sources\data\haarcascades_cuda\haarcascade_frontalface_default.xml"
# face_cascade_Path = "/home/pi/opencv-3.4.3/data/haarcascades_cuda/haarcascade_frontalface_default.xml"
face_cascade_Path = "C:\opencv-master\data\haarcascades_cuda\haarcascade_frontalface_default.xml"
face_cascade = cv2.CascadeClassifier(face_cascade_Path)

lastFound = 0
currentFound = 0

print("Starting...")
while(True):
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(160, 160),
        # maxSize=(200, 200),
        flags=0
    )

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow('frame', frame)

    if hasattr(faces, 'shape'):
        currentFound = faces.shape[0]
        if currentFound != lastFound:
            lastFound = currentFound
            print(currentFound)
    else:
        currentFound = 0
        lastFound = 0
        #print('0')

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
