import cv2

import Agent.ImageProcessing.multi_level_detection as mld

pattern = cv2.imread('knife_handle.jpg')
scene = cv2.imread('knife_desk.jpg')
mld.match_pattern(scene, pattern)