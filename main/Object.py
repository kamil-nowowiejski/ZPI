from enum import Enum


class Size(Enum):
    SMALL = 1
    MEDIUM = 2
    BIG = 4


class Color(Enum):
    RED = 1
    ORANGE = 2
    YELLOW = 4
    GREEN = 8
    BLUE = 16
    VIOLET = 32


class Object:

    def __init__(self, id):
        self.id = id


class Shape(Object):

    def __init__(self, type, height, width, color, symbols=[], id=None):
        Object.__init__(self, id)
        self.type = type
        self.height = height
        self.width = width
        self.color = color
        self.symbols = symbols
