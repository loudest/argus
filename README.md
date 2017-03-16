## Python videostreams for facial detection & biometrics

1. Analyize video streams with OpenCV object detection of faces and apply biometric markers to data.
2. Utilize IoT sensors (such as tempature, humidity) to improve the data collection process.

![Screenshot](screenshot.png)

## Challenge and Approach

Our approach for satisfying this challenge was to:

- Utilize the computer's webcam to detect bounding boxes for eyes, nose, and mouth.  Once the bounding region has been assigned with machine learning, the biometric marker is compared against a mathematical predictive models to improved facial recognition detection.
- Run the webcam on a Raseberry PI or server with Flask acting as a micro-service to stream video realtime as a image/jpeg video feed.

## Team Members

Our team is comprised of:

- [@loudest](https://github.com/loudest) - README.md writer, took the "blue pill" in the matrix and spent 3 days at [VR Hackathon - Seattle] (http://vrhackathon.com/seattle.html) coding this

## Technologies, APIs, and Datasets Utilized

We made use of:
- [Flask](http://flask.pocoo.org/) to render local host and video streams
- [OpenCV](http://opencv.org/) for video analysis and facial detection
- [openbr](http://openbiometrics.org/) biometrics markers and using machine learning to improve accuracy
- [Arduino Uno](https://www.arduino.cc/en/Main/ArduinoBoardUno/) to obtain temperature and humidity data.

## How to run our app:

1. Go into the server/ directory
2. Run it via: python main.py

## TO-DO

1. [Blocking I/O] In camera.py, the function parse_serial_connection() utilizes a COM3 serial connection on an Arduino board.  The I/O is polling very 60 seconds.
2. [Threading] Update sensor data as a sperate thread with a dynamic endpoint to a Flask route.  

Our code is licensed under the [MIT License](LICENSE.md). Pull requests will be accepted to this repo, pending review and approval.
