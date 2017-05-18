import cv2
import numpy as np

import main.ImageProcessing.contour_detection as cd
import main.ImageProcessing.shape_detection as sd


class BlockDetector:

    def __init__(self):
        self.external_contours = []
        self.internal_contours = []
        self.masked_images = []

    def _find_external_contours(self, image):
        res = cv2.cvtColor(image, cv2.COLOR_BGR2HLS)
        mask = cv2.inRange(res, (0, 0, 0), (180, 40, 255))
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        result = []
        for single_contour in contours:
            e = cv2.arcLength(single_contour, True)
            contour_area = cv2.contourArea(single_contour)
            if contour_area > 1500:
                result_contour = cv2.approxPolyDP(single_contour, e * 0.02, closed=True)
                result.append(result_contour)
        self.external_contours = result
        return result

    def _assume_walls_shapes(self, image, contour):
        image = self._mask_for_single_block(image, contour)


        wall_contours, _ = cv2.findContours(image.copy(), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

        filtered_contours = []
        for single_contour in wall_contours:
            e = cv2.arcLength(single_contour, True)
            contour_area = cv2.contourArea(single_contour)
            if contour_area > 500:
                result_contour = cv2.approxPolyDP(single_contour, e * 0.02, closed=True)
                filtered_contours.append(result_contour)
        self.internal_contours.extend(filtered_contours)

        wall_shapes = []
        for single_contour in filtered_contours:
            converted = cd.convert_numpy_array_for_shape_detection(single_contour)
            wall_shapes.append(sd.detect_shape(converted))
        return wall_shapes

    def _assume_block_shape(self, wall_shapes):
        return 0

    def _mask_for_single_block(self, image, contour):
        mask = np.zeros(image.shape, np.uint8)
        cv2.fillPoly(mask, [contour], (255, 255, 255))
        mask = cv2.bitwise_and(image, mask)
        mask = cv2.cvtColor(mask, cv2.COLOR_BGR2HLS)
        mask = cv2.inRange(mask, (0, 30, 0), (180, 255, 255))
        self.masked_images.append(mask)
        return mask

    def detect_blocks(self, image, external_contour_auto_clear=True, internal_contour_auto_clear=True,
                      masked_images_auto_clear=True):
        external_contours = self._find_external_contours(image.copy())
        blocks = []
        for single_contour in external_contours:
            wall_shapes = self._assume_walls_shapes(image.copy(), single_contour)
            blocks.append(self._assume_block_shape(wall_shapes))

        if external_contour_auto_clear:
            self.external_contours = []
        if internal_contour_auto_clear:
            self.internal_contours = []
        if masked_images_auto_clear:
            self.masked_images = []

        return blocks

    def combine_masked_images(self):
        if len(self.masked_images) is 0:
            return None

        final_image = self.masked_images[0]
        for image in self.masked_images:
            final_image = cv2.bitwise_or(final_image, image)
        return final_image
