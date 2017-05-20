import cv2
import Agent.ImageProcessing.contour_detection as cd
from Agent.enums import Color

'''
There is no 100% guarantee that triangle will be detected as three point curve.
Sometimes it is recognized as 4 points curve but it is still ok, because extra point is very close to
one of other three main points. That gives chance to reduce this extra point using RDP algorithm - shape_detection in
our case.
'''


def test_detect_contours_blue_pentagon():
    frame = cv2.imread('images/obj_det_blue_pentagon.bmp')
    contours = cd.detect_contours(Color.BLUE, frame)
    assert len(contours) is 1
    assert contours[0].shape[0] is 5 or contours[0].shape[0] is 6


def test_detect_contours_red_square():
    frame = cv2.imread('images/obj_det_blue_pentagon.bmp')
    contours = cd.detect_contours(Color.RED, frame)
    assert len(contours) is 1
    assert contours[0].shape[0] is 4 or contours[0].shape[0] is 5


def test_detect_contours_green_triangle():
    frame = cv2.imread('images/obj_det_green_triangle.bmp')
    contours = cd.detect_contours(Color.GREEN, frame)
    assert len(contours) is 1
    assert contours[0].shape[0] is 3 or contours[0].shape is 4


def test_detect_contours_blue_rectangle():
    frame = cv2.imread('images/obj_det_green_triangle.bmp')
    contours = cd.detect_contours(Color.BLUE, frame)
    assert len(contours) is 1
    assert contours[0].shape[0] is 3 or contours[0].shape[0] is 4
