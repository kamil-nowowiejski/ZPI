from hardwaremanagement.CameraManager import CameraManager
from detectionalgorythms.ObjectDetector import ObjectDetector
import detectionalgorythms.CornerDetector as cd
import detectionalgorythms.TemplateMatching as tm
import cv2

cameraManager = CameraManager()
objectDetector = ObjectDetector()

while True:
    frame = cameraManager.getNextFrame()
    scene = objectDetector.run(frame)
    #other detections