import cv2

cap = cv2.VideoCapture(0)
cascPath = "C:\opencv-master\data\haarcascades_cuda\haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)

while (True):
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(100, 100),
        flags=0
    )
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow('video streaming', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # if cv2.waitKey(1) & 0xFF == ord('c'):
    #     cv2.imwrite('img.jpg',frame)

cap.release()
cv2.destroyAllWindows()
