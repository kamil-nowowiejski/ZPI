import cv2
import math
import numpy as np
import common_operations as common
from Server.enums import Pattern, Color
from Agent.resources import ares


def find_pattern(image):
    """
    Find pattern and its color in the given image
    :param image: image where only pattern is visible, image must be in BGR color space
    :return: tuple in form of (pattern, color_pattern), where
            pattern is pattern id defined in class Pattern from enums.py,
            pattern_color is color id defined in class Color from enums.py
    """

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    canny_threshold_1 = ares('image_processing_params\\pattern_recognition\\canny_threshold_1')
    canny_threshold_2 = ares('image_processing_params\\pattern_recognition\\canny_threshold_2')
    edges = cv2.Canny(gray, canny_threshold_1, canny_threshold_2)

    min_line_length = ares('image_processing_params\\pattern_recognition\\minimum_line_length')
    hough_lines_threshold = ares('image_processing_params\\pattern_recognition\\hough_lines_threshold')
    max_line_gap = ares('image_processing_params\\pattern_recognition\\max_line_gap')
    lines = cv2.HoughLinesP(image=edges, rho=1, theta=np.pi / 180, threshold=hough_lines_threshold, lines=np.array([]),
                            minLineLength=min_line_length, maxLineGap=max_line_gap)

    if lines is None:
        return Pattern.NONE, Color.NONE

    pattern_color = _find_patterns_color(cv2.cvtColor(image, cv2.COLOR_BGR2HSV))
    pattern = _assume_pattern(lines)
    return pattern, pattern_color


def _assume_pattern(lines):
    """
    Given ndarray containing lines of pattern assume its pattern
    :param lines: ndarray containing line of pattern
    :return: pattern id defined in class Pattern from enums.py
    """

    number_of_lines, _, _ = lines.shape
    angles = []
    for i in range(number_of_lines):
        begin = (lines[i][0][0], lines[i][0][1])
        end = (lines[i][0][2], lines[i][0][3])
        angles.append(_line_angle((begin, end)))

    angle_epsilon = ares('image_processing_params\\pattern_recognition\\angle_epsilon')
    number_of_horizontal_lines = sum(i >= 180 - angle_epsilon or i <= angle_epsilon for i in angles)
    number_of_vertical_lines = sum(90 - angle_epsilon <= i <= 90 + angle_epsilon for i in angles)
    number_of_left_inclined_lines = sum(90 + angle_epsilon < i < 180 - angle_epsilon for i in angles)
    number_of_right_inclined_lines = sum(angle_epsilon < i < 90 - angle_epsilon for i in angles)

    percentage_of_line_type_to_qualify_as_pattern = ares('image_processing_params\\pattern_recognition\\'
                                                         'percentage_of_line_type_to_qualify_as_pattern')
    if float(number_of_horizontal_lines) / len(angles) > percentage_of_line_type_to_qualify_as_pattern:
        return Pattern.HORIZONTAL_LINES
    if float(number_of_vertical_lines) / len(angles) > percentage_of_line_type_to_qualify_as_pattern:
        return Pattern.VERTICAL_LINES
    if float(number_of_left_inclined_lines) / len(angles) > percentage_of_line_type_to_qualify_as_pattern:
        return Pattern.LEFT_INCLINED_LINES
    if float(number_of_right_inclined_lines) / len(angles) > percentage_of_line_type_to_qualify_as_pattern:
        return Pattern.RIGHT_INCLINED_LINES
    if float(number_of_vertical_lines) / len(angles) >= percentage_of_line_type_to_qualify_as_pattern / 2 and \
       float(number_of_horizontal_lines) / len(angles) >= percentage_of_line_type_to_qualify_as_pattern / 2:
        return Pattern.GRID
    if float(number_of_left_inclined_lines) / len(angles) >= percentage_of_line_type_to_qualify_as_pattern / 2 and \
       float(number_of_right_inclined_lines) / len(angles) >= percentage_of_line_type_to_qualify_as_pattern / 2:
        return Pattern.INCLINED_GRID
    return Pattern.NONE


def _line_angle(line):
    """
    Calculates the agle of line
    :param line: ndarray representing line
    :return: angle of line in degrees
    """

    a = line[0]
    b = line[1]
    if a[1] < b[1]:
        temp = a
        a = b
        b = temp
    c = (a[0], b[1])
    horizontal_length = b[0] - c[0]
    vertical_length = a[1] - c[1]
    line_length = math.sqrt(pow(a[0] - b[0], 2) + pow(a[1] - b[1], 2))
    sin_alpha = vertical_length / line_length
    cos_alpha = horizontal_length / line_length
    alpha = math.degrees(math.atan2(sin_alpha, cos_alpha))
    if alpha == 180:
        alpha = 0
    return alpha


def _find_patterns_color(image):
    """
    Find color of pattern in image
    :param image: image with only pattern present
    :return: color id defined in class Color from enums.py
    """
    non_black_pixels = image[np.where((image != [0, 0, 0]).all(axis=2))]
    if len(non_black_pixels) is 0:
        return Color.NONE
    avg_color = (0., 0., 0.)
    for pixel in non_black_pixels:
        avg_color += pixel
    avg_color /= len(non_black_pixels)
    return common.color_from_bounds(avg_color)
