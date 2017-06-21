import cv2
import numpy as np
from Server.enums import Color
from Agent.resources import ares
from ast import literal_eval


def find_contours(image, mode):
    """
    Finds contours in given image
    :param image: image from which contours are to be found; it is best for image to be binary image
    :param mode: openCV mode for detecting contours;
                mode can be one of the following: cv2.RETR_EXTERNAL, cv2.RETR_FLOODFILL, cv2.RETR_LIST,
                cv2.RETR_CCOMP, cv2.RETR_TREE

    :return: list of detected contours
    """

    _, contours, _ = cv2.findContours(image, mode, cv2.CHAIN_APPROX_SIMPLE)
    result_contours = []
    for single_contour in contours:
        e = cv2.arcLength(single_contour, True)
        contour_area = cv2.contourArea(single_contour)
        # if contour area is about 98% of whole image size then contour is just frame of the image
        if contour_area / image.size > 0.98:
            continue
        # if contour area is less than given param (recommended 500) it is considered to be noise and should be ignored
        if contour_area > ares('image_processing_params\\contour_area_noise_border'):
            result_contour = cv2.approxPolyDP(single_contour, e * 0.02, closed=True)
            result_contours.append(result_contour)
    return result_contours


def convert_numpy_array_for_shape_detection(numpy_shape):
    """
    Converts numpy ndarray representing contour to ndarray suitable for shape detection.
    It is used alongside with shape_detection.py.
    :param numpy_shape: contour represents as ndarray
    :return: ndarray suitable for shape detection
    """

    result = []
    if numpy_shape is not None:
        number_of_vertexes = numpy_shape.shape[0]
        for i in range(0, number_of_vertexes):
            x = numpy_shape[i][0][0]
            y = numpy_shape[i][0][1]
            result.append([x, y])
        return np.array(result)


def minimum_bound():
    """
    Minimal possible color in HSV color space
    :return: tuple in form of (hue, saturation, value)
    """
    return literal_eval(ares('image_processing_params\\colors\\min_color_bound_hsv'))


def maximum_bound():
    """
    Maximal possible color in hsv color space
    :return: tuple in form of (hue, saturation, value)
    """
    return literal_eval(ares('image_processing_params\\colors\\max_color_bound_hsv'))


def color_bounds(color_id):
    """
    Given color_id returns bounds of this color in hsv color space
    :param color_id: color id defined in class Color from enums.py
    :return: tuple represents color bounds of given color
    """

    min_bound = minimum_bound()
    max_bound = maximum_bound()
    lower_s = min_bound[1]
    upper_s = max_bound[1]
    lower_v = min_bound[2]
    upper_v = max_bound[2]

    red_bound = literal_eval(ares('image_processing_params\\colors\\red_hue_bound'))
    yellow_bound = literal_eval(ares('image_processing_params\\colors\\yellow_hue_bound'))
    green_bound = literal_eval(ares('image_processing_params\\colors\\green_hue_bound'))
    blue_bound = literal_eval(ares('image_processing_params\\colors\\blue_hue_bound'))
    violet_bound = literal_eval(ares('image_processing_params\\colors\\violet_hue_bound'))

    bounds = {
        Color.RED: ((red_bound[0], lower_s, lower_v), (red_bound[1], upper_s, upper_v)),
        Color.YELLOW: ((yellow_bound[0], lower_s, lower_v), (yellow_bound[1], upper_s, upper_v)),
        Color.GREEN: ((green_bound[0], lower_s, lower_v), (green_bound[1], upper_s, upper_v)),
        Color.BLUE: ((blue_bound[0], lower_s, lower_v), (blue_bound[1], upper_s, upper_v)),
        Color.VIOLET: ((violet_bound[0], lower_s, lower_v), (violet_bound[1], upper_s, upper_v)),
    }

    return bounds[color_id]


def color_from_bounds(color):
    """
    Given color tuple in from of (hue, saturation, value) returns it's id from Color in enums.py
    :param color: tuple representing color in hsv color space in form of (hue, saturation, value)
    :return: color id defined in class Color from enums.py
    """

    min_bound = minimum_bound()
    max_bound = maximum_bound()
    lower_s = min_bound[1]
    upper_s = max_bound[1]
    lower_v = min_bound[2]
    upper_v = max_bound[2]

    red_bound = literal_eval(ares('image_processing_params\\colors\\red_hue_bound'))
    yellow_bound = literal_eval(ares('image_processing_params\\colors\\yellow_hue_bound'))
    green_bound = literal_eval(ares('image_processing_params\\colors\\green_hue_bound'))
    blue_bound = literal_eval(ares('image_processing_params\\colors\\blue_hue_bound'))
    violet_bound = literal_eval(ares('image_processing_params\\colors\\violet_hue_bound'))

    if not (lower_s <= color[1] <= upper_s or lower_v <= color[2] <= upper_v):
        return Color.NONE

    if red_bound[0] <= color[0] <= max_bound[0] or min_bound[0] <= color[0] <= red_bound[1]:
        return Color.RED
    if yellow_bound[0] <= color[0] <= yellow_bound[1]:
        return Color.YELLOW
    if green_bound[0] <= color[0] <= green_bound[1]:
        return Color.GREEN
    if blue_bound[0] <= color[0] <= blue_bound[1]:
        return Color.BLUE
    if violet_bound[0] <= color[0] <= violet_bound[1]:
        return Color.VIOLET
    return Color.NONE
