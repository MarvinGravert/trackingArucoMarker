import numpy as np
import cv2,os
import cv2.aruco as aruco
import matplotlib.pyplot as plt
import matplotlib
#more intricate explanation in poseEstimation.py
cameramatrix=np.array([[1.00960817e+03, 0.00000000e+00, 1.92015178e+03]
 ,[0.00000000e+00, 1.00960817e+03, 2.55982854e+03],
 [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])

distortion=np.array([[-4.78775837e-04],[-2.67098072e-04],[-1.00359742e-02],[-1.46699378e-02],[-3.57763854e-05],
 [ 9.25316047e-04],[ 4.65017990e-04],[ 8.53696597e-05],[ 0.00000000e+00],[ 0.00000000e+00],
 [ 0.00000000e+00],[ 0.00000000e+00],[ 0.00000000e+00],[ 0.00000000e+00]])

aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)

size_of_marker =  0.06

cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:#if reading was successful
        cv2.waitKey(1)
        continue
    # Detect marker
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    parameters =  aruco.DetectorParameters_create()
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
    #frame_markers = aruco.drawDetectedMarkers(frame.copy(), corners, ids)
    #estimatePositio
    rotationVecs,translationVecs, _objectCorners = aruco.estimatePoseSingleMarkers(corners, size_of_marker , cameramatrix, distortion)

    length_of_axis = 0.1
    imaxis = aruco.drawDetectedMarkers(frame.copy(), corners, ids)
    for i in range(len(translationVecs)):
        imaxis = aruco.drawAxis(imaxis, cameramatrix, distortion, rotationVecs[i], translationVecs[i], length_of_axis)
    #X:red, Y:green, Z:blue.
    # Display the resulting frame
    length_of_axis = 0.1
    imaxis = aruco.drawDetectedMarkers(resized.copy(), corners, ids)
    try:
        #alternative to try is a if condition which might be faster https://stackoverflow.com/questions/2522005/cost-of-exception-handlers-in-python 
        #if you have 10 loops  and only 1 throws exception if and try are probably equal(prob not if yuo can cancel if earlier)
        for i in range(len(translationVecs)):
            imaxis = aruco.drawAxis(imaxis, cameramatrix, distortion, rotationVecs[i], translationVecs[i], length_of_axis)
            #X:red, Y:green, Z:blue.
            cv2.imshow('Detected',imaxis)
        except TypeError :
            cv2.imshow('Detected',imaxis)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()