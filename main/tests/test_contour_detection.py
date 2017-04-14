import main.contour_detection as od
import cv2
import numpy as np


def detect_shape_in_image_test():
    frame = cv2.imread('images/test_img5.jpg')
    frame = cv2.resize(frame, None, fx=0.25, fy=0.25, interpolation=cv2.INTER_AREA)
    shape = od.detect_contours(od.Color.RED, frame)

    cv2.drawContours(frame, [shape], -1, (255, 255, 255), 3)

    cv2.imshow('Original', frame)
    cv2.waitKey(0)


def color_bounds_test():
    img = cv2.imread('hsv_color_test.jpg')
    colors = [od.Color.RED, od.Color.ORANGE, od.Color.YELLOW, od.Color.GREEN, od.Color.BLUE, od.Color.VIOLET]
    for color in colors:
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        colorBounds = od.get_color_bounds(color)
        mask = cv2.inRange(hsv, colorBounds[0], colorBounds[1])
        cv2.imshow('Mask', mask)
        cv2.waitKey(0)

detect_shape_in_image_test()