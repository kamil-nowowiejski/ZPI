import cv2
import main.ObjectDetection as od
import main.shape_detection as sd

frame = cv2.imread('ObjectDetectionTest\\test_img4.jpg')
frame = cv2.resize(frame, None, fx=0.25, fy=0.25, interpolation=cv2.INTER_AREA)
shape = od.detect(od.Color.RED, frame)
cv2.drawContours(frame, [shape], -1, (255, 255, 255), 3)
cv2.imshow('Original', frame)
cv2.waitKey(0)
print sd.detect_shape(shape)
