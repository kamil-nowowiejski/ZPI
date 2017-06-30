"""Data model"""
import enums as enums


class Object:
    """Basic object class. Doesn't define any features."""

    def __init__(self, id, name=''):
        self.id = id
        self.name = name


class Shape(Object):
    """Shape object"""

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

    def __str__(self):
        result = 'Shape: ' + self.color.name + ' ' + self.type.name + ' ' + self.width.name + ' ' + self.height.name +\
                 ' ' + self.pattern.name + ' ' + self.pattern_color.name + ' ' + str(len(self.symbols)) + '\n'
        for symbol in self.symbols:
            result += '\t' + str(symbol)
        return result

    def __repr__(self):
        result = '0|'
        if self.type is not None:
            result += '%d' % self.type.value
        result += '|'
        if self.width is not None:
            result += '%d' % self.width.value
        result += '|'
        if self.height is not None:
            result += '%d' % self.height.value
        result += '|'
        if self.color is not None:
            result += '%d' % self.color.value
        result += '|'
        if self.pattern is not None:
            result += '%d' % self.pattern.value
        result += '|'
        if self.pattern_color is not None:
            result += '%d' % self.pattern_color.value
        result += '|%d' % len(self.symbols)
        for symbol in self.symbols:
            result += '|%s' % repr(symbol)
        return result

    def _is_triangle(self):
        return self.type is enums.Shape.TRIANGLE or self.type is enums.Shape.EQUILATERAL_TRIANGLE or \
               self.type is enums.Shape.ISOSCELES_TRIANGLE

    @staticmethod
    def from_repr(string, offset=0):
        """create shape from string representation returned by repr()"""
        parts = string.split('|')
        obj_type = enums.Shape.NONE
        obj_width = enums.Size.NONE
        obj_height = enums.Size.NONE
        obj_color = enums.Color.NONE
        obj_pattern = enums.Pattern.NONE
        obj_pattern_color = enums.Color.NONE
        if parts[offset] != '':
            obj_type = enums.Shape(int(parts[offset]))
        if parts[offset + 1] != '':
            obj_width = enums.Size(int(parts[offset + 1]))
        if parts[offset + 2] != '':
            obj_height = enums.Size(int(parts[offset + 2]))
        if parts[offset + 3] != '':
            obj_color = enums.Color(int(parts[offset + 3]))
        if parts[offset + 4] != '':
            obj_pattern = enums.Pattern(int(parts[offset + 4]))
        if parts[offset + 5] != '':
            obj_pattern_color = enums.Color(int(parts[offset + 5]))
        symbol_count = int(parts[offset + 6])
        offset += 7
        obj_symbols = []
        for i in range(symbol_count):
            offset += 1
            obj, offset = Shape.from_repr(string, offset)
            obj_symbols.append(obj)
        return Shape(obj_type, obj_width, obj_height, obj_color, obj_pattern, obj_pattern_color, obj_symbols), offset


class CombinedObject(Object):
    """Object combined from adjacent shapes"""

    def __init__(self, type, width, height, parts=[], id=None):
        Object.__init__(self, id)
        self.type = type
        self.width = width
        self.height = height
        self.parts = parts

    def __str__(self):
        result = 'Combined: ' + self.type.name + ' ' + self.width.name + ' ' + self.height.name + ' ' +\
                 str(len(self.parts)) + '\n'
        for part in self.parts:
            result += '\t' + str(part)
        return result

    def __repr__(self):
        result = '1|'
        if self.type is not None:
            result += '%d' % self.type.value
        result += '|'
        if self.width is not None:
            result += '%d' % self.width.value
        result += '|'
        if self.height is not None:
            result += '%d' % self.height.value
        result += '|%d' % len(self.parts)
        for part in self.parts:
            result += '|%s' % repr(part)
        return result

    @staticmethod
    def from_repr(string, offset=0):
        """create shape from string representation returned by repr()"""
        parts = string.split('|')
        obj_type = enums.Shape.NONE
        obj_width = enums.Size.NONE
        obj_height = enums.Size.NONE
        if parts[offset] != '':
            obj_type = enums.Shape(int(parts[offset]))
        if parts[offset + 1] != '':
            obj_width = enums.Size(int(parts[offset + 1]))
        if parts[offset + 2] != '':
            obj_height = enums.Size(int(parts[offset + 2]))
        part_count = int(parts[offset + 3])
        offset += 4
        obj_parts = []
        for i in range(part_count):
            offset += 1
            obj, offset = Shape.from_repr(string, offset)
            obj_parts.append(obj)
        return CombinedObject(obj_type, obj_width, obj_height, obj_parts), offset
