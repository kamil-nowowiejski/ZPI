import cv2
import numpy as np
import shape_detection as sd
import pictures_transformations as pt
import contour_detection as cd
import pattern_recognition as pr
from Agent.enums import Color, ColorSpace, Pattern
from Agent.object import Shape


class ObjectDetector:

    def __init__(self, detected_contours=[]):
        self.detected_contours = detected_contours

    def detect_objects(self, frame, auto_contour_clear=True, prepare_image_befor_detection=True):
        detected_objects = []

        if frame is not None:
            frame_copy = frame.copy()
            if prepare_image_befor_detection:
                frame_copy = self._prepare_image_for_detection(frame_copy)
            for main_color in Color:
                contours_list = cd.detect_contours(main_color, frame_copy)

                if contours_list is []:
                    continue

                hull_contours_list = []
                for single_contour in contours_list:
                    hull_contours_list.append(cv2.convexHull(single_contour))

                for single_contour in hull_contours_list:
                    self.detected_contours.append((main_color, single_contour))
                    object = self._calculate_object_from_contour(main_color, single_contour, frame_copy)
                    detected_objects.append(object)

            if auto_contour_clear:
                self.clear_contours()

        return detected_objects

    def clear_contours(self):
        self.detected_contours = []

    def _calculate_object_from_contour(self, color, contour, frame):

        image_for_symbol_detection = self._prepare_image_for_symbol_detection(frame, contour)
        image_for_pattern_recognition = self._prepare_image_for_pattern_recognition(frame, contour, color)

        main_shape = sd.detect_shape(cd.convert_numpy_array_for_shape_detection(contour))
        pattern = pr.find_pattern(image_for_pattern_recognition)
        symbols_list = self._find_symbols_in_range(color, image_for_symbol_detection)

        return Shape(main_shape, -1, -1, color, pattern, symbols_list)

    def _find_symbols_in_range(self, main_color, sub_img):

        symbols_list = []

        for symbol_color in Color:
            if symbol_color is main_color:
                continue
            symbol_contours = cd.detect_contours(symbol_color, sub_img)
            if symbol_contours is not None:
                for single_contour in symbol_contours:
                    e = cv2.arcLength(single_contour, True)
                    single_contour = cv2.approxPolyDP(single_contour, e * 0.02, closed=True)
                    self.detected_contours.append((symbol_color, single_contour))
                    symbol_shape = sd.detect_shape(cd.convert_numpy_array_for_shape_detection(single_contour))
                    symbol = Shape(symbol_shape, -1, -1, symbol_color, Pattern.NONE)
                    symbols_list.append(symbol)

        return symbols_list

    def _prepare_image_for_symbol_detection(self, frame, contour):
        mask = np.zeros(frame.shape, np.uint8)
        cv2.fillPoly(mask, [contour], (255, 255, 255))
        return cv2.bitwise_and(mask, frame)

    def _prepare_image_for_pattern_recognition(self, frame, contour, color):
        mask = np.zeros(frame.shape, np.uint8)
        cv2.fillPoly(mask, [contour], (255, 255, 255))
        image_for_pattern = cv2.cvtColor(cv2.bitwise_and(mask, frame), cv2.COLOR_BGR2HSV)
        color_range = cd.color_bounds(color)
        image_for_pattern = cv2.inRange(image_for_pattern, color_range[0], color_range[1])
        image_for_pattern = cv2.cvtColor(image_for_pattern, cv2.COLOR_GRAY2BGR)
        image_for_pattern = cv2.bitwise_xor(mask, image_for_pattern)
        image_for_pattern = cv2.bitwise_and(image_for_pattern, frame)
        image_for_pattern = cv2.cvtColor(image_for_pattern, cv2.COLOR_BGR2HSV)

        non_black_pixels = image_for_pattern[np.where((image_for_pattern != [0, 0, 0]).all(axis=2))]
        avg_color = (0., 0., 0.)
        for pixel in non_black_pixels:
            avg_color += pixel
        avg_color /= len(non_black_pixels)
        return image_for_pattern

    def _prepare_image_for_detection(self, im):
        if pt.percentage_of_bright_pixels(im, ColorSpace.BGR) < 0.4:
            im = pt.adjust_gamma(im, 2.0)
        im = pt.remove_light_gray_background(im)
        return pt.color_quantization_using_k_means(im, 12)
