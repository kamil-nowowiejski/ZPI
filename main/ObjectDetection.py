import cv2
import numpy as np
from enum import Enum
'''
color - tuple(lower_bound, upper_bound), where lower_bound and upper_bound are tuples representing HSV color space
Hue is value from [0,180], not [0,360]
frame - image tu analyze
'''
def detect(color, frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    colorBounds = getColorBounds(color)
    mask = None
    if colorBounds[0] > colorBounds[1]:
        mask1 = cv2.inRange(hsv, colorBounds[0], getMaximumBound())
        mask2 = cv2.inRange(hsv, getMinimumBound(), colorBounds[1])
        mask = cv2.bitwise_or(mask1, mask2)
    else:
        mask = cv2.inRange(hsv, colorBounds[0], colorBounds[1])
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    cnts, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    result_shape = None
    result_shape_area = 0;
    for single_contour in cnts:
        e = cv2.arcLength(single_contour, True)
        shape = cv2.approxPolyDP(single_contour, e * 0.02, closed=True)
        contour_area = cv2.contourArea(single_contour)
        if contour_area > 500 and contour_area > result_shape_area:
            result_shape = shape
            result_shape_area = contour_area

    return convertNumpyShapeToMatrixOfPoints(result_shape)

def convertNumpyShapeToMatrixOfPoints(numpyShape):
    result = []
    numberOfVertexes = numpyShape.shape[0]
    for i in range(0, numberOfVertexes):
        x = numpyShape[i][0][0]
        y = numpyShape[i][0][1]
        result.append([x, y])
    return np.array(result)

def getMinimumBound():
    return (0, 86, 6)

def getMaximumBound():
    return (179, 255, 255)

def getColorBounds(colorId):
    lower_s = 86
    upper_s = 255
    lower_v = 6
    upper_v = 255

    bounds = {
        Color.RED: ((172, lower_s, lower_v), (7, upper_s, upper_v)),
        Color.ORANGE: ((11, lower_s, lower_v), (25, upper_s, upper_v)),
        Color.YELLOW: ((28, lower_s, lower_v), (30, upper_s, upper_v)),
        Color.GREEN: ((33, lower_s, lower_v), (82.5, upper_s, upper_v)),
        Color.BLUE: ((85, lower_s, lower_v), (138, upper_s, upper_v)),
        Color.VIOLET: ((142.5, lower_s, lower_v), (171, upper_s, upper_v)),
    }
    return bounds[colorId]

class Color(Enum):
    RED = 1
    ORANGE = 2
    YELLOW = 3
    GREEN = 4
    BLUE = 5
    VIOLET = 6
