import numpy as np
import cv2
import cv2.aruco as aruco
import matplotlib.pyplot as plt


'''
    drawMarker(...)
        drawMarker(dictionary, id, sidePixels[, img[, borderBits]]) -> img
'''
def scaleImage(img,scale):
    """
    scale cv2 image object by a given number.
    scale: percent as number, upscale for numbers >100
        downscale for numbers <100

    returns the resized image
    """
    scale_percent = 10 # percent of original size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    #resizing using "resampling using pixel area relation" default is "INTER_LINEAR"- a bilinear interpolation
    return cv2.resize(img, dim, interpolation = cv2.INTER_AREA) 

aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
frame=cv2.imread("images/markerPic.jpg")
#frame=cv2.imread("calibrationImages/IMG_20191210_183704.jpg")
gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
resized = scaleImage(gray,10)
parameters=cv2.aruco.DetectorParameters_create()
corners, ids, rejectedImgPoints = aruco.detectMarkers(resized, aruco_dict, parameters=parameters)
print(corners)


frame_markers = aruco.drawDetectedMarkers(resized.copy(), corners, ids)

#cv2.imshow('frame',frame_markers)
fig=plt.figure()
plt.imshow(frame_markers)
for i in range(len(ids)):
    c = corners[i][0]#corners is a list of lists, and the corner coordinatnes are in the first list
    #then we plot the mean x and y value of the corners though this wont actually be the center
    plt.plot([c[:, 0].mean()], [c[:, 1].mean()], "o", label = "id={0}".format(ids[i]))
plt.legend()
plt.show()

cv2.waitKey(0)
