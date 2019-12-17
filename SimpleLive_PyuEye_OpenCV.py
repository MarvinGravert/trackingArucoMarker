# ===========================================================================#
#                                                                           #
#  Copyright (C) 2006 - 2018                                                #
#  IDS Imaging Development Systems GmbH                                     #
#  Dimbacher Str. 6-8                                                       #
#  D-74182 Obersulm, Germany                                                #
#                                                                           #
#  The information in this document is subject to change without notice     #
#  and should not be construed as a commitment by IDS Imaging Development   #
#  Systems GmbH. IDS Imaging Development Systems GmbH does not assume any   #
#  responsibility for any errors that may appear in this document.          #
#                                                                           #
#  This document, or source code, is provided solely as an example          #
#  of how to utilize IDS software libraries in a sample application.        #
#  IDS Imaging Development Systems GmbH does not assume any responsibility  #
#  for the use or reliability of any portion of this document or the        #
#  described software.                                                      #
#                                                                           #
#  General permission to copy or modify, but not for profit, is hereby      #
#  granted, provided that the above copyright notice is included and        #
#  reference made to the fact that reproduction privileges were granted     #
#  by IDS Imaging Development Systems GmbH.                                 #
#                                                                           #
#  IDS Imaging Development Systems GmbH cannot assume any responsibility    #
#  for the use or misuse of any portion of this software for other than     #
#  its intended diagnostic purpose in calibrating and testing IDS           #
#  manufactured cameras and software.                                       #
#                                                                           #
# ===========================================================================#

# Developer Note: I tried to let it as simple as possible.
# Therefore there are no functions asking for the newest driver software or freeing memory beforehand, etc.
# The sole purpose of this program is to show one of the simplest ways to interact with an IDS camera via the uEye API.
# (XS cameras are not supported)
# ---------------------------------------------------------------------------------------------------------------------------------------

