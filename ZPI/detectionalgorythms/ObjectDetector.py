# -*- coding: utf-8 -*-
import cv2
import numpy as np

from ZPI.detectionalgorythms.Accumulator import Accumulator
import CornerDetector as cd

class ObjectDetector:

    last_detected_shapes = []
    last_detected_countours = []
    last_mean_colors = []
    logger = None
    acu = None

    def __init__(self):

        self.acu = Accumulator()
        return


    def getDetectedObjects(self, mat):
        gray = cv2.cvtColor(mat, cv2.COLOR_BGR2GRAY)
        img_filt = cv2.medianBlur(gray, 5)

        img_th = cv2.Canny(img_filt, 30,40)
        kernel = np.ones((2, 2), np.uint8)
        img_th = cv2.dilate(img_th, None, iterations=1)
        img_th = cv2.erode(img_th, None, iterations=1)
        img_th = cv2.dilate(img_th, kernel, iterations=1)

        cv2.imshow('canny first', img_th)
        cv2.waitKey(1)

        height, width, depth = mat.shape
        contours, hierarchy = cv2.findContours(img_th, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        self.last_detected_shapes = []
        self.last_detected_countours = []
        self.last_mean_colors = []
        cnt=0
        for single_contour in contours:

            e = cv2.arcLength(single_contour, True)
            shape = cv2.approxPolyDP(single_contour, e * 0.02 , closed=True)
            if cv2.contourArea(single_contour) < 500 or cv2.isContourConvex(single_contour):
                continue
            self.last_detected_shapes.insert(cnt,shape)
            self.last_detected_countours.insert(cnt,single_contour)
            cnt += 1

        i = 0
        for h,cnt in enumerate(self.last_detected_countours):
            mask = np.zeros(gray.shape,np.uint8)
            cv2.drawContours(mask,[cnt],0,255,-1)
            mean = cv2.mean(mat,mask = mask)
            self.last_mean_colors.insert(i, mean)
            i += 1
        return True

    def run(self, mat):
        while True:
            #mat = self.cm.getNextFrame()
            #mat = cv2.imread("IMG2.png")
            if not self.getDetectedObjects(mat):
                return

            i=0
            for shape in self.last_detected_shapes:
                self.acu.addShape(shape, self.last_mean_colors[i])
                i+=1
            ret = self.acu.newFrame(mat)

            if(ret != False):
                cv2.imshow("Object Detector", mat)
                cv2.waitKey(1)
                return ret
            else:
                continue
