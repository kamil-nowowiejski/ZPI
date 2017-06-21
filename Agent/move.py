from threading import Thread
from time import sleep

import arduino
from enums import MoveState as State


class Move:

    def __init__(self):
        self._state = State.DISCONNECTED
        self.server = arduino.ArduinoServer()
        self._thread = Thread(target=self._go)
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
            thread = Thread(target=self._run)
            thread.start()
            self._state = State.MOVING

    def _run(self):
        self._drive_to_marker([None, 30], [1])

    def _go(self):
        self.server.turn(135)
        while not self._stop:
            if self.server.queue and 'COM41' in self.server.queue[-1]:
                break
            elif self.server.queue and self.server.queue[-1] == 'stuck':
                self._state = State.STUCK
                return
            sleep(1)
        if self._stop:
            self._state = State.IDLE
            return
        self.server.go_distance(1)
        while not self.server.queue and self._stop:
            if self.server.queue and 'COM41' in self.server.queue[-1]:
                break
            elif self.server.queue and self.server.queue[-1] == 'stuck':
                self._state = State.STUCK
                return
            sleep(1)
        self._state = State.IDLE

    def seek(self):
        self.server.turn(135)
        while not self._stop:
            if self.server.queue and 'COM41' in self.server.queue[-1]:
                break
            elif self.server.queue and self.server.queue[-1] == 'stuck':
                self._state = State.STUCK
                return
            sleep(1)
        if self._stop:
            self._state = State.IDLE
            return
        self.server.go_distance(1)
        while not self.server.queue and self._stop:
            if 'COM41' in self.server.queue[-1]:
                break
            elif self.server.queue and self.server.queue[-1] == 'stuck':
                self._state = State.STUCK
                return
            sleep(1)
        self._state = State.IDLE

    def close(self):
        self._stop = True
        self.server.stop()
        self.server.close()

    def drive_to_marker(self, rvec, tvec):
        self.server.turn(-rvec[1])
        while not self._stop:
            if self.server.queue and 'COM41' in self.server.queue[-1]:
                break
            elif self.server.queue and self.server.queue[-1] == 'stuck':
                self._state = State.STUCK
                return
            sleep(1)
        if self._stop:
            self._state = State.IDLE
            return
        if rvec[1] > 0:
            self.server.turn(90)
        else:
            self.server.turn(-90)
        while not self._stop:
            if self.server.queue and 'COM41' in self.server.queue[-1]:
                break
            elif self.server.queue and self.server.queue[-1] == 'stuck':
                self._state = State.STUCK
                return
            sleep(1)
        if self._stop:
            self._state = State.IDLE
            return
        self.server.go_distance(tvec[0] * 100)
        while not self._stop:
            if self.server.queue and 'COM41' in self.server.queue[-1]:
                break
            elif self.server.queue and self.server.queue[-1] == 'stuck':
                self._state = State.STUCK
                return
            sleep(1)
        if self._stop:
            self._state = State.IDLE
            return
        if rvec[1] > 0:
            self.server.turn(-90)
        else:
            self.server.turn(90)
        while not self.server.queue and self._stop:
            if 'COM41' in self.server.queue[-1]:
                break
            elif self.server.queue and self.server.queue[-1] == 'stuck':
                self._state = State.STUCK
                return
            sleep(1)
        self._state = State.IDLE

    def _drive_to_marker(self, rvec, tvec):
        self.server.turn(-rvec[1])
        if rvec[1] > 0:
            self.server.turn(90)
        else:
            self.server.turn(-90)

        self.server.go_distance(tvec[0] * 100)
        if rvec[1] > 0:
            self.server.turn(-90)
        else:
            self.server.turn(90)


    def _drive_to_marker_rec(self, rvec, tvec):
        self.server.turn(-rvec[1])
        if rvec[1] > 0:
            self.server.turn(90)
        else:
            self.server.turn(-90)

        self.server.go_distance(tvec[0] * 100)
        if rvec[1] > 0:
            self.server.turn(-90)
        else:
            self.server.turn(90)
        if(abs(rvec[1])>45): self._drive_to_marker_rec(rvec, tvec);


    def _drive_to_marker_rec_v2(self, rvec, tvec):
        self.server.turn(-rvec[1])
        if rvec[1] > 0:
            self.server.turn(90)
        else:
            self.server.turn(-90)

        self.server.go_distance(tvec[0] * 100)
        if rvec[1] > 0:
            self.server.turn(-90)
        else:
            self.server.turn(90)
        if(tvec[2]>1): self.server.go_distance(tvec[2]/2);
        if(abs(rvec[1])>45): self._drive_to_marker_rec(rvec, tvec);