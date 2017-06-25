import cv2
import logger as log
from agent import Agent, Sensor
from time import sleep
from TCPConnections import TCPAgent
from resources import ares
from arduino import ArduinoServer
import random


class Main:
    stop = [False]

    def __init__(self):
        self.server = TCPAgent(self)
        self.move = ArduinoServer()
        self.camera_manager = cv2.VideoCapture(0)

    def _setup(self):
        # sensors = []
        # for sensor in ares('agent_info\\sensors'):
        #    sensors.append(Sensor(sensor['name'], sensor['accuracy'], sensor['unit_type'], sensor['type']))
        # log.agent_registration(Agent(ares('agent_info\\id'), ares('agent_info\\name'), ares('agent_info\\description'),
        #                             ares('agent_info\\type'), sensors))
        self.move.start()
        self.server.start()
        timeouts = 0
        while not self.server.connected and timeouts < 10:
            timeouts += 1
            sleep(1)
        if timeouts >= 10:
            self.stop[0] = True

    def _clean(self):
        self.camera_manager.release()
        self.move.close()
        self.server.stop()
        print 'server stopped'

    def _loop(self):
        sleep(2)
        event = None
        cont = False
        while not self.stop[0]:
            self.observe()
            if self.stop[0]:
                break
            self.server.has_aruco = False
            if self.server.aruco is not None:
                self.drive_to_marker(self.server.aruco[0], self.server.aruco[1])
                continue
            self.move.go_distance(33)
            self.move.queue = []
            while True:
                event = self.move.event
                if event is None:
                    sleep(1)
                    continue
                elif event == 'COMOK':
                    continue
                elif event.split('|')[0] == 'COMERR':
                    cont = True
                    break
                elif event.split('|')[0] == 'GOF':
                    dist = event.split('|')[1]
                    break
                elif event.split('|')[0] == 'OINR':
                    saved = self.obstacle()
                    if saved:
                        cont = True
                    else:
                        self.stop[0] = True
                    break
            if self.stop[0]:
                break
            if cont:
                continue

            self.observe()
            if self.stop[0]:
                break
            self.server.has_aruco = False
            if self.server.aruco is not None:
                self.drive_to_marker(self.server.aruco[0], self.server.aruco[1])
                break
            self.move.turn(67)
            sleep(3)

            self.observe()
            if self.stop[0]:
                break
            self.server.has_aruco = False
            if self.server.aruco is not None:
                self.drive_to_marker(self.server.aruco[0], self.server.aruco[1])
                break
            self.move.turn(-134)
            sleep(4)

            self.observe()
            if self.stop[0]:
                break
            self.server.has_aruco = False
            if self.server.aruco is not None:
                self.drive_to_marker(self.server.aruco[0], self.server.aruco[1])
                break
            self.move.turn(67)
            sleep(3)
            if self.stop[0]:
                break
            self.move.turn(random.randint(-180, 180))
        sleep(10)

    def observe(self):
        self.camera_manager = cv2.VideoCapture(0)
        _, image = self.camera_manager.read()
        self.server.process_image(image)
        self.camera_manager.release()
        timeouts = 0
        #while not self.server.has_aruco and timeouts < 10:
        #    timeouts += 1
        #    sleep(1)
        #if timeouts >= 10:
        #    self.stop[0] = True

        while not self.server.received_aruco_answer and not self.stop[0]:
            sleep(1)
        self.server.received_aruco_answer = False

    def obstacle(self):
        self.move.turn(135)
        while True:
            event = self.move.event
            if event is None:
                sleep(1)
                continue
            elif event == 'COMOK':
                continue
            elif event.split('|')[0] == 'COMERR':
                return False
            elif event.split('|')[0] == 'TURN':
                self.move.distance()
                continue
            elif event.split('|')[0] == 'DIST':
                dist = float(event.split('|')[1])
                if dist > 33:
                    return True
                else:
                    return False

    def drive_to_marker(self, rvec, tvec):
        print 'turn rvec'
        #self.move.turn(-rvec[1])
        sleep(5)
        print 'turn 1st 90'
        if rvec[1] > 0:
            self.move.turn(90 - rvec[1])
        else:
            self.move.turn(-90 - rvec[1])
        sleep(5)
        print 'go dist'
        #self.move.go_distance(tvec[0] * 100)
        self.move.go(3)
        sleep(7)
        print 'turn 2nd 90'
        if rvec[1] > 0:
            self.move.turn(-90)
        else:
            self.move.turn(90)
        sleep(5)
        #self.observe()
        self.server.has_aruco = False

    def run(self):
        self._setup()
        self._loop()
        self._clean()
