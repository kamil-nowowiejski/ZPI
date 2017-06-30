"""Communication with arduino"""
import serial
from threading import Timer
from threading import Thread
from time import sleep
from resources import res
import main_loop


class ArduinoServer:
    """Server maintaining connection with arduino"""

    def __init__(self):
        self._thread = Thread(target=self.run)
        self._stop = False
        self._serial = serial.Serial(res('serial\\port'), res('serial\\speed'))
        self.queue = []

    @property
    def running(self):
        """Check if server is running"""
        return self._thread.isAlive()

    @property
    def open(self):
        """Check if serial port is open"""
        return self._serial.isOpen()

    @property
    def event(self):
        """Return oldest message from arduino and remove it from queue or return None if there is no message"""
        if len(self.queue) == 0:
            return None
        else:
            return self.queue.pop(0)

    def end(self):
        """stop server (use close())"""
        self._stop = True

    def close(self):
        """stop server and close serial port"""
        self.end()
        if self.running:
            self._thread.join()
        self._serial.close()

    def start(self):
        """Start server"""
        if self.running:
            self.end()
            self._thread.join()
        self._thread = Thread(target=self.run)
        self._thread.start()

    def run(self):
        """Main loop of server polling messages from arduino"""
        while not self._stop:
            if self._serial.inWaiting() > 0:
                data = self._serial.readline()
                self.queue.append(data)
                if main_loop.Main.debug_arduino:
                    print '[INO] >> %s' % data
            sleep(1)

    def _send(self, message):
        """send message to arduino"""
        self._serial.write(message)
        if main_loop.Main.debug_arduino:
            print '[INO] << %s' % message

    def go(self, time=0):
        """Agent drives forward for specified number of seconds. If time not specified agent drives until stopped"""
        self._send(res('serial\\arduino\\run'))
        if time > 0:
            Timer(time, self.stop).start()

    def stop(self):
        """Stop agent"""
        self._send(res('serial\\arduino\\stop'))

    def turn(self, angle):
        """Turn agent right if angle is positive or left if angle is negative"""
        self._send(res('serial\\arduino\\turn').replace('?', str(angle * 1.6)))

    def go_distance(self, distance):
        """Agent drives specified number of centimeters"""
        self._send(res('serial\\arduino\\run_distance').replace('?', str(distance)))

    # set_speed is broken on arduino, if you want to change speed from default you have to do it in arduino
    # def set_speed(self, speed):
    #     self._serial.send(res('serial\\arduino\\set_speed').replace('?', str(speed)))

    def distance(self):
        """arduino will return distance to obstacle from detectors"""
        self._send(res('serial\\arduino\\distance'))
