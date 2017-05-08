import cv2
import numpy as np
import contour_detection as cd
import shape_detection as sd
from enums import Color
from object import Shape


class ObjectDetector:

    def __init__(self, detected_contours=[]):
        self.detected_contours = detected_contours

    def detect_objects(self, frame, auto_contour_clear=True):
        detected_objects = []

        if frame is not None:
            frame_copy = self._prepare_image_for_detection(frame.copy())
            for main_color in Color:
                contours_list = cd.detect_contours(main_color, frame_copy)
                if contours_list is []:
                    continue

                hull_contours_list = []
                for single_contour in contours_list:
                    hull_contours_list.append(cv2.convexHull(single_contour))

                for single_contour in hull_contours_list:
                    self.detected_contours.append((main_color, single_contour))
                    detected_objects.append(self._calculate_object_from_contour(main_color, single_contour, frame_copy))
            if auto_contour_clear:
                self.clear_contours()

        return detected_objects

    def clear_contours(self):
        self.detected_contours = []

    def _calculate_object_from_contour(self, color, contour, frame):

        main_shape = sd.detect_shape(cd.convert_numpy_array_for_shape_detection(contour))
        mask = np.zeros(frame.shape, np.uint8)
        cv2.fillPoly(mask, [contour], (255, 255, 255))
        mask = cv2.bitwise_and(mask, frame)
        symbols_list = self._find_symbols_in_range(color, mask)

        return Shape(main_shape, -1, -1, color, symbols_list)

    def _find_symbols_in_range(self, main_color, sub_img):

        symbols_list = []

        for symbol_color in Color:
            if symbol_color is main_color:
                continue
            symbol_contours = cd.detect_contours(symbol_color, sub_img)
            if symbol_contours is not None:
                for single_contour in symbol_contours:
                    self.detected_contours.append((symbol_color, single_contour))
                    symbol_shape = sd.detect_shape(cd.convert_numpy_array_for_shape_detection(single_contour))
                    symbol = Shape(symbol_shape, -1, -1, symbol_color)
                    symbols_list.append(symbol)

        return symbols_list

    def _prepare_image_for_detection(self, im):
        if self._percentage_of_bright_pixels(im) < 0.4:
            im = self._adjust_gamma(im, 2.0)
        im = self._remove_background(im)
        return self._k_means(im, 12)

    def _remove_background(self, im):
        '''remove light gray and white color'''
        im = cv2.cvtColor(im, cv2.COLOR_BGR2HLS)
        mask = cv2.inRange(im, (0, 140, 0), (179, 255, 255))
        mask = cv2.bitwise_not(mask)
        im = cv2.bitwise_and(im, im, mask=mask)
        return cv2.cvtColor(im, cv2.COLOR_HLS2BGR)

    def _adjust_gamma(self, image, gamma=1.0):
        '''change brightness'''
        # build a lookup table mapping the pixel values [0, 255] to
        # their adjusted gamma values
        inv_gamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** inv_gamma) * 255
                          for i in np.arange(0, 256)]).astype("uint8")

        # apply gamma correction using the lookup table
        return cv2.LUT(image, table)

    def _k_means(self, im, k):
        '''color quantization'''
        img = im.reshape((-1, 3))
        img = np.float32(img)

        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        ret, label, center = cv2.kmeans(img, k, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

        center = np.uint8(center)
        res = center[label.flatten()]
        res = res.reshape(im.shape)
        return res

    def _percentage_of_bright_pixels(self, im):
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2HLS)
        gray = cv2.inRange(gray, (0, 160, 0), (179, 255, 255))
        number_of_pixels = gray.shape[0] * gray.shape[1]
        bright_pixels = cv2.countNonZero(gray)
        return float(bright_pixels) / float(number_of_pixels)
