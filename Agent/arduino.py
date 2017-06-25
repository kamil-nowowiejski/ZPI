import serial
import json
from threading import Timer
from threading import Thread
from time import sleep
from resources import res


class ArduinoServer:

    def __init__(self):
        self._thread = Thread(target=self.run)
        self._stop = False
        self._serial = serial.Serial(res('serial\\port'), res('serial\\speed'))
        self.queue = []

    @property
    def running(self):
        return self._thread.isAlive()

    @property
    def open(self):
        return self._serial.isOpen()

    @property
    def event(self):
        if len(self.queue) == 0:
            return None
        else:
            return self.queue.pop(0)

    def end(self):
        self._stop = True

    def close(self):
        self.end()
        if self.running:
            self._thread.join()
        self._serial.close()

    def start(self):
        if self.running:
            self.end()
            self._thread.join()
        self._thread = Thread(target=self.run)
        self._thread.start()

    def run(self):
        while not self._stop:
            if self._serial.inWaiting() > 0:
                data = self._serial.readline()
                self.queue.append(data)
                print 'arduino: %s' % data
            sleep(1)

    def go(self, time=0):
        self._serial.write(res('serial\\arduino\\run'))
        if time > 0:
            Timer(time, self.stop).start()

    def stop(self):
        self._serial.write(res('serial\\arduino\\stop'))

    def turn(self, angle):
        self._serial.write(res('serial\\arduino\\turn').replace('?', str(angle)))

    def go_distance(self, distance):
        self._serial.write(res('serial\\arduino\\run_distance').replace('?', str(distance)))

    # def set_speed(self, speed):
    #     self._serial.write(res('serial\\arduino\\set_speed').replace('?', str(speed)))

    def distance(self):
        self._serial.write(res('serial\\arduino\\distance'))
