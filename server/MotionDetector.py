import imutils
import datetime
import time
import cv2
from FacialDetect import frameFacialDetect

def treatFrame(img):
    img = imutils.resize(img, width=500)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return cv2.GaussianBlur(img, (21, 21), 0)

def motionDetector(minArea=None, adjustRate=None,delay=None):
    minArea = 200
    adjustRate = 0.2
    delay = 1
    camera = cv2.VideoCapture(0)
    ret, frame = camera.read()
    normalFrame = treatFrame(frame).copy().astype("float")
    while True:
        status, color = "No Movement", (0, 255, 0)
        ret, frame = camera.read()
        currentFrame = treatFrame(frame)
        cv2.accumulateWeighted(currentFrame, normalFrame, adjustRate)
        delta = cv2.absdiff(currentFrame, cv2.convertScaleAbs(normalFrame))
        thresh = cv2.threshold(delta, 25, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)
        _,cnts,_ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for c in cnts:
            if cv2.contourArea(c) < minArea:
                continue
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)
            status, color = "Motion Detected", (0, 0, 255)
        cv2.putText(frame, status, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
        cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 255, 0), 1)
        cv2.imshow("Camera", frame)
        k = cv2.waitKey(delay) & 0xFF
        if k == 27:
            break
    del(camera)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    motionDetector()
