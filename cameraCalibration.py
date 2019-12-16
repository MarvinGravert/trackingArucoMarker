import numpy as np
import cv2,os
import cv2.aruco as aruco
import matplotlib.pyplot as plt
import matplotlib


aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
###CREATE BOARD

#create charucuboardobject
#(number squares in x,number squares in y, size of checkers squares in meter,
#   size of arucuo squares(relative size matters), aruco_dict object as reference
#   for the markers
board = aruco.CharucoBoard_create(5, 7, 1, .6, aruco_dict)
imboard = board.draw((4000, 4000))#returns ready to be printed board with given size
# cv2.imwrite("calibrationChessboard.tiff", imboard)#write to file
# fig = plt.figure()

# plt.imshow(imboard,cmap=matplotlib.cm.gray,  interpolation = "nearest")
# plt.show()

###READ IN CALIBRATION PICTURES
# datadir="calibrationImages/"
datadir="new/"
images=np.array([datadir + f for f in os.listdir(datadir) if f.endswith(".png") ])

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

def read_chessboards(images):
    """
    Charuco base pose estimation.
    source: https://mecaruco2.readthedocs.io/en/latest/notebooks_rst/Aruco/sandbox/ludovic/aruco_calibration_rotation.html
    """
    print("POSE ESTIMATION STARTS:")
    allCorners = []
    allIds = []
    decimator = 0
    # SUB PIXEL CORNER DETECTION CRITERION
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.00001)
    
    for im in images:
        print("=> Processing image {0}".format(im))
        frame = cv2.imread(im)       
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #resized=scaleImage(gray,10)
        #parameters=cv2.aruco.DetectorParameters_create()#modification
        corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(gray, aruco_dict)
        """ PLOT THE DETECTED ONES
        frame_markers=aruco.drawDetectedMarkers(resized.copy(), corners, ids)
        
        fig=plt.figure()
        plt.imshow(frame_markers)
        for i in range(len(ids)):
            c = corners[i][0]#corners is a list of lists, and the corner coordinatnes are in the first list
            #then we plot the mean x and y value of the corners though this wont actually be the center
            plt.plot([c[:, 0].mean()], [c[:, 1].mean()], "o", label = "id={0}".format(ids[i]))
        plt.legend()
        plt.show()
        """
        ######
        if len(corners)>0:
            # SUB PIXEL DETECTION
            for corner in corners:
                cv2.cornerSubPix(gray, corner,
                                 winSize = (3,3),
                                 zeroZone = (-1,-1),
                                 criteria = criteria)
            res2 = cv2.aruco.interpolateCornersCharuco(corners,ids,gray,board)
            if res2[1] is not None and res2[2] is not None and len(res2[1])>3 and decimator%1==0:
                allCorners.append(res2[1])
                allIds.append(res2[2])

        decimator+=1

    imsize = gray.shape
    return allCorners,allIds,imsize

def calibrate_camera(allCorners,allIds,imsize):
    """
    Calibrates the camera using the dected corners.
    source: https://mecaruco2.readthedocs.io/en/latest/notebooks_rst/Aruco/sandbox/ludovic/aruco_calibration_rotation.html
    some modifaction have been done+comments added
    """
    print("CAMERA CALIBRATION")

    cameraMatrixInit = np.array([[ 1000.,    0., imsize[0]/2.],
                                 [    0., 1000., imsize[1]/2.],
                                 [    0.,    0.,           1.]])

    distCoeffsInit = np.zeros((5,1))
    #calibration flags are set here
    flags = (cv2.CALIB_USE_INTRINSIC_GUESS + cv2.CALIB_RATIONAL_MODEL + cv2.CALIB_FIX_ASPECT_RATIO)
    #flags = (cv2.CALIB_RATIONAL_MODEL)
    (ret, camera_matrix, distortion_coefficients0,
     rotation_vectors, translation_vectors,
     stdDeviationsIntrinsics, stdDeviationsExtrinsics,
     perViewErrors) = cv2.aruco.calibrateCameraCharucoExtended(
                      charucoCorners=allCorners,
                      charucoIds=allIds,
                      board=board,
                      imageSize=imsize,
                      cameraMatrix=cameraMatrixInit,
                      distCoeffs=distCoeffsInit,
                      flags=flags,
                      criteria=(cv2.TERM_CRITERIA_EPS & cv2.TERM_CRITERIA_COUNT, 10000, 1e-9))

    return ret, camera_matrix, distortion_coefficients0, rotation_vectors, translation_vectors

allCorners,allIds,imsize=read_chessboards(images)



ret, camera_matrix, distortion_coefficients0, rotation_vectors, translation_vectors = calibrate_camera(allCorners,allIds,imsize)
print(camera_matrix)
print(distortion_coefficients0)


"""
cameramatrix=np.array([[1.00960817e+03, 0.00000000e+00, 1.92015178e+03]
 ,[0.00000000e+00, 1.00960817e+03, 2.55982854e+03],
 [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])

distortion=np.array([[-4.78775837e-04],[-2.67098072e-04],[-1.00359742e-02],[-1.46699378e-02],[-3.57763854e-05],
 [ 9.25316047e-04],[ 4.65017990e-04],[ 8.53696597e-05],[ 0.00000000e+00],[ 0.00000000e+00],
 [ 0.00000000e+00],[ 0.00000000e+00],[ 0.00000000e+00],[ 0.00000000e+00]])
 """