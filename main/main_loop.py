from HTTPServer import HTTPServer
from move import Move
import cv2
import objects_detection as od
import database as db
import logger as log
from Agent import Agent
import time
from enums import MoveState


class Main:

    stop = [False]

    def __init__(self):
        self.server = HTTPServer()
        self.move = Move()
        self.camera_manager = cv2.VideoCapture()
        self.detector = od.ObjectDetector()

    def _setup(self):
        self.server.start()
        log.agent_registration(Agent(2, 'Andrzej', 'Agent Andrzej', 'agent', []))
        self.move.connect()

    def _clean(self):
        self.camera_manager.release()
        self.move.close()
        self.server.close()

    def _loop(self):
        while not self.stop[0]:
            self._observe()
            self._move()
            time.sleep(5)

    def _observe(self):
        if self.move.state is MoveState.IDLE:
            _, image = self.camera_manager.read()
            detected_objects = self.detector.detect_objects(image)
            for obj in detected_objects:
                db.insert(obj)

    def _move(self):
        if self.move.state is MoveState.IDLE:
            self.move.go()

    def run(self):
        self._setup()
        self._loop()
        self._clean()
