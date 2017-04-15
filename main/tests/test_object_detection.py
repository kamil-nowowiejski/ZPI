import main.objects_detection as od
import cv2


def test():
    frame = cv2.imread('tests/images/object_detection_1.jpg')
    objects_list = od.detect_objects(frame)
    print objects_list
