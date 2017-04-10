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


class Cuboid(Object):

    def __init__(self, height, width, depth, color, id=None):
        Object.__init__(self, id)
        self.height = height
        self.width = width
        self.depth = depth
        self.color = color


class Sphere(Object):

    def __init__(self, size, color, id=None):
        Object.__init__(self, id)
        self.size = size
        self.color = color
