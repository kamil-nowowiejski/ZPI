import cv2
import math
import numpy as np
from Agent.resources import ares
from Agent.enums import Size


def assume_size_from_contour(distance, contour, image_resolution, h_fov=None, v_fov=None):
    if distance is None or distance <= 0:
        return Size.NONE, Size.NONE
    box = cv2.minAreaRect(contour)
    box = cv2.boxPoints(box)
    box = np.int0(box)
    object_width_pixels = _euclidean_distance(box[0], box[1])
    object_height_pixels = _euclidean_distance(box[1], box[2])
    return assume_size(distance, (object_width_pixels, object_height_pixels), image_resolution, h_fov, v_fov)


def assume_size(distance, object_size_pixels, image_resolution, h_fov=None, v_fov=None):
    if h_fov is None:
        h_fov = ares('camera_info\\horizontal_field_of_view')
    if v_fov is None:
        v_fov = ares('camera_info\\vertical_field_of_view')

    horizontal_ratio = _calculate_pixel_per_metrics_ration(distance, image_resolution[0], h_fov)
    vertical_ratio = _calculate_pixel_per_metrics_ration(distance, image_resolution[1], v_fov)

    real_width = object_size_pixels[0] * horizontal_ratio
    real_height = object_size_pixels[1] * vertical_ratio

    discrete_width = _size_discretization(real_width)
    discrete_height = _size_discretization(real_height)

    return discrete_width, discrete_height


def _calculate_pixel_per_metrics_ration(real_distance, resolution, fov):
    image_length_in_metrics = 2 * real_distance * math.sin(math.radians(fov / 2))
    return image_length_in_metrics / resolution


def _size_discretization(size):
    if size is None:
        return Size.NONE
    if 0 < size <= 3:
        return Size.TINY
    if 3 < size <= 6:
        return Size.SMALL
    if 6 < size <= 9:
        return Size.MEDIUM
    if 9 < size <= 12:
        return Size.BIG
    if size > 12:
        return Size.LARGE


def _euclidean_distance(p_1, p_2):
    return math.sqrt(math.pow(p_1[0] - p_2[0], 2) + math.pow(p_1[1] - p_2[1], 2))
