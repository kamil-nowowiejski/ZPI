import cv2
import main.contour_detection as od
import main.shape_detection as sd
from main.Enums.Color import Color

frame = cv2.imread('images\\test_img5.jpg')
frame = cv2.resize(frame, None, fx=0.25, fy=0.25, interpolation=cv2.INTER_AREA)
shape = od.detect_contours(Color.RED, frame)
cv2.drawContours(frame, [shape], -1, (255, 255, 255), 3)
cv2.imshow('Original', frame)
cv2.waitKey(0)

x, y, w, h = cv2.boundingRect(shape)
crop_img = frame[y:y + h, x:x + w]
cv2.imshow('output', crop_img)
cv2.waitKey()

print sd.detect_shape(shape)

