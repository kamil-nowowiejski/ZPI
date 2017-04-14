import main.objects_detection as od
import cv2
import os


def test():
    frame = cv2.imread('tests/images/test_img5.jpg')
    frame = cv2.resize(frame, None, fx=0.25, fy=0.25, interpolation=cv2.INTER_AREA)
    objects_list = od.detect_objects(frame)
    print objects_list