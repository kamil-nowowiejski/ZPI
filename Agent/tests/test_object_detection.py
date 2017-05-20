import cv2
import Agent.ImageProcessing.objects_detection as od
from Agent.object import Shape
from Agent.enums import Color, Shape


def test_detect_object_red_rectangle_with_green_triangle():
    detector = od.ObjectDetector()
    frame = cv2.imread('tests/images/obj_det_red_rectangle.bmp')
    objects_list = detector.detect_objects(frame, auto_contour_clear=False, prepare_image_befor_detection=False)

    obj = None
    for x in objects_list:
        if x.color is Color.RED and x.type is Shape.RECTANGLE and len(x.symbols) is 1 and \
                        x.symbols[0].color is Color.GREEN and x.symbols[0].type is Shape.TRIANGLE:
            obj = x
            break
    assert obj is not None


def test_detect_object_blue_square_with_red_triangle_and_green_parallelogram():
    detector = od.ObjectDetector()
    frame = cv2.imread('tests/images/obj_det_blue_rectangle.bmp')
    objects_list = detector.detect_objects(frame, auto_contour_clear=False, prepare_image_befor_detection=False)
    obj = None
    for x in objects_list:
        if x.color is Color.BLUE and x.type is Shape.SQUARE and len(x.symbols) is 2:
            matched_symbols = 0
            for symbol in x.symbols:
                if (symbol.color is Color.RED and _is_triangle(symbol.type)) or \
                        (symbol.color is Color.GREEN and symbol.type is Shape.SQUARE):
                    matched_symbols += 1
            if matched_symbols is 2:
                obj = x
                break
    assert obj is not None


def test_detect_object_blue_pentagon_with_red_parallelogram():
    detector = od.ObjectDetector()
    frame = cv2.imread('tests/images/obj_det_blue_pentagon.bmp')
    objects_list = detector.detect_objects(frame, auto_contour_clear=False, prepare_image_befor_detection=False)

    obj = None
    for x in objects_list:
        if x.color is Color.BLUE and x.type is Shape.PENTAGON and len(x.symbols) is 1 and \
                        x.symbols[0].color is Color.RED and x.symbols[0].type is Shape.SQUARE:
            obj = x
            break
    assert obj is not None


def test_detect_object_green_triangle_with_blue_rectangle():
    detector = od.ObjectDetector()
    frame = cv2.imread('tests/images/obj_det_green_triangle.bmp')
    objects_list = detector.detect_objects(frame, auto_contour_clear=False, prepare_image_befor_detection=False)

    obj = None
    for x in objects_list:
        if x.color is Color.GREEN and _is_triangle(x.type) and len(x.symbols) is 1 and \
                        x.symbols[0].color is Color.BLUE and x.symbols[0].type is Shape.RECTANGLE:
            obj = x
            break
    assert obj is not None


def test_detect_object_all_objects():
    detector = od.ObjectDetector()
    frame = cv2.imread('tests/images/obj_det_all.jpg')
    objects_list = detector.detect_objects(frame, auto_contour_clear=False, prepare_image_befor_detection=False)

    obj = None
    for x in objects_list:
        if x.color is Color.RED and x.type is Shape.RECTANGLE and len(x.symbols) is 1 and \
                        x.symbols[0].color is Color.GREEN and x.symbols[0].type is Shape.TRIANGLE:
            obj = x
            break
    assert obj is not None

    obj = None
    for x in objects_list:
        if x.color is Color.BLUE and x.type is Shape.SQUARE and len(x.symbols) is 2:
            matched_symbols = 0
            for symbol in x.symbols:
                if (symbol.color is Color.RED and _is_triangle(symbol.type)) or \
                        (symbol.color is Color.GREEN and symbol.type is Shape.SQUARE):
                    matched_symbols += 1
            if matched_symbols is 2:
                obj = x
                break
    assert obj is not None

    obj = None
    for x in objects_list:
        if x.color is Color.BLUE and x.type is Shape.PENTAGON and len(x.symbols) is 1 and \
                        x.symbols[0].color is Color.RED and x.symbols[0].type is Shape.SQUARE:
            obj = x
            break
    assert obj is not None

    obj = None
    for x in objects_list:
        if x.color is Color.GREEN and _is_triangle(x.type) and len(x.symbols) is 1 and \
                        x.symbols[0].color is Color.BLUE and x.symbols[0].type is Shape.RECTANGLE:
            obj = x
            break
    assert obj is not None


def _is_triangle(shape):
    return shape is Shape.TRIANGLE or shape is Shape.EQUILATERAL_TRIANGLE or shape is Shape.ISOSCELES_TRIANGLE
