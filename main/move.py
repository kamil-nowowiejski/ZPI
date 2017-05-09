import serial
import json
from threading import Timer
from resources import res


def run_left(time=0):
    ser = serial.Serial(res('serial\\port'), res('serial\\speed'))
    ser.write(res('serial\\arduino\\run_left'))
    ser.close()
    if time > 0:
        Timer(time, stop()).start()


def run_right(time=0):
    ser = serial.Serial(res('serial\\port'), res('serial\\speed'))
    ser.write(res('serial\\arduino\\run_right'))
    ser.close()
    if time > 0:
        Timer(time, stop()).start()


def run(time=0):
    ser = serial.Serial(res('serial\\port'), res('serial\\speed'))
    ser.write(res('serial\\arduino\\run'))
    ser.close()
    if time > 0:
        Timer(time, stop()).start()


def stop():
    ser = serial.Serial(res('serial\\port'), res('serial\\speed'))
    ser.write(res('serial\\arduino\\stop'))
    line = ser.readline()
    data = json.loads(line)
    ser.close()
    return data['distance']


def turn(angle):
    ser = serial.Serial(res('serial\\port'), res('serial\\speed'))
    ser.write(res('serial\\arduino\\turn').replace('?', str(angle)))
    ser.close()


def run_distance(distance):
    ser = serial.Serial(res('serial\\port'), res('serial\\speed'))
    ser.write(res('serial\\arduino\\run_distance').replace('?', str(distance)))
    ser.close()


def set_speed(speed):
    ser = serial.Serial(res('serial\\port'), res('serial\\speed'))
    ser.write(res('serial\\arduino\\set_speed').replace('?', str(speed)))
    ser.close()
