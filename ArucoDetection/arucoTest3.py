import cv2
import Aruco_detectPosition as aruco

cap = cv2.VideoCapture(1)
x = aruco.MrkerDetector()
if x.b_setUp():
    while (True):
        ret, frame = cap.read()
        print x.detect(frame)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()