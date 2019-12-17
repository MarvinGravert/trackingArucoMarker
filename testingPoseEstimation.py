# import numpy as np
# import cv2
# from cv2 import aruco 

# cameraMatrix=np.array([[1.39600404e+03, 0.00000000e+00, 7.31255395e+02],
#  [0.00000000e+00, 1.39600404e+03, 6.62993401e+02],
#  [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])
# distortionMatrix=np.array([[-0.07742588],
#  [ 0.03566092],
#  [ 0.00470899],
#  [-0.00515483],
#  [-0.82473463],
#  [ 0.09419457],
#  [ 0.06327745],
#  [-0.99720608],
#  [ 0.        ],
#  [ 0.        ],
#  [ 0.        ],
#  [ 0.        ],
#  [ 0.        ],
#  [ 0.        ]])

# def estimatePose(frame):
#     """
#     Estimates the pose of the marker(s), which are detected beforehand in the frame
#     input
#     frame: grayscaled image potentially including an marker
#     output: roationVector and translationVector of the markers detected as tuple of (array([[[x,y,z]]],
#     """
#     corners, ids, rejectedImgPoints = aruco.detectMarkers(frame, aruco_dict, parameters=parameters)
#     rotationVecs,translationVecs, _objectCorners = aruco.estimatePoseSingleMarkers(corners, size_of_marker , cameraMatrix, distortionMatrix)
#     return rotationVecs,translationVecs
# def detectMarker(frame):
#     """
#     Detects the markers in the picture
#     frame: grayscaled image potentially including a marker
#     output: number of markers detected
#     """
#     try:
#         corners, ids, rejectedImgPoints = aruco.detectMarkers(frame, aruco_dict, parameters=parameters)
#         numMarker=len(ids)
#     except TypeError :#TypeError happends if no markers detected and hence ids=[] thus no length
#         numMarker=0
#     return numMarker

# aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
# size_of_marker =  0.05#0.06 measurement in meter
# parameters =  aruco.DetectorParameters_create()


# frame = cv2.imread("images/Lenna.png")
# gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
# print(estimatePose(gray))
# msvcrt is a windows specific native module
import msvcrt
import time

# asks whether a key has been acquired
def kbfunc():
    #this is boolean for whether the keyboard has bene hit
    x = msvcrt.kbhit()
    if x:
        #getch acquires the character encoded in binary ASCII
        ret = msvcrt.getch()
    else:
        ret = False
    return ret

#begin the counter
number = 1

#infinite loop
while True:

    #acquire the keyboard hit if exists
    x = kbfunc() 

    #if we got a keyboard hit
    if x != False and x.decode() == 's':
        #we got the key!
        #because x is a binary, we need to decode to string
        #use the decode() which is part of the binary object
        #by default, decodes via utf8
        #concatenation auto adds a space in between
        print ("STOPPING, KEY:", x.decode())
        #break loop
        
    time.sleep(0.1)