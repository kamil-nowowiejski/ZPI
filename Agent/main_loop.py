from move import Move
import cv2
import ImageProcessing.objects_detection as od
import database as db
import logger as log
from agent import Agent, Sensor
from time import sleep
from enums import MoveState
from TCPConnections import TCPAgent


class Main:

    stop = [False]

    def __init__(self):
        self.server = TCPAgent(self)
        #self.move = Move()
        self.camera_manager = cv2.VideoCapture()
        self.detector = od.ObjectDetector()

    def _setup(self):
        self.server.start()
        log.agent_registration(Agent(2, 'Andrzej', 'Agent Andrzej', 'agent', [Sensor('s1', 0.1, 'm', 'type1')]))
        #self.move.connect()

    def _clean(self):
        self.camera_manager.release()
        #self.move.close()
        self.server.stop()

    def _loop(self):
        while not self.stop[0]:
            if self.server.autonomous:
                self._observe()
                #self._move()
                sleep(5)
            if self.server.feed:
                _, image = self.camera_manager.read()
                self.server.send_feed(image)
                sleep(0.2)

    def _observe(self):
        pass
        if self.move.state is MoveState.IDLE:
            _, image = self.camera_manager.read()
            detected_objects = self.detector.detect_objects(image)
            for obj in detected_objects:
                db.insert(obj)

    def _move(self):
        pass
        #if self.move.state is MoveState.IDLE:
        #    self.move.go()

    def run(self):
        self._setup()
        self._loop()
        self._clean()
