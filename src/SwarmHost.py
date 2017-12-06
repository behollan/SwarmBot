#!/usr/bin/python
# coding: utf-8
"""
   _____                              __  __           __ 
  / ___/      ______ __________ ___  / / / /___  _____/ /_
  \__ \ | /| / / __ `/ ___/ __ `__ \/ /_/ / __ \/ ___/ __/
 ___/ / |/ |/ / /_/ / /  / / / / / / __  / /_/ (__  ) /_  
/____/|__/|__/\__,_/_/  /_/ /_/ /_/_/ /_/\____/____/\__/  

Welcome to the SwarmHost controller Version 0.1.0
For more information about this project, visit the github:
	 https://github.com/behollan/SwarmBot

Authors:	Ben Holland 
			Graduate Student, Colorado School of Mines 
			Mechanical Engineering Department
			benjamin.holland1@gmail.com
		Josh McNeely 
			Graduate Student, Colorado School of Mines 
			Electrical Engineering Department
			jmcneely@mines.edu

Usage: 
    SwarmHost -h | --help
    SwarmHost -v | --version 
    SwarmHost calibrate --outfile=<FILE> [--infile=<FILE>]
    SwarmHost homography --calibFile=<FILE> [--outfile=<FILE>]
    SwarmHost listBots
    SwarmHost arucoTest [--calibFile=<FILE> --dict=<INT>]
    SwarmHost loadParams --calibFile=<FILE>
    SwarmHost homoTest [--calibFile=<FILE> --homography=<FILE>] 

Options:
    -o=<FILE> --outfile=<FILE> 	        Location of output calibration file
    -i FILE --infile=<FILE>    	        Location of input calibration file
    --matrix=<FILE>   	                Homography matrix file, .CSV format
    -c FILE --calibFile=<FILE>  	Path of calibration file
    -d=<INT> --dict=<INT>		Standard Aruco Dictionary Value, see wiki
    --homography=<FILE>                 Homography matrix file location
"""

## New main console application, cause Python > C++
from docopt import docopt
import subprocess
import cv2
import cv2.aruco as aruco
import shlex
import numpy as np
font = cv2.FONT_HERSHEY_SIMPLEX

def arucoTest():
# Runs the aruco test script from the openCV modules. Checks for input
#   arguments otherwise runs using 4x4_50 dictionary and no camera 
#   calibration (no pose estimation).
 
    # Default dictionary and calib file:
    dictionary = 0
    calibFile = None

    # Check if dictionary value is passed
    if "--dict" in arguments and "--calibFile" in arguments:
        calibFile = arguments["--calibFile"]
        dictionary = arguments["--dict"]
	args = "./aruco_detect_markers -d=%s -c%s"%(dictionary, calibFile)
    # Dictionary only, no calibfile
    elif "--dict" in arguments:
        dictionary = arguments["--dict"]
        args = "./aruco_detect_markers -d=%s "%(dictionary)
    # No dict or calib file, use default
    else:
        args = "./aruco_detect_markers -d=%s "%(dictionary)

    # Execute the aruco detect script from OpenCV Modules
    print("Dictionary: %s, calibFile: %s"%(dictionary,calibFile))
    print(args)
    
    args = shlex.split(args)

    popen = subprocess.Popen(args, stdout = subprocess.PIPE)
    popen.wait()
    output = popen.stdout.read()
    print output

def calibrate():
# Calibrate the camera using a ChAruco Board. Uses hardoced values for board right now.
#    Could be changed to be more adaptable in the future, though this process really only needs i
#    to be performed once for a give camera. 
    h = 5
    w = 7
    ml = 0.0165 # 1.65 cm
    sl = 0.033  # 3.3 cm
    d = 0       # 4x4_50

    print("To capture a frame for calibration, press 'c'")
    print("To finish capturing, press 'ESC' key and calibration starts.")
    outfile = arguments["--outfile"]

    args = "./aruco_calibrate_camera_charuco -d=%s -h=%s -w=%s --ml=%s --sl=%s %s "%(d, h, w, ml, sl, outfile)
    args = shlex.split(args)
    popen = subprocess.Popen(args, stdout = subprocess.PIPE)
    popen.wait()
    output = popen.stdout.read()
    print output
   
    return

