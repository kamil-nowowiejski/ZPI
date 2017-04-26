import cv2
import objects_detection as od
import database as db
import logger as log
import time

class Main:
    exit = False

    def __init__(self):
        pass


log.agent_registration()
cameraManager = cv2.VideoCapture(0)
for i in range(10):
    _, image = cameraManager.read()
    detected_objects = od.detect_objects(image)
    for object in detected_objects:
        db.insert(object)
    time.sleep(5)
cameraManager.release()
'''server = HTTPServer()
server.run()
cameraManager = cv2.VideoCapture(0)
while not exit:
    ret, image = cameraManager.read()
    detected_objects = od.detect_objects(image)
    for object in detected_objects:
        db.insert(object)
    exit = True

cameraManager.realease()
'''