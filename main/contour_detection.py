import cv2
import numpy as np
from enums import Color
'''
color - tuple(lower_bound, upper_bound), where lower_bound and upper_bound are tuples representing HSV color space
Hue is value from [0,180], not [0,360]
frame - images tu analyze
'''


def detect_contours(color, frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    color_bound = color_bounds(color)
    if color_bound[0] > color_bound[1]:
        mask1 = cv2.inRange(hsv, color_bound[0], maximum_bound())
        mask2 = cv2.inRange(hsv, minimum_bound(), color_bound[1])
        mask = cv2.bitwise_or(mask1, mask2)
    else:
        mask = cv2.inRange(hsv, color_bound[0], color_bound[1])
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    cnts, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    result_contours = []
    for single_contour in cnts:
        e = cv2.arcLength(single_contour, True)
        contour_area = cv2.contourArea(single_contour)
        if contour_area > 500:
            result_contour = cv2.approxPolyDP(single_contour, e * 0.02, closed=True)
            result_contours.append(result_contour)

    return result_contours


def convert_numpy_array_for_shape_detection(numpy_shape):
    result = []
    if numpy_shape is not None:
        number_of_vertexes = numpy_shape.shape[0]
        for i in range(0, number_of_vertexes):
            x = numpy_shape[i][0][0]
            y = numpy_shape[i][0][1]
            result.append([x, y])
        return np.array(result)


def minimum_bound():
    return 0, 86, 6


def maximum_bound():
    return 179, 255, 255


def color_bounds(color_id):
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
    return bounds[color_id]