def findHomo():
    """
    findHomo calculates the homography transform matrix. 
    More information on why we use the homography transform can be found on the wiki.

    findHomo draws a 7x5 ChAruco Board on the projector display using 100 px wide sides.
    The location of these squares is then observed and stored using the webcam.

    cv2.findHomography(pts_src, pts_dst) is then used to calculate the 3x3 homography transform from the
    projector frame to the camera frame. The inverse of this transform is also stored. 

    cv2.warpPerspective(im_src, im_dst, h, size) then transforms points in the src frame to the dst frame 
    using the homography transform above.
    """
    aruco_dict = aruco.getPredefinedDictionary(0)
    
    # Load camera calibration Parameters
    calibrationFile = arguments["--calibFile"]
    calibParams = cv2.FileStorage(calibrationFile, cv2.FILE_STORAGE_READ)
    mtx = calibParams.getNode("cameraMatrix").mat()
    dist = calibParams.getNode("distCoeffs").mat()
    
    arucoParams = aruco.DetectorParameters_create()

    # Print some help information
    print("Calculate the homography transform matrix.")
    print("Using a 4x3 4x4_50 ChAruco Board on the projector for calibration.\n")

    # Draw the ChAruco Board in a projector window
    aruco_dict = aruco.getPredefinedDictionary(0)
    board = aruco.CharucoBoard_create(4, 3 , 1824/4 , 1824/4/2, aruco_dict)
    board_image = board.draw((1824,984))
    # Copy of image for adding prompt text
    board_image_prompt = board_image
    cv2.putText(board_image_prompt, "Verify image is shown on projector in full screen.",(14,20),font,0.5,(0,0,0))
    cv2.putText(board_image_prompt, "Press ENTER to continue.", (14,40), font, 0.5, (0,0,0)) 
    # Put prompt image full screen on the projector window.
    cv2.namedWindow("Calibration Image", cv2.WND_PROP_FULLSCREEN )
    cv2.setWindowProperty("Calibration Image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow('Calibration Image', board_image_prompt)
    cv2.waitKey(0)

    print("Beginning homography calculation...")
    # Charuco Board Corners
    pts_src = board.chessboardCorners
    pts_src = np.delete(pts_src,2,1)
    print("Printed Corner Locations (Projector Frame): ")
    print(pts_src)
    
    # Setup camera for image
    webCam = cv2.VideoCapture( 0 )
    while(True):
        if webCam.isOpened( ) == False:
            print("Failed to open webcam.")
            return -1
        ret = False
        while ret == False:
            ret, cam_image = webCam.read() 
        # Have user verify camera sees image
        cv2.putText(cam_image, "Verify that the webcam can see the iamge.",(14,20),font,0.5,(0,0,255))
        cv2.putText(cam_image, "Press q to continue", (14,40),font, 0.5, (0,0,255))
        cv2.imshow('Webcam', cam_image )
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyWindow("Webcam")
            ret, homoCapture = webCam.read()
            print("Image capture.")
            break
    # Close all windows
    cv2.destroyAllWindows()
    # Detect Charuco Checkerboard corners and IDs
    corners, ids, _ = aruco.detectMarkers(homoCapture, aruco_dict, parameters=arucoParams, cameraMatrix=mtx, distCoeffs=dist)
    retval, charucoCorners, charucoIds = aruco.interpolateCornersCharuco(corners, ids, homoCapture, board, cameraMatrix=mtx, distCoeffs=dist)
    
    # Draw the detected markers
    aruco.drawDetectedCornersCharuco(homoCapture, charucoCorners, charucoIds)
    
    print("Detected Corners (Camera Frame): ")
    
    charucoCorners = np.squeeze(charucoCorners) # Resize Charuco corner array
    print(charucoCorners) # Print detected chessboard corners
    
    cv2.arrowedLine(homoCapture, (0,0),(50,0), (0,0,255),1)
    cv2.arrowedLine(homoCapture, (0,0),(0,50), (0,0,255),1)
    cv2.putText(homoCapture, "x", (50,10),font,0.5,(0,0,255)) 
    cv2.putText(homoCapture, "y", (5,50),font,0.5,(0,0,255)) 

    cv2.imshow("Detected Markers",homoCapture)
    cv2.waitKey(0)

    homo = cv2.findHomography(pts_src, charucoCorners)
    print("\nHomography Matrix:")
    print(homo[0])
    if arguments["--outfile"] is not None:
        print("Saving file to " + arguments["--outfile"])
        np.savetxt(arguments["--outfile"],homo[0])
    return

def homoTest():
    """
    homoTest detects a marker and prints a location on the screen defined by the homography matrix given
    Used to test a homography transform created using findHomo()
    """

    h = np.loadtxt(arguments["--homography"])
    print(h)
    cap = cv2.VideoCapture(0)
    aruco_dict = aruco.getPredefinedDictionary(0)
    
    # Load camera calibration Parameters
    calibrationFile = arguments["--calibFile"]
    calibParams = cv2.FileStorage(calibrationFile, cv2.FILE_STORAGE_READ)
    mtx = calibParams.getNode("cameraMatrix").mat()
    dist = calibParams.getNode("distCoeffs").mat()
    
    arucoParams = aruco.DetectorParameters_create()
    while(1):
        ret, im_src = cap.read()
        ids = None
        markerImage = np.zeros((1824,984,3),np.uint8)
        if ret is True:
            corners, ids, _ = aruco.detectMarkers(im_src, aruco_dict, parameters=arucoParams, cameraMatrix=mtx, distCoeff=dist)
            
            if ids is not None: # Check if any markers were detected and draw them
                print("Marker(s) Detected.")
                markerImage = aruco.drawDetectedMarkers(markerImage, corners, ids, (255,0,0))
                im_out = cv2.warpPerspective(markerImage, h, (1824, 984))
                cv2.namedWindow("Homography Applied", cv2.WND_PROP_FULLSCREEN )
                cv2.setWindowProperty("Homography Applied", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
                cv2.imshow('Homography Applied', im_out)
        
        if cv2.waitKey(1) & 0xFF== ord('q'): # If ESC is pressed, break the test loop
            break
    
if __name__=='__main__':
    arguments = docopt(__doc__, version='Swarm Host 0.1')
    print(arguments)

    # Aruco marker Detection
    if arguments["arucoTest"] == True:
        print("Running Aruco Test")
	arucoTest()	

    # Camera calibration using ChAruco board
    elif arguments["calibrate"] == True:
	print("Calibrating Camera.\n")
	calibrate()

    # Calculate the homography matrix
    elif arguments["homography"] == True:
	findHomo()

    elif arguments["homoTest"] == True:
        homoTest()
