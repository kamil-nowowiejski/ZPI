from hardwaremanagement.CameraManager import CameraManager
from detectionalgorythms.ObjectDetector import ObjectDetector
import detectionalgorythms.CornerDetector as cd
import detectionalgorythms.TemplateMatching as tm
import detectionalgorythms.SizeMeasuring as sm
import cv2

cameraManager = CameraManager()
objectDetector = ObjectDetector()

#img = cv2.imread('test_images/sm_test.jpg')
#sm.calculate(img, 4.5)

while True:
    frame = cameraManager.getNextFrame()
    #cd.shiTomasiDetection(frame, maxCorners=200, minDistance=5, qualityLevel=0.01)
    scene = objectDetector.run(frame)
    #other detections

