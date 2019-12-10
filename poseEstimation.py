import numpy as np
import cv2,os
import cv2.aruco as aruco
import matplotlib.pyplot as plt
import matplotlib

def scaleImage(img,scale):
    """
    scale cv2 image object by a given number.
    scale: percent as number, upscale for numbers >100
        downscale for numbers <100

    returns the resized image
    """
    width = int(img.shape[1] * scale / 100)
    height = int(img.shape[0] * scale / 100)
    dim = (width, height)
    #resizing using "resampling using pixel area relation" default is "INTER_LINEAR"- a bilinear interpolation
    return cv2.resize(img, dim, interpolation = cv2.INTER_AREA) 

aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
# frame = cv2.imread("calibrationImages/IMG_20191210_183704.jpg")
#frame = cv2.imread("images/markerPic.jpg")
frame = cv2.imread("poseEstimationImages/room.jpg")
resized = scaleImage(frame,10)
gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
parameters =  aruco.DetectorParameters_create()
corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
#frame_markers = aruco.drawDetectedMarkers(resized.copy(), corners, ids)


# conn = np.array([0, 1, 2, 3, 0])
# plt.figure()
# plt.imshow(frame_markers)
# plt.legend()
# plt.show()

cameramatrix=np.array([[1.00960817e+03, 0.00000000e+00, 1.92015178e+03]
 ,[0.00000000e+00, 1.00960817e+03, 2.55982854e+03],
 [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])

distortion=np.array([[-4.78775837e-04],[-2.67098072e-04],[-1.00359742e-02],[-1.46699378e-02],[-3.57763854e-05],
 [ 9.25316047e-04],[ 4.65017990e-04],[ 8.53696597e-05],[ 0.00000000e+00],[ 0.00000000e+00],
 [ 0.00000000e+00],[ 0.00000000e+00],[ 0.00000000e+00],[ 0.00000000e+00]])

size_of_marker =  0.06 # side lenght of the marker in meter
rotationVecs,translationVecs, _objectCorners = aruco.estimatePoseSingleMarkers(corners, size_of_marker , cameramatrix, distortion)
#The returned transformation is the one that transforms points from each marker coordinate system to the camera coordinate system. 
#The marker corrdinate system is centered on the middle of the marker, with the Z axis perpendicular to the marker plane.
#The coordinates of the four corners of the marker in its own coordinate system are:
#(-markerLength/2, markerLength/2, 0), (markerLength/2, markerLength/2, 0),
#(markerLength/2, -markerLength/2, 0), (-markerLength/2, -markerLength/2, 0)
length_of_axis = 0.1
imaxis = aruco.drawDetectedMarkers(resized.copy(), corners, ids)
try:
    #alternative to try is a if condition which might be faster https://stackoverflow.com/questions/2522005/cost-of-exception-handlers-in-python 
    for i in range(len(translationVecs)):
        imaxis = aruco.drawAxis(imaxis, cameramatrix, distortion, rotationVecs[i], translationVecs[i], length_of_axis)
        #X:red, Y:green, Z:blue.
    plt.figure()
    plt.imshow(imaxis)
    plt.show()
except TypeError :
    pass
