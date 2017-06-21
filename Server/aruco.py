import cv2.aruco as aruco
import yaml
import numpy as np
import math
import cv2
import numpy


class MarkerDetector:

    def __init__(self):
        self.markerSize = 0.05
        self._camera_matrix = None
        self._dist_coeffs = None
        self._aruco_dict = None
        self._parameters = None
        self.set_up()

    def set_up(self):
        calibration_path = "Resources/calibration_raspberry.yaml"
        try:
            calibration_file = open(calibration_path, "r")
            yml = yaml.load(calibration_file)
            self._camera_matrix = numpy.asanyarray(yml.get("camera_matrix"))
            self._dist_coeffs = numpy.asanyarray(yml.get("dist_coeff"))
            self._aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
            self._parameters = aruco.DetectorParameters_create()
            return True
        except:
            return False

    def detect(self, image):
        corners, ids, rejectedImgPoints = aruco.detectMarkers(image, self._aruco_dict, parameters=self._parameters)
        if corners:
            rvecs, tvecs, objectPoints = aruco.estimatePoseSingleMarkers(corners, self.markerSize, cameraMatrix=self._camera_matrix, distCoeffs=self._dist_coeffs)
            for x in range(0, len(rvecs)):
                rvecs[x] = self._convert_rot_matrix_to_degrees(rvecs[x])
            return rvecs[0], tvecs[0]
        else: return None, None

    def _convert_rot_matrix_to_degrees(self, rvec):

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