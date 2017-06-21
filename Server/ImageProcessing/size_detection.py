import cv2
import math
import numpy as np
from Agent.resources import ares
from Server.enums import Size


def assume_size_from_contour(distance, contour, image_resolution, h_fov=None, v_fov=None):
    """
    Assumes width and height of object and discretizes its values
    :param distance: distance from objects scene - this value should be read from sensor
    :param contour: contour of object which size is calculated
    :param image_resolution: resolution of camera image
    :param h_fov: horizontal field of view of agent's camera; this value should be assigned in agent.yaml
    :param v_fov: vertical field of view of agent's camera; this value should be assigned in agent.yaml
    :return: tuple representing discrete values of width and height of object
    """
    if distance is None or distance <= 0:
        return Size.NONE, Size.NONE
    box = cv2.minAreaRect(contour)
    box = cv2.boxPoints(box)
    box = np.int0(box)
    object_width_pixels = _euclidean_distance(box[0], box[1])
    object_height_pixels = _euclidean_distance(box[1], box[2])
    return assume_size(distance, (object_width_pixels, object_height_pixels), image_resolution, h_fov, v_fov)


def assume_size(distance, object_size_pixels, image_resolution, h_fov=None, v_fov=None):
    """
    Assumes width and height of object and discretizes its values
    :param distance: distance from objects scene - this value should be read from sensor
    :param object_size_pixels: tuple representing width and height of object in pixels
    :param image_resolution: resolution of camera image
    :param h_fov: horizontal field of view of agent's camera; this value should be assigned in agent.yaml
    :param v_fov: vertical field of view of agent's camera; this value should be assigned in agent.yaml
    :return: tuple representing discrete values of width and height of object
    """
    if h_fov is None:
        h_fov = ares('camera_info\\horizontal_field_of_view')
    if v_fov is None:
        v_fov = ares('camera_info\\vertical_field_of_view')

    horizontal_ratio = _calculate_pixel_per_metrics_ratio(distance, image_resolution[0], h_fov)
    vertical_ratio = _calculate_pixel_per_metrics_ratio(distance, image_resolution[1], v_fov)

    real_width = object_size_pixels[0] * horizontal_ratio
    real_height = object_size_pixels[1] * vertical_ratio

    discrete_width = _size_discretization(real_width)
    discrete_height = _size_discretization(real_height)

    return discrete_width, discrete_height


def _calculate_pixel_per_metrics_ratio(real_distance, resolution, fov):
    """
    Calculates pixel per metric ration
    :param real_distance: distance from objects scene - this value should be read from sensor
    :param resolution: resolution of camera image
    :param fov: camera field of view
    :return: pixel per metric ration
    """
    image_length_in_metrics = 2 * real_distance * math.sin(math.radians(fov / 2))
    return image_length_in_metrics / resolution


def _size_discretization(size):
    """
    Converts continuous values of size to discrete values
    :param size: continuous value of size
    :return: discrete value of size
    """
    tiny_bounds = ares('image_processing_params\\size_discretization\\tiny_bounds')
    small_bounds = ares('image_processing_params\\size_discretization\\small_bounds')
    medium_bounds = ares('image_processing_params\\size_discretization\\medium_bounds')
    big_bounds = ares('image_processing_params\\size_discretization\\big_bounds')
    if size is None:
        return Size.NONE
    if tiny_bounds[0] < size <= tiny_bounds[1]:
        return Size.TINY
    if small_bounds[0] < size <= small_bounds[1]:
        return Size.SMALL
    if medium_bounds[0] < size <= medium_bounds[1]:
        return Size.MEDIUM
    if big_bounds[0] < size <= big_bounds[1]:
        return Size.BIG
    if size > big_bounds[1]:
        return Size.LARGE


def _euclidean_distance(p_1, p_2):
    """
    Calculates euclidean distance between two points
    :param p_1: tuple with two members representing first point
    :param p_2: tuple with two members representing second point
    :return: euclidean distance of two given points
    """
    return math.sqrt(math.pow(p_1[0] - p_2[0], 2) + math.pow(p_1[1] - p_2[1], 2))
