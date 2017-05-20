import cv2

import Agent.ImageProcessing.pictures_transformations as pm

capture = cv2.VideoCapture(0)
for _ in range(0,50):
    capture.read()

while True:
    pictures = []
    for _ in range(1,10):
        _, img = capture.read()
        pictures.append(img)
    final = pm.merge_pictures(pictures)

    cv2.imshow('dsafa', final)
    cv2.waitKey(1)
