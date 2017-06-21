import cv2
import numpy as np
from Server.enums import ColorSpace
from Agent.resources import ares


def percentage_of_bright_pixels(im, color_space):
    """
    Calculates percentage of bright pixels in the image
    :param im: image to be calculated
    :param color_space: color space in which image is represented,
                        color_space is id defined in class ColorSpace from enums.py
    :return: percentage of bright pixels in the image
    """
    if color_space is ColorSpace.BGR:
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2HLS)
    elif color_space is ColorSpace.HSV:
        gray = cv2.cvtColor(im, cv2.COLOR_HSV2BGR)
    elif color_space is ColorSpace.HSL:
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2HLS)
    else:
        return None

    gray = cv2.inRange(gray, (0, 160, 0), (179, 255, 255))
    number_of_pixels = gray.shape[0] * gray.shape[1]
    bright_pixels = cv2.countNonZero(gray)
    return float(bright_pixels) / float(number_of_pixels)


def merge_pictures(pictures, color_space, ignore_dark_images=False):
    """
    Give list of pictures merges them into one pixture.
    :param pictures: list of pictures to be merged
    :param color_space: color space of given pictures
    :param ignore_dark_images: if True, dark images are ignored
    :return: merged picture
    """
    if len(pictures) is 0:
        return None
    if len(pictures) is 1:
        return pictures[0]

    dark_pixels_percentage_border = ares('image_processing_params\\pictures_merge\\dark_pixels_percentage_border')
    final_picture = pictures[0]
    for picture in pictures:
        if ignore_dark_images and percentage_of_bright_pixels(picture, color_space) < dark_pixels_percentage_border:
            final_picture = cv2.addWeighted(final_picture, 0.5, picture, 0.5, 0)
    return final_picture


def remove_light_gray_background(im):
    """
    Removes light gray / white background from image
    :param im: image from which background is to be removed; image must be in BGR color space
    :return: image without light gray / white background
    """

    im = cv2.cvtColor(im, cv2.COLOR_BGR2HLS)
    mask = cv2.inRange(im, (0, 140, 0), (179, 255, 255))
    mask = cv2.bitwise_not(mask)
    im = cv2.bitwise_and(im, im, mask=mask)
    return cv2.cvtColor(im, cv2.COLOR_HLS2BGR)


def adjust_gamma(image, gamma=1.0):
    """
    Changes gamma channel of image
    :param image: image to be changed
    :param gamma: new gamma value
    :return: changed image
    """
    # build a lookup table mapping the pixel values [0, 255] to
    # their adjusted gamma values
    inv_gamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** inv_gamma) * 255
                    for i in np.arange(0, 256)]).astype("uint8")

    # apply gamma correction using the lookup table
    return cv2.LUT(image, table)


def color_quantization_using_k_means(im, k):
    """
    Averages colors of image
    :param im: image for quantization
    :param k: number of color after quantization
    :return: color quantizied image
    """
    img = im.reshape((-1, 3))
    img = np.float32(img)

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    # ret, label, center = cv2.kmeans(img, k, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    ret, label, center = cv2.kmeans(img, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    center = np.uint8(center)
    res = center[label.flatten()]
    res = res.reshape(im.shape)
    return res

