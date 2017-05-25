import cv2
import math
import numpy as np
from Agent.enums import Pattern


def find_pattern(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)

    min_line_length = 100
    lines = cv2.HoughLinesP(image=edges, rho=1, theta=np.pi / 180, threshold=85, lines=np.array([]), \
                            minLineLength=min_line_length, maxLineGap=200)

    if lines is None:
        return Pattern.NONE

    a, b, c = lines.shape
    for i in range(a):
        begin = (lines[i][0][0], lines[i][0][1])
        end = (lines[i][0][2], lines[i][0][3])
        cv2.line(image, begin, end, (255, 255, 0), 2, cv2.LINE_AA)

    cv2.imshow('ds',image)
    cv2.waitKey(0)
    pattern_color = _find_patterns_color(image)
    pattern = _assume_pattern(lines)
    return pattern, pattern_color


def _assume_pattern(lines):
    number_of_lines, _, _ = lines.shape
    angles = []
    for i in range(number_of_lines):
        begin = (lines[i][0][0], lines[i][0][1])
        end = (lines[i][0][2], lines[i][0][3])
        angles.append(_line_angle((begin, end)))

    number_of_horizontal_lines = sum(i >= 170 or i <= 10 for i in angles)
    number_of_vertical_lines = sum(i in range(80, 101) for i in angles)
    number_of_left_inclined_lines = sum(i in range(101, 170) for i in angles)
    number_of_right_inclined_lines = sum(i in range(11, 80) for i in angles)

    if float(number_of_horizontal_lines) / len(angles) > 0.6:
        return Pattern.HORIZONTAL_LINES
    if float(number_of_vertical_lines) / len(angles) > 0.6:
        return Pattern.VERTICAL_LINES
    if float(number_of_left_inclined_lines) / len(angles) > 0.6:
        return Pattern.LEFT_INCLINED_LINES
    if float(number_of_right_inclined_lines) / len(angles) > 0.6:
        return Pattern.RIGHT_INCLINED_LINES
    if float(number_of_vertical_lines) / len(angles) >= 0.3 and float(number_of_horizontal_lines) / len(angles) >= 0.3:
        return Pattern.GRID
    if float(number_of_left_inclined_lines) / len(angles) >= 0.3 and float(number_of_right_inclined_lines) / len(angles) >= 0.3:
        return Pattern.INCLINED_GRID
    return Pattern.NONE


def _line_angle(line):
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
    non_black_pixels = image[np.where((image != [0, 0, 0]).all(axis=2))]
    avg_color = (0., 0., 0.)
    for pixel in non_black_pixels:
        avg_color += pixel
    avg_color /= len(non_black_pixels)
    return avg_color
