import cv2
import Agent.ImageProcessing.pattern_recognition as pr
from Agent.enums import Pattern, Color


def test_find_pattern_vertical_lines():
    img = cv2.imread('images/pattern_rec_vert_lines.bmp')
    pattern, pattern_color = pr.find_pattern(img)
    assert pattern is Pattern.VERTICAL_LINES
    assert pattern_color is Color.GREEN


def test_find_pattern_horizontal_lines():
    img = cv2.imread('images/pattern_rec_hor_lines.bmp')
    pattern, pattern_color = pr.find_pattern(img)
    assert pattern is Pattern.HORIZONTAL_LINES
    assert pattern_color is Color.RED


def test_find_pattern_left_inclined_lines():
    img = cv2.imread('images/pattern_rec_left_inc_lines.bmp')
    pattern, pattern_color = pr.find_pattern(img)
    assert pattern is Pattern.LEFT_INCLINED_LINES
    assert pattern_color is Color.RED


def test_find_pattern_right_inclined_lines():
    img = cv2.imread('images/pattern_rec_right_inc_lines.bmp')
    pattern, pattern_color = pr.find_pattern(img)
    assert pattern is Pattern.RIGHT_INCLINED_LINES
    assert pattern_color is Color.YELLOW


def test_find_pattern_grid():
    img = cv2.imread('images/pattern_rec_grid.bmp')
    pattern, pattern_color = pr.find_pattern(img)
    assert pattern is Pattern.GRID
    assert pattern_color is Color.RED


def test_find_pattern_inclined_grid():
    img = cv2.imread('images/pattern_rec_inc_grid.bmp')
    pattern, pattern_color = pr.find_pattern(img)
    assert pattern is Pattern.INCLINED_GRID
    assert pattern_color is Color.GREEN


def test_find_pattern_no_pattern():
    img = cv2.imread('images/pattern_rec_no_pattern.bmp')
    pattern, pattern_color = pr.find_pattern(img)
    assert pattern is Pattern.NONE
    assert pattern_color is Color.NONE
