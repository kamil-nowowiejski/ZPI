"""Main loop and logic of agent"""
import cv2
import logger as log
from Agent.serwer import Serv
from agent import Agent, Sensor
from move import Move
from time import sleep
from TCPConnections import TCPAgent
from resources import ares
import random


class Main:
    stop = [False]
    debug_tcp = True
    debug_db = True
    debug_arduino = True
    # setting stop value to [True] stops agent, debug values enable/disable debug messages

    def __init__(self):
        self.server = TCPAgent(self)
        self.move = Move()
        self.camera_manager = None

    def _setup(self):
        """Pre-loop actions"""
        # sensors = []
        # for sensor in ares('agent_info\\sensors'):
        #    sensors.append(Sensor(sensor['name'], sensor['accuracy'], sensor['unit_type'], sensor['type']))
        # log.agent_registration(Agent(ares('agent_info\\id'), ares('agent_info\\name'), ares('agent_info\\description'),
        #                             ares('agent_info\\type'), sensors))
        self.move.connect()
        self.server.start()
        timeouts = 0
        while not self.server.connected and timeouts < 10:
            timeouts += 1
            sleep(1)
        if timeouts >= 10:
            self.stop[0] = True

    def _clean(self):
        """Post-loop actions"""
        self.move.close()
        self.server.stop()

    def _loop(self):
        """Main loop"""
        self.logic_on= False
        while not self.stop[0]:
            if self.logic_on:
                self.logic()
            else:
                sleep(1)
        sleep(10)

    def logic(self):
        while self.logic_on:
            cont = False

            sleep(2)
            # single step consists of:
            #   - checking for aruco
            #   - going to marker, looking for objects and turning away if found
            #   - executing step if marker not found
            #   - going to next step if everything ok
            #   - starting loop from beginning after observing marker or encountering error
            #   - exiting loop is stuck
            self.aruco()
            if self.stop[0]:
                break
            self.server.has_aruco = False
            if self.server.aruco is not None:
                if self.move.drive_to_marker(self.server.aruco[0], self.server.aruco[1]):
                    self.observe()
                    self.move.turn(135)
                continue
            self.stop[0], cont = self.move.go(33)
            if self.stop[0]:
                break
            if cont:
                continue

            self.aruco()
            if self.stop[0]:
                break
            self.server.has_aruco = False
            if self.server.aruco is not None:
                if self.move.drive_to_marker(self.server.aruco[0], self.server.aruco[1]):
                    self.observe()
                    self.move.turn(135)
                continue
            self.stop[0], cont = self.move.turn(66)
            if self.stop[0]:
                break
            if cont:
                continue

            self.aruco()
            if self.stop[0]:
                break
            self.server.has_aruco = False
            if self.server.aruco is not None:
                if self.move.drive_to_marker(self.server.aruco[0], self.server.aruco[1]):
                    self.observe()
                    self.move.turn(135)
                continue
            self.stop[0], cont = self.move.turn(-132)
            if self.stop[0]:
                break
            if cont:
                continue

            self.aruco()
            if self.stop[0]:
                break
            self.server.has_aruco = False
            if self.server.aruco is not None:
                if self.move.drive_to_marker(self.server.aruco[0], self.server.aruco[1]):
                    self.observe()
                    self.move.turn(135)
                continue
            self.stop[0], cont = self.move.turn(66)
            if self.stop[0]:
                break
            if cont:
                continue

            self.stop[0], cont = self.move.turn(random.randint(-180, 180))
            if self.stop[0]:
                break
            if cont:
                continue

    def observe(self):
        """Take picture and send to server to extract objects"""
        self.camera_manager = cv2.VideoCapture(0)
        _, image = self.camera_manager.read()
        self.camera_manager.release()
        self.server.process_image(image)

    def aruco(self):
        """Take picture, send to server to extract aruco data and wait for response"""
        self.camera_manager = cv2.VideoCapture(0)
        _, image = self.camera_manager.read()
        self.camera_manager.release()
        self.server.find_aruco(image)
        timeouts = 0
        # while not self.server.has_aruco and timeouts < 10:
        #    timeouts += 1
        #    sleep(1)
        # if timeouts >= 10:
        #    self.stop[0] = True
        while not self.server.received_aruco_answer and not self.stop[0]:
            sleep(1)
        self.server.received_aruco_answer = False

    def run(self):
        """start agent (use start_agent.py)"""
        self._setup()
        server = Serv(self.move, self)
        self._loop()
        self._clean()
