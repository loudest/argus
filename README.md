## Python videostreams for facial recognization & biometrics

![Screenshot](screenshot.png)

## Challenge and Approach

Our approach for satisfying this Machine Learning challenge was to:

1. Analyize video streams with facial object detection and apply biometric markers to data (facial recognition).
2. Utilize IoT sensors (tempature, humidity) to improve the data collection process (location data).
3. Develop a microservice that outputs JSON data so datasets can be collected and used by a Machine Learning API.

## Team Members

Our team is comprised of:

- [@loudest](https://github.com/loudest) - README.md writer, took the "blue pill" in the matrix and spent 3 days at [VR Hackathon - Seattle] (http://vrhackathon.com/seattle.html) coding this

## Technologies, APIs, and Datasets Utilized

I made use of:
- [Flask](http://flask.pocoo.org/) python RESTful microservice
- [OpenCV](http://opencv.org/) for video analysis and facial detection
- [openbr](http://openbiometrics.org/) facial biometrics 
- [Arduino Uno](https://www.arduino.cc/en/Main/ArduinoBoardUno/) to obtain temperature and humidity data.
- [JS Stats](http://github.com/mrdoob/stats.js) javascript for video frame rate detection and CPU utilization

## Microservice REST API explained
Flask service listens to the following REST endpoints:
1. /video_feed - raw video feed as Motion JPEG stream 
2. /sensor_data - IoT sensor data returned as JSON: {"temperature":string,"humidity":string}
3. /facial_data - Facial biometrics as JSON: {"data":{"head_cordinates":array[{x,y}],"left_eye_coordinates":array[{x,y}],"right_eye_coordinates":array[{x,y}],"mouth_coordinates":array[{x,y}],"mood":string,"facial_hash_string":string}

## How to run our app:

1. Go into the server/ directory
2. Run it via: python main.py

## TO-DO

1. [Blocking I/O] In camera.py, the function parse_serial_connection() utilizes a COM3 serial connection on an Arduino board.  The I/O is polling very 60 seconds.
2. [Threading] Update sensor data as a sperate thread with a dynamic endpoint to a Flask route.  

Our code is licensed under the [MIT License](LICENSE.md). Pull requests will be accepted to this repo, pending review and approval.
