from move import Move
import cv2
import ImageProcessing.objects_detection as od
import database as db
import logger as log
from agent import Agent, Sensor
from time import sleep
from enums import MoveState
from TCPConnections import TCPAgent
from resources import ares
from Aruco_detectPosition import MarkerDetector


class Main:

    stop = [False]

    def __init__(self):
        #self.server = TCPAgent(self)
        self.move = Move()
        self.camera_manager = cv2.VideoCapture(0)
        self.detector = od.ObjectDetector()
        self.aruco_detector = MarkerDetector()

    def _setup(self):
        #self.server.start()
        #sensors = []
        #for sensor in ares('agent_info\\sensors'):
        #    sensors.append(Sensor(sensor['name'], sensor['accuracy'], sensor['unit_type'], sensor['type']))
        #log.agent_registration(Agent(ares('agent_info\\id'), ares('agent_info\\name'), ares('agent_info\\description'),
        #                             ares('agent_info\\type'), sensors))
        self.aruco_detector.b_setUp()
        self.move.connect()

    def _clean(self):
        self.camera_manager.release()
        self.move.close()
        #self.server.stop()

    def _loop(self):
        while not self.stop[0]:
            if self.move.state is MoveState.IDLE:
                _, image = self.camera_manager.read()
                detected_objects = self.detector.detect_objects(image)
                for obj in detected_objects:
                    db.insert(obj)
                rvec, tvec = self.aruco_detector.detect(image)
                if rvec is not None and tvec is not None:
                    self.move.drive_to_marker(rvec, tvec)
                else:
                    self.move.seek()
            else:
                sleep(1)
            #if self.server.autonomous:
            #    self._observe()
            #    self._move()
            #    sleep(5)
            #if self.server.feed:
            #    _, image = self.camera_manager.read()
            #    self.server.send_feed(image)
            #    sleep(0.2)

    def _observe(self):
        pass
        if self.move.state is MoveState.IDLE:
            _, image = self.camera_manager.read()
            detected_objects = self.detector.detect_objects(image)
            for obj in detected_objects:
                db.insert(obj)

    def _move(self):
        pass
        if self.move.state is MoveState.IDLE:
            self.move.go()

    def run(self):
        self._setup()
        self._loop()
        self._clean()
