import cv2
import Agent.ImageProcessing.pattern_recognition as pr
from Agent.enums import Pattern


def test_find_pattern_vertical_lines():
    img = cv2.imread('images/pattern_rec_vert_lines.bmp')
    assert pr.find_pattern(img)[0] is Pattern.VERTICAL_LINES


def test_find_pattern_horizontal_lines():
    img = cv2.imread('images/pattern_rec_hor_lines.bmp')
    assert pr.find_pattern(img)[0] is Pattern.HORIZONTAL_LINES


def test_find_pattern_left_inclined_lines():
    img = cv2.imread('images/pattern_rec_left_inc_lines.bmp')
    assert pr.find_pattern(img)[0] is Pattern.LEFT_INCLINED_LINES


def test_find_pattern_right_inclined_lines():
    img = cv2.imread('images/pattern_rec_right_inc_lines.bmp')
    assert pr.find_pattern(img)[0] is Pattern.RIGHT_INCLINED_LINES


def test_find_pattern_grid():
    img = cv2.imread('images/pattern_rec_grid.bmp')
    assert pr.find_pattern(img)[0] is Pattern.GRID


def test_find_pattern_inclined_grid():
    img = cv2.imread('images/pattern_rec_inc_grid.bmp')
    assert pr.find_pattern(img)[0] is Pattern.INCLINED_GRID

