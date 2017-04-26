import cv2
import numpy as np
import contour_detection as cd
import shape_detection as sd
from Enums.Color import Color
from Object import Shape


def detect_objects(frame):
    detected_objects = []

    if frame is not None:
        frame_copy = frame.copy()
        for main_color in Color:
            contours_list = cd.detect_contours(main_color, frame_copy)
            if contours_list is []:
                continue

            for single_contour in contours_list:
                detected_objects.append(_calculate_object_from_contour(main_color, single_contour, frame_copy))

    return detected_objects


def _calculate_object_from_contour(color, contour, frame):

    main_shape = sd.detect_shape(cd.convert_numpy_array_for_shape_detection(contour))
    mask = np.zeros(frame.shape, np.uint8)
    cv2.fillPoly(mask, [contour], (255, 255, 255))
    mask = cv2.bitwise_and(mask, frame)
    symbols_list = _find_symbols_in_range(color, mask)

    return Shape(main_shape, -1, -1, color, symbols_list)


def _find_symbols_in_range(main_color, sub_img):

    symbols_list = []

    for symbol_color in Color:
        if symbol_color is main_color:
            continue
        symbol_contours = cd.detect_contours(symbol_color, sub_img)
        if symbol_contours is not None:
            for single_contour in symbol_contours:
                symbol_shape = sd.detect_shape(cd.convert_numpy_array_for_shape_detection(single_contour))
                symbol = Shape(symbol_shape, -1, -1, symbol_color)
                symbols_list.append(symbol)

    return symbols_list


def rectangles_union(a, b):

    x = min(a[0], b[0])
    y = min(a[1], b[1])
    w = max(a[0]+a[2], b[0]+b[2]) - x
    h = max(a[1]+a[3], b[1]+b[3]) - y
    return x, y, w, h
