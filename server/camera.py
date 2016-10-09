import cv2, sys, time, datetime, numpy as np, itertools as it, serial
from glob import glob
import SMSTwilio

eyes = cv2.CascadeClassifier("haarcascades/haarcascade_eye.xml")
mouth = cv2.CascadeClassifier("haarcascades/haarcascade_mcs_mouth.xml")
nose = cv2.CascadeClassifier("haarcascades/haarcascade_mcs_nose.xml")
head = cv2.CascadeClassifier("haarcascades/haarcascade_frontalface_default.xml")
overlay_mask = cv2.imread("static/images/overlay.png", -1)
overlay_eyes = cv2.imread("static/images/eye.png", -1)
#overlay_logo = cv2.imread("static/images/logo.png", -1)
text_color = (0, 255, 0)

def detect_bounds(img, cascade):
    rects = cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(30, 30), flags = cv2.CASCADE_SCALE_IMAGE)
    if len(rects) == 0:
        return []
    rects[:,2:] += rects[:,:2]
    return rects

def draw_rects(img, rects, color):
    for x1, y1, x2, y2 in rects:
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)

def draw_overlay(img, rect, overlay_image):
    x1, y1, x2, y2 = rect
    y=y2-y1 + 40
    x=x2-x1 + 40
    small = cv2.resize(overlay_image, (x, y))

    x_offset = x1 - 10
    y_offset = y1 - 10

    for c in range(0,3):
        img[y_offset:y_offset + small.shape[0], x_offset:x_offset+ small.shape[1], c] = small[:,:,c] * (small[:,:,3]/255.0) + img[y_offset:y_offset+small.shape[0], x_offset:x_offset+small.shape[1], c] * (1.0 - small[:,:,3]/255.0)

def blur_rectangle(img, rect):
    x, y, w, h = rect    
    sub_face = img[y:y+h, x:x+w]
    sub_face = cv2.GaussianBlur(sub_face,(23, 23), 30)
    img[y:y+sub_face.shape[0], x:x+sub_face.shape[1]] = sub_face

def parse_serial_connection():
    serial_object = serial.Serial(
        port='COM3',
        baudrate=9600,
        parity=serial.PARITY_ODD,
        stopbits=serial.STOPBITS_TWO,
        bytesize=serial.SEVENBITS
    )
    string = serial_object.read(15)
    string = string.strip()
    array = string.split('\r\n')
    temperature = 0.0
    humidity = 0.0
    if(array[0] != None):
        temperature = float(array[0].strip())
    if(array[1] != None):
        humidity =  float(array[1].strip())
    value = {"temperature":str(temperature),"humidity":str(humidity)}
    print value
    serial_object.close()
    return value

class VideoCamera(object):

    def __init__(self):
        #init values
        self.video = cv2.VideoCapture(0)
        data = parse_serial_connection()
        self.temperature = data['temperature']
        self.humidity = data['humidity']
        self.lock = 0
    
    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()

        if success == True:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            gray = cv2.equalizeHist(gray)
            found_eyes = detect_bounds(gray, eyes)
            found_head = detect_bounds(gray, head)

            # only draw head
            if (len(found_head) > 0):
                draw_rects(image, found_head, (255, 255, 255))
                for rect in found_eyes:
                    try:
                        draw_overlay(image, rect, overlay_eyes)
                    except:
                        pass
                if(self.lock % 300 == 0):
                    SMSTwilio.send_sms(self.humidity, self.temperature)

            # get sensor data and only use if current minute is even to update temperature for polling
            if(self.lock % 60 == 0):
                data = parse_serial_connection()
                self.temperature = str(data['temperature'])
                self.humidity = str(data['humidity'])

            #semaphore lock
            self.lock = self.lock + 1

            # draw overlay
            temperature_string = "Temperature: "+str(self.temperature)+"F"
            humidity_string = "Humidity: "+str(self.humidity)+'%'
            cv2.rectangle(image, (0, 0), (280, 70), (0,0,0), -1)
            cv2.putText(image, temperature_string, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.8, text_color, 2)
            cv2.putText(image, humidity_string, (10, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.8, text_color, 2)            
            cv2.putText(image, datetime.datetime.now().strftime("%A, %d %B %Y - %I:%M:%S %p"), (10, image.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
		  
            # drag logo
            #draw_overlay(image, [0,0,1,1], overlay_logo)

        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()
