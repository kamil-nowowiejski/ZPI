import numpy as np
import pytest
from main.shape_detection import _align_points
from main.shape_detection import detect_shape


def test__align_points():
    assert np.array_equal(_align_points(np.array([[3, 5]])), np.array([[0, 0]]))
    assert np.array_equal(_align_points(np.array([[-4, 100]])), np.array([[0, 0]]))
    assert np.array_equal(_align_points(np.array([[3, 8], [12, 1], [5, 5]])), np.array([[0, 7], [9, 0], [2, 4]]))
    assert np.array_equal(_align_points(np.array([[-3, -8], [-12, -1], [-5, -5]])), np.array([[9, 0], [0, 7], [7, 3]]))
    assert np.array_equal(_align_points(np.array([[9, 4], [-7, 2], [0, 3]])), np.array([[16, 2], [0, 0], [7, 1]]))


def test__under3_detection():
    assert detect_shape(np.array([[0, 0]])) == 'point'
    assert detect_shape(np.array([[7, 1]])) == 'point'
    with pytest.raises(ValueError):
        assert detect_shape(np.array([[]]))
    assert detect_shape((np.array([[0, 0], [0, 0]]))) == 'point'
    assert detect_shape((np.array([[3, 1], [9, 2]]))) == 'line'


def test__triangle_detection():
    assert detect_shape(np.array([[0, 0], [9, 0], [4.5, 7.794]])) == 'equilateral triangle'
    assert detect_shape(np.array([[0, 0], [3.464, -2], [3.464, 2]])) == 'equilateral triangle'
    assert detect_shape(np.array([[0, 0], [9, 0], [4.5, 10]])) == 'isosceles triangle'
    assert detect_shape(np.array([[0, 0], [3.464, -2], [2.482, 0.299]])) == 'isosceles triangle'
    assert detect_shape(np.array([[3, 8], [1, 0], [6, 6]])) == 'triangle'
    assert detect_shape(np.array([[-6, 3], [8, 9], [5, -2]])) == 'triangle'


def test__quadrilateral_detection():
    assert detect_shape(np.array([[0, 0], [0, 2], [2, 2], [2, 0]])) == 'square'
    assert detect_shape(np.array([[0, 0], [1.5, 2.598], [4.098, 1.092], [2.598, -1.5]])) == 'square'
    assert detect_shape(np.array([[0, 0], [0, 5], [2, 5], [2, 0]])) == 'rectangle'
    assert detect_shape(np.array([[0, 0], [4.145, 2.796], [3.027, 4.454], [-1.118, 1.658]])) == 'rectangle'
    assert detect_shape(np.array([[0, 0], [4, 2], [6, 6], [2, 4]])) == 'rhombus'
    assert detect_shape(np.array([[0, 0], [2.198, 3.895], [1.619, 8.329], [-0.579, 4.435]])) == 'rhombus'
    assert detect_shape(np.array([[0, 0], [0, 3], [2, 4], [2, 1]])) == 'parallelogram'
    assert detect_shape(np.array([[0, 0], [0.572, -2.945], [-1.2, -4.308], [-1.772, -1.363]])) == 'parallelogram'
    assert detect_shape(np.array([[0, 0], [6, 0], [5, 3], [1, 3]])) == 'trapezium'
    assert detect_shape(np.array([[0, 0], [-5.89, -1.145], [-4.336, -3.899], [-0.409, -3.136]])) == 'trapezium'
    assert detect_shape(np.array([[2, 0], [0, 4], [2, 5], [4, 4]])) == 'kite'
    assert detect_shape(np.array([[-0.313, -1.975], [4.938, -0.782], [3.638, -2.601], [4.313, -4.733]])) == 'kite'
    assert detect_shape(np.array([[1, 7], [3, 3], [4, 6], [8, 2]])) == 'quadrilateral'
    assert detect_shape(np.array([[7.3, -2.3], [8.3, 2.4], [-2, -3.1], [-5.8, 9.9]])) == 'quadrilateral'


def test__n_polygons_detection():
    assert detect_shape(np.array([[1, 5], [8, 3], [1, 9], [3, 3], [2, 9]])) == 'pentagon'
    assert detect_shape(np.array([[9, 3], [2, 4], [6, 6], [1, 5], [2, 0], [0, 8]])) == 'hexagon'
    assert detect_shape(np.array([[1, 5], [8, 3], [1, 9], [6, 6], [1, 5], [2, 0], [0, 8]])) == 'heptagon'
    assert detect_shape(np.array([[1, 9], [6, 6], [1, 5], [2, 0], [9, 3], [2, 4], [3, 3], [2, 9]])) == 'octagon'


def test__conics_detection():
    assert detect_shape(np.array(
        [[10, 0], [18, 1], [24, 7], [25, 18], [21, 23], [17, 25], [6, 24], [2, 20], [4, 4], [5, 3]])) == 'circle'
    assert detect_shape(np.array(
        [[2.7, 1.1], [-1.2, 8.2], [-9.1, 11.4], [-19.6, 8], [-22.8, 2.4], [-22.9, -2.1], [-17.7, -11.8], [-12.6, -14.1],
         [1.5, -6], [1.9, -4.7]])) == 'circle'
    # assert detect_shape(np.array(
    #   [[0, 23], [1, 20], [3, 15], [4, 13], [6, 11], [8, 8], [10, 7], [11, 6], [13, 4], [14, 4]])) == 'circle'
    assert detect_shape(np.array(
        [[7, 5], [16, 1], [36, 1], [54, 13], [49, 22], [33, 28], [18, 27], [5, 22], [0, 16], [0, 14]])) == 'ellipse'
    assert detect_shape(np.array(
        [[8.48, -1.41], [12.02, -10.60], [26.16, -24.75], [47.38, -28.99], [50.2, -19.09], [43.13, -3.53],
         [31.82, 6.36], [19.09, 12.02], [11.31, 11.31], [9.9, 9.9]])) == 'ellipse'
    assert detect_shape(
        np.array([[1, 9], [6, 6], [1, 5], [2, 0], [9, 3], [2, 4], [3, 3], [2, 9], [7, 2], [1, 11]])) == 'polygon'
    assert detect_shape(np.array(
        [[7.3, -2.3], [8.3, 2.4], [3.027, 4.454], [-1.118, 1.658], [3.464, -2], [2.482, 0.299], [0.572, -2.945],
         [-1.2, -4.308], [4.938, -0.782], [3.638, -2.601]])) == 'polygon'
