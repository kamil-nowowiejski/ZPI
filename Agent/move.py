from threading import Thread
from time import sleep

import arduino
from enums import MoveState as State


class Move:

    def __init__(self):
        self._state = State.DISCONNECTED
        self.server = arduino.ArduinoServer()
        self._thread = Thread(target=self._drive_to_marker(), args=[[None, 30], [1]])
        self._stop = False

    @property
    def has_events(self):
        return len(self.server.queue) > 0

    @property
    def state(self):
        return self._state

    def event(self):
        if self.has_events:
            return self.server.queue.pop(0)

    def connect(self):
        self.server.start()
        self._state = State.IDLE

    def go(self):
        if self._state is not State.DISCONNECTED:
            thread = Thread(target=self._drive_to_marker, args=[[None, 30], [1]])
            thread.start()
            self._state = State.MOVING

    def _go(self):
        self.server.turn(135)
        while not self._stop:
            if self.server.queue[-1] == 'stop':
                break
            elif self.server.queue[-1] == 'stuck':
                self._state = State.STUCK
                return
            sleep(1)
        if self._stop:
            self._state = State.IDLE
            return
        self.server.go_distance(1)
        while not self._stop:
            if self.server.queue[-1] == 'stop':
                break
            elif self.server.queue[-1] == 'stuck':
                self._state = State.STUCK
                return
            sleep(1)
        self._state = State.IDLE

    def close(self):
        self._stop = True
        self.server.stop()
        self.server.close()

    def _drive_to_marker(self, rvec, tvec):
        self.server.turn(-rvec[1])
        self.server.go_distance(tvec[0] * 100)
        if rvec[1] > 0:
            self.turn(90)
        else:
            self.turn(-90)
