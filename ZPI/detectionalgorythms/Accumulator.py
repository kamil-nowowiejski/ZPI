__author__ = 'kosto'

import numpy as np
import math
import cv2
import copy


class Accumulator:
    log = []

    counter = 0
    max_counter = 10

    center_offset_pixels = 10
    minimum_ocurrences_factor = 4

    def __init__(self, center_pixel_offset = 20, max_counter = 20):
        self.center_offset_pixels =center_pixel_offset
        self.max_counter = max_counter

    def filterOut(self):
        i=0
        new_log = []
        while i < len(self.log):
            if(len(self.log[i]["shapes"]) > self.max_counter / self.minimum_ocurrences_factor):
                new_log.append(self.log[i])
            i+=1
        self.log = new_log

    def drawDetectedOntoMat(self, mat):
        for single_detected_shape in self.log:
            y=-1
            shape = single_detected_shape["shapes"][0]
            while y < (len(shape) -1):
                #cv2.line(mat, (shape[y][0][0], shape[y][0][1]), (shape[y+1][0][0], shape[y+1][0][1]),single_detected_shape["color"], 3)
                cv2.line(mat, (shape[y][0][0], shape[y][0][1]), (shape[y+1][0][0], shape[y+1][0][1]),(0,0,255), 3)
                y+=1


    def newFrame(self, mat):
        if(self.counter > self.max_counter):
            self.filterOut()
            dets = copy.deepcopy(self.log)
            self.counter = 0
            self.drawDetectedOntoMat(mat)

            y=0
            self.log = []
            return dets
        else:
            self.counter += 1
            return False

    def getCenter(self,shape):
        x=0
        y=0
        for point in shape:
            x+= point[0][0]
            y+= point[0][1]
        x = x / len(shape)
        y = y / len(shape)
        return x, y

    def getDist(self,p1, p2):
        return math.sqrt(math.pow(p2[0] - p1[0], 2) + math.pow(p2[1]-p1[1], 2))

    def isSameShape(self, shape1, shape2):
        center1 = np.array(self.getCenter(shape1))
        center2 = np.array(self.getCenter(shape2))
        if(shape1.size != shape2.size):
            return False
        if(self.getDist(center1, center2) < self.center_offset_pixels):
            return True
        else:
            return False

    def addShape(self, shape, colour):
        i = 0
        added = False
        while(i < len(self.log)):
            if(self.isSameShape(self.log[i]["shapes"][0], shape)):
                self.log[i]["shapes"].append(shape)
                added = True
            i+=1
        if not added:
            new_class_obejct = {}
            new_class_obejct["shapes"] = []
            new_class_obejct["shapes"].append(shape)
            new_class_obejct["size"] = shape.size / 2
            new_class_obejct["center"] = self.getCenter(shape)
            new_class_obejct["color"] = colour
            self.log.append(new_class_obejct)
