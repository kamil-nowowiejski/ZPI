import cv2
import numpy as np
from Agent.enums import Color


def find_contours(image, mode):
    contours = cv2.findContours(image, mode, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[1]
    result_contours = []
    for single_contour in contours:
        e = cv2.arcLength(single_contour, True)
        contour_area = cv2.contourArea(single_contour)
        if contour_area / image.size > 0.98:
            continue
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
    return 0, 50, 40


def maximum_bound():
    return 179, 255, 255


def color_bounds(color_id):
    lower_s = 50
    upper_s = 255
    lower_v = 40
    upper_v = 255

    bounds = {
        Color.RED: ((144, lower_s, lower_v), (11, upper_s, upper_v)),
        Color.YELLOW: ((12, lower_s, lower_v), (35, upper_s, upper_v)),
        Color.GREEN: ((36, lower_s, lower_v), (75, upper_s, upper_v)),
        Color.BLUE: ((76, lower_s, lower_v), (130, upper_s, upper_v)),
        Color.VIOLET: ((131, lower_s, lower_v), (143, upper_s, upper_v)),
    }

    return bounds[color_id]


def color_from_bounds(color):
    lower_s = 0
    upper_s = 256
    lower_v = 40
    upper_v = 256

    if not (lower_s <= color[1] <= upper_s or lower_v <= color[2] <= upper_v):
        return Color.NONE

    if 144 <= color[0] <= 180 or 0 <= color[0] <= 11:
        return Color.RED
    if 12 <= color[0] <= 35:
        return Color.YELLOW
    if 36 <= color[0] <= 75:
        return Color.GREEN
    if 76 <= color[0] <= 130:
        return Color.BLUE
    if 131 <= color[0] <= 143:
        return Color.VIOLET
    return Color.NONE
