
'''
frame = cv2.imread('ObjectDetectionTest\\circle.jpg')
frame = cv2.resize(frame, None, fx=0.1, fy=0.1, interpolation=cv2.INTER_AREA)
shape = od.detect(od.Color.BLUE, frame)
cv2.drawContours(frame, [shape], -1, (255, 255, 255), 3)
cv2.imshow('Original', frame)
cv2.waitKey(0)
print sd.detect_shape(shape)
'''

from main.HTTPServer import HTTPServer

s = HTTPServer()
s.run()