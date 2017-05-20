class Agent:

    def __init__(self, id, name, description, type, sensor_list):
        self.id = id
        self.name = name
        self.description = description
        self.type = type
        self.sensor_list = sensor_list


class Sensor:

    def __init__(self, name, accuracy, unit_type, type):
        self.name = name
        self.accuracy = accuracy
        self.unit_type = unit_type
        self.type = type
