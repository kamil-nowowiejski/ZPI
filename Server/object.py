"""Data model"""
import enums as enums

class Object:

    def __init__(self, id, name=''):
        self.id = id
        self.name = name


class Shape(Object):

    def __init__(self, type, width, height, color, pattern, pattern_color, symbols=[], id=None):
        Object.__init__(self, id)
        self.type = type
        self.width = width
        self.height = height
        self.color = color
        self.pattern = pattern
        self.pattern_color = pattern_color
        self.symbols = symbols

    def features(self):
        feature = [0] * len(self.type.__objclass__)
        feature[self.type.value] = 1
        result = feature
        feature = [0] * len(self.height.__objclass__)
        feature[self.height.value] = 1
        result += feature
        feature = [0] * len(self.width.__objclass__)
        feature[self.width.value] = 1
        result += feature
        feature = [0] * len(self.color.__objclass__)
        feature[self.color.value] = 1
        result += feature
        for symbol in self.symbols:
            result += symbol.features()
        return result

    def quasi_equals(self, another):
        are_equal = (self.type == another.type) or (self._is_triangle() and another._is_triangle())
        are_equal = are_equal and self.color == another.color
        are_equal = are_equal and self.height == another.height
        are_equal = are_equal and self.width == another.width
        are_equal = are_equal and self.pattern == another.pattern
        are_equal = are_equal and self.pattern_color == another.pattern_color
        are_equal = are_equal and len(self.symbols) == len(self.symbols)
        if not are_equal:
            return False

        if len(self.symbols) != len(another.symbols):
            return False

        for i in range(0, len(self.symbols)):
            are_equal = are_equal and self.symbols[i].quasi_equals(another.symbols[i])
        return are_equal

    def to_string(self):
        result = 'Shape: ' + str(self.color) + ' ' + str(self.type) + ' ' + str(self.width) + ' ' + str(self.height) + ' ' + \
                 str(self.pattern) + str(self.pattern_color) + '\n'
        for symbol in self.symbols:
            result += '\t' + symbol.to_string()
        return result

    def _is_triangle(self):
        return self.type is enums.Shape.TRIANGLE or self.type is enums.Shape.EQUILATERAL_TRIANGLE or \
               self.type is enums.Shape.ISOSCELES_TRIANGLE


class CombinedObject(Object):

    def __init__(self, type, width, height, parts=[], id=None):
        Object.__init__(self, id)
        self.type = type
        self.width = width
        self.height = height
        self.parts = parts

    def to_string(self):
        result = 'Combined: ' + str(self.type) + ' ' + str(self.width) + ' ' + str(self.height) + ' ' + \
                 str(len(self.parts)) + '\n'
        for part in self.parts:
            result += '\t' + part.to_stirng()
        return result
