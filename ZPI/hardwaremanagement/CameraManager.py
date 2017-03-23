# -*- coding: utf-8 -*-
import cv2
import numpy as np
# Klasa do obslugi lokalnie podlaczonej i już skonfigurowanej kamery.
# 2014 konstanty.karagiorgis@pwr.edu.pl

class CameraManager:

    capture = None

    # Konstruktor nawiazuje polaczenie z kamera

    def __init__(self):
        try:
            self.initialize()
        except ValueError:
            raise "Device is busy"

    def initialize(self):
        self.capture = cv2.VideoCapture(0)

    def deinitialize(self):
        self.capture.release()

    # Klatki sa ukladane w kolejce. Jesli system nie wyrabia z przetwarzaniem klatek (przetworzenie i wyswietlenie
    # wynikow zajmuje mu więcej czasu niż kamerze na pobranie nastepnej klatki), a chcemy pobrac zawszę najswiezsza
    # klatke, nalezy wykonać metode reset
    def getNextFrame(self):
         try:
            ret, frame = self.capture.read()
            return frame
         except ValueError:
            raise "Error in getting frame"


    def reset(self):
        self.deinitialize()
        self.initialize()
