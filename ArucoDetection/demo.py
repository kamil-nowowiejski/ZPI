import cv2
import cv2.aruco as aruco
import yaml
import numpy

'''
przyklad mozliwosci aruco, przy pokazniu marker.jpg, zaznacza znacznik i rysuje osie
'''

cap = cv2.VideoCapture(1)
i=0;


calibrationFile = "calibration.yaml"

plik = open(calibrationFile, "r")
myYaml = yaml.load(plik)
camera_matrix =numpy.asanyarray(myYaml.get("camera_matrix"))
dist_coeffs =numpy.asanyarray(myYaml.get("dist_coeff"))



rvecs = None
tvecs = None
i=0
while (True):
    i=i+1
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, gray = cv2.threshold(gray,50,255,cv2.THRESH_BINARY)
    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
    parameters = aruco.DetectorParameters_create()

    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

    if corners :
        aruco.drawDetectedMarkers(gray, corners, borderColor=(0,240,123))
        rvecs, tvecs, objectPoints =  aruco.estimatePoseSingleMarkers(corners, 0.05, cameraMatrix=camera_matrix, distCoeffs=dist_coeffs)
        if i%10==0:
            print (str(round(tvecs[0][0][0], 1))+" "+str(round(tvecs[0][0][1], 2))+" "+str(round(tvecs[0][0][2], 1)))
    if(rvecs!=None):
        aruco.drawAxis(image=frame,cameraMatrix=camera_matrix, distCoeffs=dist_coeffs, rvec=rvecs, tvec=tvecs, length=0.1)



    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()