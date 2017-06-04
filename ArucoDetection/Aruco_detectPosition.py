import cv2.aruco as aruco
import yaml
import numpy.linalg.norm as norm
import numpy as np
import math

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


    def _rodrigues(self, rot_vec):
        theta = norm(rot_vec)
        rot_vec = rot_vec / theta

        cos_theta = math.cos(theta)
        cos_theta_matrix = np.ndarray([[cos_theta]])
        cos_theta_matrix = np.repeat(cos_theta_matrix, 3, axis=1)
        cos_theta_matrix = np.repeat(cos_theta_matrix, 3, axis=0)

        temp_r = np.array([rot_vec])
        temp_r = temp_r * np.transpose(temp_r)
        temp_r = temp_r * (1 - cos_theta)

        last_matrix = np.array([
            [0, -rot_vec[2], rot_vec[1]],
            [rot_vec[2], 0, -rot_vec[0]],
            [-rot_vec[1], rot_vec[0], 0]])
        last_matrix = math.sin(theta) * last_matrix

        return cos_theta_matrix + temp_r + last_matrix

        rodriguez_matrix = []
        x_rot = math.atan2(rodriguez_matrix[2][1], rodriguez_matrix[2][2])
        y_rot = math.atan2(-rodriguez_matrix[2][0], math.sqrt(math.pow(rodriguez_matrix[2][1], 2) + math.pow(rodriguez_matrix[2][2], 2)))
        z_rot = math.atan2(rodriguez_matrix[1][0], rodriguez_matrix[0][0])

