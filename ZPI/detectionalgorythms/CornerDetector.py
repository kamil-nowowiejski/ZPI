import cv2
import numpy as np
from matplotlib import pyplot as plt


def harrisDetection(imgToScan):
    gray = cv2.cvtColor(imgToScan,cv2.COLOR_BGR2GRAY)

    gray = np.float32(gray)
    dst = cv2.cornerHarris(gray, 2, 3, 0.04)

    #result is dilated for marking the corners, not important
    dst = cv2.dilate(dst,None)

    # Threshold for an optimal value, it may vary depending on the image.
    imgToScan[dst>0.01*dst.max()]=[0,0,255]

    cv2.imshow('Harris Detection',imgToScan)
    cv2.waitKey(0)

def shiTomasiDetection(imgToScan, maxCorners=20, qualityLevel=0.01, minDistance=10):
    gray = cv2.cvtColor(imgToScan,cv2.COLOR_BGR2GRAY)

    corners = cv2.goodFeaturesToTrack(gray,maxCorners,qualityLevel,minDistance)
    corners = np.int0(corners)

    for i in corners:
        x,y = i.ravel()
        cv2.circle(imgToScan,(x,y),3,255,-1)

    plt.imshow(imgToScan)
    plt.show()

def siftDetection(imgToScan):
    gray = cv2.cvtColor(imgToScan, cv2.COLOR_BGR2GRAY)

    sift = cv2.SIFT()
    kp = sift.detect(gray, None)

    img = cv2.drawKeypoints(gray, kp)
    cv2.imshow("SIFT Detection", img)
    cv2.waitKey(0)


def fastDetection(imgToScan):
    # Initiate FAST object with default values
    fast = cv2.FastFeatureDetector()

    # find and draw the keypoints
    kp = fast.detect(imgToScan, None)
    img2 = cv2.drawKeypoints(imgToScan, kp, color=(255, 0, 0))

    # Print all default params
    print "Threshold: ", fast.getInt('threshold')
    print "nonmaxSuppression: ", fast.getBool('nonmaxSuppression')
#    print "neighborhood: ", fast.getInt('type')
    print "Total Keypoints with nonmaxSuppression: ", len(kp)

    cv2.imshow('FAST Destection TRUE', img2)
    cv2.waitKey(0)

    # Disable nonmaxSuppression
    fast.setBool('nonmaxSuppression', 0)
    kp = fast.detect(imgToScan, None)

    print "Total Keypoints without nonmaxSuppression: ", len(kp)

    img3 = cv2.drawKeypoints(imgToScan, kp, color=(255, 0, 0))

    cv2.imshow('FAST Detection FALSE', img3)
    cv2.waitKey(0)