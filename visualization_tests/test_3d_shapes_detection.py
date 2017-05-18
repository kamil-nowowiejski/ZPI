'''
1. convert to hsl image
2. range - (0,0,0) - (180,50,255)
3. find external contour
4. mask this contour
5. you are left with walls of single block
6. assume shape of every wall
7. assume shape of 3d block
'''

import cv2

import main.ImageProcessing.block_detection as bd

capture = cv2.VideoCapture(1)

for _ in range(1, 25):
    capture.read()

detector = bd.BlockDetector()

while True:
    _, img = capture.read()
    detector.detect_blocks(img, external_contour_auto_clear=False, internal_contour_auto_clear=False, masked_images_auto_clear=False)

    cv2.drawContours(img, detector.external_contours, -1, (0, 255, 0), 2)
    cv2.drawContours(img, detector.internal_contours, -1, (0, 255, 255), 1)

    cv2.imshow('original', img)
    cv2.waitKey(1)
    cv2.imshow('masked', detector.combine_masked_images())
    cv2.waitKey(1)

    print len(detector.masked_images)

    detector.external_contours = []
    detector.internal_contours = []
    detector.masked_images = []