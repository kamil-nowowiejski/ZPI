import cv2.aruco as aruco
import yaml

import numpy


class MrkerDetector:

    markerSize = 0.05
    camera_matrix = None
    dist_coeffs = None
    aruco_dict = None
    parameters = None

    def b_setUp(self):
        calibrationFile = "calibration.yaml"

        try:
            plik = open(calibrationFile, "r")
            myYaml = yaml.load(plik)
            self.camera_matrix = numpy.asanyarray(myYaml.get("camera_matrix"))
            self.dist_coeffs = numpy.asanyarray(myYaml.get("dist_coeff"))
            self.aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
            self.parameters = aruco.DetectorParameters_create()
            return True
        except:
            return False

    def detect(self, image):
        corners, ids, rejectedImgPoints = aruco.detectMarkers(image, self.aruco_dict, parameters=self.parameters)
        if corners:
            rvecs, tvecs, objectPoints = aruco.estimatePoseSingleMarkers(corners, self.markerSize, cameraMatrix=self.camera_matrix,distCoeffs=self.dist_coeffs)
            return rvecs, tvecs
        else: return None, None