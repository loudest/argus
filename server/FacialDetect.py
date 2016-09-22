import numpy as np
import cv2

def facialDetect(cascadePath=None):
    if cascadePath == None:
        cascadePath = "haarcascades/haarcascade_frontalface_default.xml"
    camera = cv2.VideoCapture(0)
    while True:
        res, frame = camera.read()
        cascade = cv2.CascadeClassifier(cascadePath)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.imshow('face detection', frame)
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            cv2.destroyAllWindows()
            break
    del(camera)

def frameFacialDetect(frame, cascadePath=None, color=None):
    if cascadePath == None:
        cascadePath = "haarcascade_frontalface_default.xml"
    if color == None:
        color = (0, 255, 0)
    cascade = cv2.CascadeClassifier(cascadePath)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
    return frame