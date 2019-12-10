import numpy as np
import cv2
import cv2.aruco as aruco


'''
    drawMarker(...)
        drawMarker(dictionary, id, sidePixels[, img[, borderBits]]) -> img
'''

aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
print(aruco_dict)
# second parameter is id number
# last parameter is total image size
i=2
img = aruco.drawMarker(aruco_dict, i, 700)
cv2.imwrite("test_marker{0}.jpg".format(i), img)

cv2.imshow('frame',img)
cv2.waitKey(0)
cv2.destroyAllWindows()