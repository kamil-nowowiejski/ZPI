"""Data model"""


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

