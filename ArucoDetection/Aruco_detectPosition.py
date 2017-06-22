import cv2.aruco as aruco
import yaml
import numpy as np
import math
import cv2
import numpy


class MarkerDetector:
    '''
    klasa do wykrywania kodow aruco na zdjeciach, przed uzyciem nalezy ustawic b_setUp()
    '''

    markerSize = 0.05
    _camera_matrix = None
    _dist_coeffs = None
    _aruco_dict = None
    _parameters = None

    def b_setUp(self):

        '''
        pobranie danych z wymaganych plikow
        :return: 
        true jezeli pliki istnieja i maja wymagane dane, w przeciwnym wypadku false
        '''
        calibrationFile = "calibration_raspberry.yaml"

        try:
            plik = open(calibrationFile, "r")
            myYaml = yaml.load(plik)
            self._camera_matrix = numpy.asanyarray(myYaml.get("camera_matrix"))
            self._dist_coeffs = numpy.asanyarray(myYaml.get("dist_coeff"))
            self._aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
            self._parameters = aruco.DetectorParameters_create()
            return True
        except Exception as e:
            print e
            return False

    def detect(self, image):
        '''
        wykrycie znacznikow aruco, wyznaczenie ich katow i odleglosci na podanym obrazie
        :param image: obraz ze znacznikami
        :return: rvecs[] tablica, pierwszy wymiar oznacza znaczniki, pozostale 3 to poszczegolne katy pod jakimi znajduje sie dany znacznik
                tvecs[] tablica, pierwszy wymiar oznacza znaczniki, pozostale 3 to odleglosci znacznika w poszczegolnych osiach wzgledem kamery
        '''
        corners, ids, rejectedImgPoints = aruco.detectMarkers(image, self._aruco_dict, parameters=self._parameters)
        if corners:
            rvecs, tvecs, objectPoints = aruco.estimatePoseSingleMarkers(corners, self.markerSize, cameraMatrix=self._camera_matrix, distCoeffs=self._dist_coeffs)
            for x in range(0, len(rvecs)):
                rvecs[x] = self._convert_rot_matrix_to_degrees(rvecs[x])
            return rvecs[0], tvecs[0]
        else: return None, None

    def _convert_rot_matrix_to_degrees(self, rvec):
        '''
        przeksztalcenie katow podanych w przeksztalceniu rodrigueza na normalne katy
        :param rvec: tablica katow zwracana przez aruco
        :return: tablica normalnych katow
        '''

        rot_matrix = numpy.empty([3, 3])
        cv2.Rodrigues(rvec, rot_matrix, None)

        x_rot = math.atan2(rot_matrix[2][1], rot_matrix[2][2])
        y_rot = math.atan2(-rot_matrix[2][0], math.sqrt(math.pow(rot_matrix[2][1], 2) + math.pow(rot_matrix[2][2], 2)))
        z_rot = math.atan2(rot_matrix[1][0], rot_matrix[0][0])

        if x_rot > 0:
            x_rot = 180 - math.degrees(x_rot)
        else:
            x_rot = -180 - math.degrees(x_rot)
        return round(x_rot), round(math.degrees(y_rot)), round(math.degrees(z_rot))