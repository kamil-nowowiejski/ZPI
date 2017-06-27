import cv2
import numpy as np
import shape_detection as sd
import pictures_transformations as pt
import pattern_recognition as pr
import common_operations as common
import size_detection as size_det
from Server.enums import Color, ColorSpace, Pattern
from Server.enums import Shape as enumShape
from Server.object import Shape, CombinedObject
from Agent.resources import ares


class ObjectDetector:
    """
    Class used for object detection.
    Instance of this class should be used for extracting list of objects from image.
    """

    def __init__(self, detected_contours=[]):
        """
        Constructor of ObjectDetector
        :param detected_contours: all objects cotours which were detected during process of detection, this list is used
        for visualization of detected objects
        """
        self.detected_contours = detected_contours

    def detect_objects(self, frame, real_distance=None, auto_contour_clear=True, prepare_image_before_detection=True):
        """
        Method used for extracting objects form image
        :param frame: image from which objects should be extracted
        :param real_distance: distance from objects scene - this value should be read from sensor
        :param auto_contour_clear: if True, field detected_contours will clear itself after every function call
        :param prepare_image_before_detection: if True, image will be prepared for detection
                using _prepare_image_for_detection methid
        :return: list of detected objects
        """

        if frame is None:
            return []

        frame_copy = frame.copy()
        if prepare_image_before_detection:
            frame_copy = self._prepare_image_for_detection(frame_copy)
        result = []

        #cv2.imshow('dsv', frame_copy)
        #cv2.waitKey(0)

        # find contours of all combinded objects; here basic objects are considered to be combined objects
        external_contours = self._find_external_contours(frame_copy)
        for single_contour in external_contours:
            single_object_image = self._prepare_image_for_single_combined_object(frame_copy, single_contour)
            part_objects = self._detect_part_objects(single_object_image, real_distance)

            # if list of part objects contains only one element than detected combined object contains only one
            # part object which means that it should be considered as basic object
            if len(part_objects) is 1:
                result.append(part_objects[0])
            elif len(part_objects) > 1:
                shape_type = sd.detect_shape(common.convert_numpy_array_for_shape_detection(single_contour))
                real_width, real_height = size_det.assume_size_from_contour(real_distance, single_contour, frame.shape)
                result.append(CombinedObject(type=shape_type, width=real_width, height=real_height, parts=part_objects))

        if auto_contour_clear:
            self.clear_contours()
        return result

    def _find_external_contours(self, image):
        """
        Find contours of combined objects in given image
        :param image: raw image from camera or prepared for detection image
        :return: contours list of combined objects in the image
        """
        canny_threshold_1 = ares('image_processing_params\\combined_objects_detecion\\canny_threshold_1')
        canny_threshold_2 = ares('image_processing_params\\combined_objects_detecion\\canny_threshold_2')
        edges = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        edges = cv2.Canny(edges, canny_threshold_1, canny_threshold_2)
        edges = cv2.dilate(edges, None, iterations=2)
        edges = cv2.erode(edges, None, iterations=2)
        return common.find_contours(edges, cv2.RETR_EXTERNAL)

    def _prepare_image_for_single_combined_object(self, image, contour):
        """
        Creates image where only one combined object is visible and background is black
        :param image: image which are to be prepared for detection of single combined object
        :param contour: contour of combined object
        :return: image with only one combined object
        """
        mask = np.zeros(image.shape, np.uint8)
        cv2.fillPoly(mask, [contour], (255, 255, 255))
        mask = cv2.bitwise_and(mask, image)
        return mask

    def _detect_part_objects(self, image, real_distance):
        """
        Finds basic objects within combined object
        :param image: image where only one combined object is visible
        :param real_distance: distance from objects scene - this value should be read from sensor
        :return: list of basic objects which together create combined object
        """
        result = []
        for main_color in [c for c in Color if c != Color.NONE]:
            # find contours of objects with color main_color
            contours_list = self._detect_basic_objects_contours(main_color, image)
            if contours_list is []:
                continue

            # remove concave contours
            hull_contours_list = []
            for single_contour in contours_list:
                hull_contours_list.append(cv2.convexHull(single_contour))

            for single_contour in hull_contours_list:
                self.detected_contours.append((main_color, single_contour))
                object = self._calculate_object_from_contour(main_color, single_contour, image, real_distance)
                if object is not None:
                    result.append(object)
        result = self._remove_symbol_objects(result)
        return result

    def _prepare_image_for_detection(self, im):
        """
        If image is considered to be dark then it's brightened.
        After this from image is removed light gray / white background.
        Then start process of color quantization which reduce color noise
        :param im: raw image from camera
        :return: image ready to for process of object detection
        """

        dark_pixels_percentage_border = ares('image_processing_params\\image_preparetion\\dark_pixels_percentage_border')
        gamma_increase = ares('image_processing_params\\image_preparetion\\gamma_increase')
        number_of_quantizied_colors = ares('image_processing_params\\image_preparetion\\number_of_quantizied_colors')
        if pt.percentage_of_bright_pixels(im, ColorSpace.BGR) < dark_pixels_percentage_border:
            im = pt.adjust_gamma(im, gamma_increase)
        im = pt.remove_light_gray_background(im)
        return pt.color_quantization_using_k_means(im, number_of_quantizied_colors)

    def clear_contours(self):
        """
        Removes all detected contours
        :return: None
        """
        self.detected_contours = []

    def _calculate_object_from_contour(self, color, contour, frame, real_distance):
        """
        Creates basic object instance
        :param color: color of detected basic object
        :param contour: contour of detected basic object
        :param frame: image where searched object is present; others objects can be present too
        :param real_distance: distance from objects scene - this value should be read from sensor
        :return: instance of basic object
        """

        main_shape = sd.detect_shape(common.convert_numpy_array_for_shape_detection(contour))

        if main_shape is enumShape.LINE:
            return None

        image_for_symbol_detection = self._prepare_image_for_symbol_detection(frame, contour)
        symbols_list = self._find_symbols_in_range(color, image_for_symbol_detection, real_distance)

        pattern, pattern_color = Pattern.NONE, Color.NONE
        if len(symbols_list) is 0:
            image_for_pattern_recognition = self._prepare_image_for_pattern_recognition(frame, contour, color)
            pattern, pattern_color = pr.find_pattern(image_for_pattern_recognition)

        real_width, real_height = size_det.assume_size_from_contour(real_distance, contour, frame.shape)

        return Shape(main_shape, real_width, real_height, color, pattern, pattern_color, symbols_list)

    def _find_symbols_in_range(self, main_color, sub_img, real_distance):
        """
        Finds symbols of single basic object
        :param main_color: color of basic object which may contain symbols
        :param sub_img: image where only one basic object is present
        :param real_distance: distance from objects scene - this value should be read from sensor
        :return: list of detected symbols
        """

        symbols_list = []

        for symbol_color in [c for c in Color if c != Color.NONE]:
            if symbol_color is main_color:
                continue
            symbol_contours = self._detect_basic_objects_contours(symbol_color, sub_img)
            if symbol_contours is not None:
                for single_contour in symbol_contours:
                    e = cv2.arcLength(single_contour, True)
                    single_contour = cv2.approxPolyDP(single_contour, e * 0.02, closed=True)
                    self.detected_contours.append((symbol_color, single_contour))
                    symbol_shape = sd.detect_shape(common.convert_numpy_array_for_shape_detection(single_contour))

                    if symbol_shape is enumShape.LINE:
                        continue

                    real_width, real_height = size_det.assume_size_from_contour(real_distance, single_contour, sub_img.shape)

                    symbol = Shape(symbol_shape, real_width, real_height, symbol_color, Pattern.NONE, Color.NONE)
                    symbols_list.append(symbol)

        return symbols_list

    def _prepare_image_for_symbol_detection(self, frame, contour):
        """
        Creates image suitable for detecting symbols of one basic object
        :param frame: image where many basic objects may be present
        :param contour: contour of basic object which may or may not have symbols
        :return: image where only one basic object is present
        """

        mask = np.zeros(frame.shape, np.uint8)
        cv2.fillPoly(mask, [contour], (255, 255, 255))
        return cv2.bitwise_and(mask, frame)

    def _prepare_image_for_pattern_recognition(self, frame, contour, color):
        """
        Creates image suitable for detecting pattern of one basic object
        :param frame: image where many basic objects may be present
        :param contour: contour of basic object which may or may not have pattern
        :param color: color of searched basic object
        :return: image where only pattern is visible, if no pattern is present image is blacj
        """

        mask = np.zeros(frame.shape, np.uint8)
        cv2.fillPoly(mask, [contour], (255, 255, 255))
        image_for_pattern = cv2.cvtColor(cv2.bitwise_and(mask, frame), cv2.COLOR_BGR2HSV)
        color_range = common.color_bounds(color)
        if color_range[0][0] > color_range[1][0]:
            mask1 = cv2.inRange(image_for_pattern, color_range[0], common.maximum_bound())
            mask2 = cv2.inRange(image_for_pattern, common.minimum_bound(), color_range[1])
            image_for_pattern = cv2.bitwise_or(mask1, mask2)
        else:
            image_for_pattern = cv2.inRange(image_for_pattern, color_range[0], color_range[1])

        image_for_pattern = cv2.cvtColor(image_for_pattern, cv2.COLOR_GRAY2BGR)
        image_for_pattern = cv2.bitwise_xor(mask, image_for_pattern)
        image_for_pattern = cv2.bitwise_and(image_for_pattern, frame)

        return image_for_pattern

    def _remove_symbol_objects(self, objects):
        """
        Given list of all detected objects removes those which are classified as symbols
        :param objects: list of detected objects
        :return: list of detected objects where symbols are excluded
        """

        result = []
        symbols = []
        for obj in objects:
            if len(obj.symbols) > 0:
                for symbol in obj.symbols:
                    symbols.append(symbol)
        indexes = []
        for symbol in symbols:
            for i in range(0, len(objects)):
                if objects[i].quasi_equals(symbol):
                    indexes.append(i)
                    break
        for i in range(0, len(objects)):
            if i not in indexes:
                result.append(objects[i])

        return result

    def _detect_basic_objects_contours(self, color, frame):
        """
        Finds list of contours of objects with given color
        :param color: color id representing color of searched basic object
        :param frame: image where many different basic objects are present
        :return: contours list of objects with given color
        """

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        color_bound = common.color_bounds(color)
        if color_bound[0] > color_bound[1]:
            mask1 = cv2.inRange(hsv, color_bound[0], common.maximum_bound())
            mask2 = cv2.inRange(hsv, common.minimum_bound(), color_bound[1])
            mask = cv2.bitwise_or(mask1, mask2)
        else:
            mask = cv2.inRange(hsv, color_bound[0], color_bound[1])
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        result_contours = common.find_contours(mask.copy(), cv2.RETR_EXTERNAL)
        return result_contours

