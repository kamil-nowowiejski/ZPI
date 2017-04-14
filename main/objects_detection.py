import cv2
import numpy as np
import contour_detection as cd
import shape_detection as sd
from Enums.Color import Color
from object import Object


def detect_objects(frame):
    detected_objects = []

    frame_copy = frame.copy()
    for main_color in Color:
        contours_list = cd.detect_contours(main_color, frame_copy)
        if contours_list is []:
            continue

        for single_contour in contours_list:
            detected_objects.append(_calculate_object_from_contour(main_color, single_contour, frame_copy))

    return detected_objects


def _calculate_object_from_contour(color, contour, frame):

    x, y, w, h = cv2.boundingRect(contour)
    sub_img = frame[y:y + h, x:x + w]
    main_shape = sd.detect_shape(cd.convert_numpy_array_for_shape_detection(contour))
    symbols_list = _find_symbols_in_range(color, sub_img)

    bounding_point = np.array([[x, y], [x+w, y], [x+w, y+h], [x, y+h]], np.int32)

    cv2.fillPoly(frame, [bounding_point], 0)
    return Object(color, main_shape, symbols_list)


def _find_symbols_in_range(main_color, sub_img):

    symbols_list = []

    for symbol_color in Color:
        if symbol_color is main_color:
            continue
        symbol_contours = cd.detect_contours(symbol_color, sub_img)
        if symbol_contours is not None:
            for single_contour in symbol_contours:
                symbol_shape = sd.detect_shape(cd.convert_numpy_array_for_shape_detection(single_contour))
                symbol = Object(symbol_color, symbol_shape, [])
                symbols_list.append(symbol)

    return symbols_list