# Libraries
from pyueye import ueye
import numpy as np
import cv2
import sys
import time
import math
from cv2 import aruco
import msvcrt#for input events keyboard
# ---------------------------------------------------------------------------------------------------------------------------------------
#Camera constants
cameraMatrix=np.array([[1.39600404e+03, 0.00000000e+00, 7.31255395e+02],
 [0.00000000e+00, 1.39600404e+03, 6.62993401e+02],
 [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])
distortionMatrix=np.array([[-0.07742588],
 [ 0.03566092],
 [ 0.00470899],
 [-0.00515483],
 [-0.82473463],
 [ 0.09419457],
 [ 0.06327745],
 [-0.99720608],
 [ 0.        ],
 [ 0.        ],
 [ 0.        ],
 [ 0.        ],
 [ 0.        ],
 [ 0.        ]])
#Marker Settings
aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
size_of_marker =  0.05#0.06 measurement in meter
parameters =  aruco.DetectorParameters_create()
# ---------------------------------------------------------------------------------------------------------------------------------------
# Functions
def estimatePose(frame):
    """
    Estimates the pose of the marker(s), which are detected beforehand in the frame
    input
    frame: grayscaled image potentially including an marker
    output: roationVector and translationVector of the markers detected as tuple of (array([[[x,y,z]]],
    """
    corners, ids, rejectedImgPoints = aruco.detectMarkers(frame, aruco_dict, parameters=parameters)
    rotationVecs,translationVecs, _objectCorners = aruco.estimatePoseSingleMarkers(corners, size_of_marker , cameraMatrix, distortionMatrix)
    return rotationVecs,translationVecs
def detectMarker(frame):
    """
    Detects the markers in the picture
    frame: grayscaled image potentially including a marker
    output: number of markers detected
    """
    try:
        corners, ids, rejectedImgPoints = aruco.detectMarkers(frame, aruco_dict, parameters=parameters)
        numMarker=len(ids)
    except TypeError :#TypeError happends if no markers detected and hence ids=[] thus no length
        numMarker=0
    return numMarker
def kbfunc():
    """
    checks if a key has been hit and returns said key encoded in ASCII or if none has been
    hit it returns false
    """
    #this is boolean for whether the keyboard has bene hit
    x = msvcrt.kbhit()
    if x:
        #getch acquires the character encoded in binary ASCII
        ret = msvcrt.getch()
    else:
        ret = False
    return ret
# ---------------------------------------------------------------------------------------------------------------------------------------

# Variables
hCam = ueye.HIDS(0)  # 0: first available camera;  1-254: The camera with the specified camera ID
sInfo = ueye.SENSORINFO()
cInfo = ueye.CAMINFO()
pcImageMemory = ueye.c_mem_p()
MemID = ueye.int()
rectAOI = ueye.IS_RECT()
pitch = ueye.INT()
nBitsPerPixel = ueye.INT(24)  # 24: bits per pixel for color mode; take 8 bits per pixel for monochrome
channels = 3  # 3: channels for color mode(RGB); take 1 channel for monochrome
m_nColorMode = ueye.INT()  # Y8/RGB16/RGB24/REG32
bytes_per_pixel = int(nBitsPerPixel / 8)
# ---------------------------------------------------------------------------------------------------------------------------------------
print("START")
print()

# Starts the driver and establishes the connection to the camera
nRet = ueye.is_InitCamera(hCam, None)
if nRet != ueye.IS_SUCCESS:
    print("is_InitCamera ERROR")

# Reads out the data hard-coded in the non-volatile camera memory and writes it to the data structure that cInfo points to
nRet = ueye.is_GetCameraInfo(hCam, cInfo)
if nRet != ueye.IS_SUCCESS:
    print("is_GetCameraInfo ERROR")

# You can query additional information about the sensor type used in the camera
nRet = ueye.is_GetSensorInfo(hCam, sInfo)
if nRet != ueye.IS_SUCCESS:
    print("is_GetSensorInfo ERROR")

nRet = ueye.is_ResetToDefault(hCam)
if nRet != ueye.IS_SUCCESS:
    print("is_ResetToDefault ERROR")

# Set display mode to DIB
nRet = ueye.is_SetDisplayMode(hCam, ueye.IS_SET_DM_DIB)

# Set the right color mode
if int.from_bytes(sInfo.nColorMode.value, byteorder='big') == ueye.IS_COLORMODE_BAYER:
    # setup the color depth to the current windows setting
    ueye.is_GetColorDepth(hCam, nBitsPerPixel, m_nColorMode)
    bytes_per_pixel = int(nBitsPerPixel / 8)
    print("IS_COLORMODE_BAYER: ", )
    print("\tm_nColorMode: \t\t", m_nColorMode)
    print("\tnBitsPerPixel: \t\t", nBitsPerPixel)
    print("\tbytes_per_pixel: \t\t", bytes_per_pixel)
    print()

elif int.from_bytes(sInfo.nColorMode.value, byteorder='big') == ueye.IS_COLORMODE_CBYCRY:
    # for color camera models use RGB32 mode
    m_nColorMode = ueye.IS_CM_BGRA8_PACKED
    nBitsPerPixel = ueye.INT(32)
    bytes_per_pixel = int(nBitsPerPixel / 8)
    print("IS_COLORMODE_CBYCRY: ", )
    print("\tm_nColorMode: \t\t", m_nColorMode)
    print("\tnBitsPerPixel: \t\t", nBitsPerPixel)
    print("\tbytes_per_pixel: \t\t", bytes_per_pixel)
    print()

elif int.from_bytes(sInfo.nColorMode.value, byteorder='big') == ueye.IS_COLORMODE_MONOCHROME:
    # for color camera models use RGB32 mode
    m_nColorMode = ueye.IS_CM_MONO8
    nBitsPerPixel = ueye.INT(8)
    bytes_per_pixel = int(nBitsPerPixel / 8)
    print("IS_COLORMODE_MONOCHROME: ", )
    print("\tm_nColorMode: \t\t", m_nColorMode)
    print("\tnBitsPerPixel: \t\t", nBitsPerPixel)
    print("\tbytes_per_pixel: \t\t", bytes_per_pixel)
    print()

else:
    # for monochrome camera models use Y8 mode
    m_nColorMode = ueye.IS_CM_MONO8
    nBitsPerPixel = ueye.INT(8)
    bytes_per_pixel = int(nBitsPerPixel / 8)
    print("else")

# Can be used to set the size and position of an "area of interest"(AOI) within an image
nRet = ueye.is_AOI(hCam, ueye.IS_AOI_IMAGE_GET_AOI, rectAOI, ueye.sizeof(rectAOI))
if nRet != ueye.IS_SUCCESS:
    print("is_AOI ERROR")

width = rectAOI.s32Width
height = rectAOI.s32Height

# Prints out some information about the camera and the sensor
print("Camera model:\t\t", sInfo.strSensorName.decode('utf-8'))
print("Camera serial no.:\t", cInfo.SerNo.decode('utf-8'))
print("Maximum image width:\t", width)
print("Maximum image height:\t", height)
print()

# ---------------------------------------------------------------------------------------------------------------------------------------

# Allocates an image memory for an image having its dimensions defined by width and height and its color depth defined by nBitsPerPixel
nRet = ueye.is_AllocImageMem(hCam, width, height, nBitsPerPixel, pcImageMemory, MemID)
if nRet != ueye.IS_SUCCESS:
    print("is_AllocImageMem ERROR")
else:
    # Makes the specified image memory the active memory
    nRet = ueye.is_SetImageMem(hCam, pcImageMemory, MemID)
    if nRet != ueye.IS_SUCCESS:
        print("is_SetImageMem ERROR")
    else:
        # Set the desired color mode
        nRet = ueye.is_SetColorMode(hCam, m_nColorMode)

# Activates the camera's live video mode (free run mode)
nRet = ueye.is_CaptureVideo(hCam, ueye.IS_DONT_WAIT)
if nRet != ueye.IS_SUCCESS:
    print("is_CaptureVideo ERROR")

# Enables the queue mode for existing image memory sequences
nRet = ueye.is_InquireImageMem(hCam, pcImageMemory, MemID, width, height, nBitsPerPixel, pitch)
if nRet != ueye.IS_SUCCESS:
    print("is_InquireImageMem ERROR")
else:
    print("Press q to leave the programm")

# ---------------------------------------------------------------------------------------------------------------------------------------

# Continuous image display
counter=0
frameDetected=0
frameNotDetected=0
start_time=time.time()
while (nRet == ueye.IS_SUCCESS):

    # In order to display the image in an OpenCV window we need to...
    # ...extract the data of our image memory
    array = ueye.get_data(pcImageMemory, width, height, nBitsPerPixel, pitch, copy=False)

    # bytes_per_pixel = int(nBitsPerPixel / 8)

    # ...reshape it in an numpy array...
    frame = np.reshape(array, (height.value, width.value, bytes_per_pixel))

    # ...resize the image by a half
    frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

    # ---------------------------------------------------------------------------------------------------------------------------------------
    # Include image data processing here
    ###### Test if Marker have been detected/print Pose Estimation 
    x = kbfunc() 

    #if we got a keyboard hit
    if x != False and x.decode() == 's':
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        print("Number of Markers detected: ",detectMarker(gray))

        #print(estimatePose(gray))


        cv2.imshow("DetectedOrNot", gray)
    ###### Number of frames missed
    counter+=1
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if detectMarker(gray):
        frameDetected+=1
    else:
        frameNotDetected+=1
    # ---------------------------------------------------------------------------------------------------------------------------------------
    
    # ...and finally display it
    cv2.imshow("SimpleLive_Python_uEye_OpenCV", frame)
    # Press q if you want to end the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# ---------------------------------------------------------------------------------------------------------------------------------------
end_time=time.time()
print("this took: ",end_time-start_time, "seconds")
print(counter,"frames were considered, ", frameDetected,"frames included a detected marker, ",frameNotDetected,"frames did not")
# Releases an image memory that was allocated using is_AllocImageMem() and removes it from the driver management
ueye.is_FreeImageMem(hCam, pcImageMemory, MemID)

# Disables the hCam camera handle and releases the data structures and memory areas taken up by the uEye camera
ueye.is_ExitCamera(hCam)

# Destroys the OpenCv windows
cv2.destroyAllWindows()

print()
print("END")
