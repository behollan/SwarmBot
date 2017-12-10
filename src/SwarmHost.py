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
    SwarmHost helloWorld [--calibFile=<FILE> --homography=<FILE>]

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
import time
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
    """
    Calibrate the camera using a ChAruco Board. Uses hardoced values for board right now.
    Could be changed to be more adaptable in the future, though this process really only needs
    to be performed once for a give camera. 
    """
    
    # 7x5 Charuco board with markers 1.65 cm wide and chess squares 3.3 cm wide. Uses 4x4_50 dictionary
    h = 5
    w = 7
    ml = 0.0165 # 1.65 cm
    sl = 0.033  # 3.3 cm
    d = 0       # 4x4_50

    print("To capture a frame for calibration, press 'c'")
    print("To finish capturing, press 'ESC' key and calibration starts.")
    
    # Set the calibration output file location
    outfile = arguments["--outfile"]

    # Start the aruco_calibrate_camera_charuco script from OpenCV Modules
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

    findHomo draws a 4x3 ChAruco Board on the projector display using resolution/4 pixel wide sides.
    The location of these squares is then observed and stored using the webcam.

    cv2.findHomography(pts_src, pts_dst) is then used to calculate the 3x3 homography transform from the
    projector frame to the camera frame. The inverse of this transform is also stored. 

    cv2.warpPerspective(im_src, im_dst, h, size) then transforms points in the src frame to the dst frame 
    using the homography transform above.
    """
    # Set the dictionary to 4x4_50
    aruco_dict = aruco.getPredefinedDictionary(0)
    
    # Load camera calibration Parameters
    calibrationFile = arguments["--calibFile"]
    calibParams = cv2.FileStorage(calibrationFile, cv2.FILE_STORAGE_READ)
    mtx = calibParams.getNode("camera_matrix").mat()
    dist = calibParams.getNode("distortion_coefficients").mat()
    
    # Create a detector parameter object
    arucoParams = aruco.DetectorParameters_create()

    # Print some help information
    print("Calculate the homography transform matrix.")
    print("Using a 4x3 4x4_50 ChAruco Board on the projector for calibration.\n")

    # Draw the ChAruco Board in a projector window
    aruco_dict = aruco.getPredefinedDictionary(0)
    board = aruco.CharucoBoard_create(4, 3 , 1024/4 , 1024/4/2, aruco_dict)
    board_image = board.draw((1024,768))

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
    
    # Store Charuco Board Corners
    pts_src = board.chessboardCorners
    pts_src = np.delete(pts_src,2,1)
    
    # Roll the corners 3 values around the matrix to get indexing right during detection
    pts_src = np.roll(pts_src,-3,axis=0)

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
    corners, ids, _ = aruco.detectMarkers(homoCapture, aruco_dict, parameters=arucoParams, cameraMatrix=mtx,distCoeff=dist)
    retval, charucoCorners, charucoIds = aruco.interpolateCornersCharuco(corners, ids, homoCapture, board, cameraMatrix=mtx, distCoeffs=dist)
    
    # Draw the detected markers for the user
    aruco.drawDetectedCornersCharuco(homoCapture, charucoCorners, charucoIds)
    
    print("Detected Corners (Camera Frame): ")
    
    charucoCorners = np.squeeze(charucoCorners) # Resize Charuco corner array
    print(charucoCorners) # Print detected chessboard corners
    
    # Draw a set of coordinate axis for the user
    cv2.arrowedLine(homoCapture, (0,0),(50,0), (0,0,255),1)
    cv2.arrowedLine(homoCapture, (0,0),(0,50), (0,0,255),1)
    cv2.putText(homoCapture, "x", (50,10),font,0.5,(0,0,255)) 
    cv2.putText(homoCapture, "y", (5,50),font,0.5,(0,0,255)) 

    # Show the detected markers until the uses presses a key
    cv2.imshow("Detected Markers",homoCapture)
    cv2.waitKey(0)

    # Calculate the homography between the webcam and projector
    print("Finding homography between:")
    print(pts_src)
    print(charucoCorners)
    
    homo = cv2.findHomography(pts_src, charucoCorners)
    
    print("\nHomography Matrix:")
    print(homo[0])
    
    # Save the homography matrix to a text file specified by the user (if passed during initialization)
    if arguments["--outfile"] is not None:
        print("Saving file to " + arguments["--outfile"])
        np.savetxt(arguments["--outfile"],homo[0])
    return

def homoTest():
    """
    homoTest detects a marker and prints a location on the screen defined by the homography matrix given
    Used to test a homography transform created using findHomo()
    """
    
    # Load homography matrix
    h = np.loadtxt(arguments["--homography"])
    print(h)
    
    # Set up the camera for detection
    cap = cv2.VideoCapture(0)

    # Set the default Aruco Dictionary to 4x4_50
    aruco_dict = aruco.getPredefinedDictionary(0)
    
    # Load camera calibration Parameters
    calibrationFile = arguments["--calibFile"]
    calibParams = cv2.FileStorage(calibrationFile, cv2.FILE_STORAGE_READ)
    mtx = calibParams.getNode("camera_matrix").mat()
    dist = calibParams.getNode("distortion_coefficients").mat()
    
    # Create a detector parameter object    
    arucoParams = aruco.DetectorParameters_create()
    
    # Detect markers and perform homography until 'q' is pressed
    while(1):

        # Capture the image
        ret, im_src = cap.read()
        
        # Initialize arrays for marker output image and IDs
        ids = None
        markerImage = np.zeros((1024,768,3),np.uint8)      

        # If camera capture was successful...
        if ret is True:

            # Detect the aruco markers
            corners, ids, _ = aruco.detectMarkers(im_src, aruco_dict, parameters=arucoParams, cameraMatrix=mtx, distCoeff=dist)
            
            # If any markers were detected...
            if ids is not None:
                print("Marker(s) Detected.")
                
                # Draw detected markers in the camera frame
                markerImage = aruco.drawDetectedMarkers(markerImage, corners, None, (255,0,0))
                
                # Warp the perspective from the camera to the projector using the homography transform
                im_out = cv2.warpPerspective(markerImage, h, (1024, 768),flags=cv2.WARP_INVERSE_MAP)

                # Setup output window parameters
                cv2.namedWindow("Homography Applied", cv2.WND_PROP_FULLSCREEN )
                cv2.setWindowProperty("Homography Applied", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
                
                # Show the image
                cv2.imshow('Homography Applied', im_out)
        
        if cv2.waitKey(1) & 0xFF== ord('q'): # If 'q' is pressed, break the test loop
            break
   
def helloWorld():
    '''
    helloWorld detects arucoTags on bots and sends a series of debug
    messages to the on board solar panel. 

    Currently the message string should be:
        1. Forward Line, speed of 2, length of 200 ms
            11010010
        2. Spin CCW, speed of 4, duration of 500 ms
            01100101
        3. Spin CW, speed of 4, duration of 500 ms
            00100101
        4. Backward Line, Speed of 2, length of 200 ms
            10010010

    Messages are sent to the location of the aruco tag offset by 2 inches
    '''
    # Logging performance runs
    f = open("perf.log", 'a+')
    print("Running hello world!\n\n")
    print("Loading Parameters...")
    
    # Array of messages to be sent, only supports first message string right now. 
    messg = np.array([[1,1,0,1,0,0,1,1], [0,1,1,0,0,1,0,1], [0,0,1,0,0,1,0,1], [1,0,0,1,0,0,1,0]])
    print("Message strings:\n "+str(messg))

    # Load homography matrix
    h = np.loadtxt(arguments["--homography"])
    print("Homography matrix:\n "+ str(h))
    
    # Set up camera on interface 0
    cap = cv2.VideoCapture(0)

    # Set dictionary to 4x4_50 (0)
    aruco_dict = aruco.getPredefinedDictionary(0)
    
    # Load camera calibration Parameters
    calibrationFile = arguments["--calibFile"]
    calibParams = cv2.FileStorage(calibrationFile, cv2.FILE_STORAGE_READ)
    mtx = calibParams.getNode("camera_matrix").mat()
    dist = calibParams.getNode("distortion_coefficients").mat()
    
    # Generate detector parameters
    arucoParams = aruco.DetectorParameters_create()
    arucoParams.adaptiveThreshConstant = 30

    # Set refresh rate parameters
    fps = 5 # Projector update frames per second
    refresh_rate = 1.0/fps # Clock rate (Hz)

    # Print loaded config properties
    print("\nCamera Calibration Matrix: \n" + str(mtx))
    print("\nDistortion coefficients: \n" + str(dist))
    print("\nFrames per second: " + str(fps))
    print("\t"+str(1.0/fps)+" seconds/frame")
    time.sleep(3)

    # Start main detection and projection loop
    print("\nDetecting bots")
    
    # Set an intial timer value
    t_last = time.clock()
    
    # Run the main projection and detection loop until 'q' is held down
    while(1):
        # Set output window properties
        cv2.namedWindow("Homography Applied", cv2.WND_PROP_FULLSCREEN )
        cv2.setWindowProperty("Homography Applied", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        
        # Set up placeholder arrays for the marker image and ID values
        ids = None
        markerImage = np.zeros((1024,768,3),np.uint8)
        cv2.imshow('Homography Applied',markerImage)
        
        # Get the current webcam image
        ret, im_src = cap.read()
        cv2.imwrite("srcImg.jpg", im_src)
        print("Getting new image")
                   

        # Did we successfully get a webcam image?
        if ret is True:
            
            # Detect Aruco Tags and store corner/id values
            corners, ids, rejected = aruco.detectMarkers(im_src, aruco_dict, parameters=arucoParams, cameraMatrix=mtx, distCoeff=dist)
            
            im_src = aruco.drawDetectedMarkers(im_src,rejected, None, (0,0,255))

            cv2.imwrite("rejectImg.jpg", im_src)
            cv2.imshow("Rejected",im_src)
            # Check if any markers were detected and draw them
            if ids is not None:                
                print("Marker(s) Detected.")
                
                f.write("Num IDs: " + str(len(ids)) + "\n") 
                
                print("IDs: "+ str(ids))
                # Draw marker borders if needed for debugging
                detectedMarkerImage = aruco.drawDetectedMarkers(markerImage, corners, ids, (255,0,0))
                cv2.imwrite("detectedImg.jpg", detectedMarkerImage)
                
                # Get the rotation vectors for each marker
                rvecs, tvecs , _ = aruco.estimatePoseSingleMarkers(corners, 0.053, cameraMatrix=mtx, distCoeffs=dist)
                
                # For each individual marker...
                for i in range(0,len(ids)):

                    # Convert the rotation vector into a rotation matrix
                    # Calculate the offset vector
                    rMat, _ = cv2.Rodrigues(rvecs[i])
                    if i is 0: # Initialize Rot Mat storage if first time in the loop
                        rMats = [rMat]
                        offset = np.dot(rMat,([40],[0],[0]))
                        offset = np.delete(offset, 2)
                        offset_vec = [offset]
                    else: # Append the Rot Mats
                        rMats.append(rMat)
                        offset = [np.dot(rMats[i],([40],[0],[0]))] 
                        offset = np.delete(offset, 2)
                        offset_vec.append(offset)

                # For each bit in the message...
                for bitNum in range(0,len(messg[0])):
                    
                    # Set the message bit
                    bit = messg[0][bitNum]
                    print("Sending Bit: " + str(bit))
                    
                    # Draw an offset polygon for the solar panel
                    for i in range(0,len(ids)): 

                        # Get and set the bit value for the projected square
                        if bit == 1:
                            markerImage = cv2.fillPoly(markerImage, [corners[i].astype(int)], (255,255,255), offset=tuple(offset_vec[i].astype(int)) ) 
                        elif bit == 0:
                            markerImage = cv2.fillPoly(markerImage, [corners[i].astype(int)], (0,0,0), offset=tuple(offset_vec[i].astype(int)) ) 
                
                    # Apply homography mapping for final projector image
                    im_out = cv2.warpPerspective(markerImage, h, (1024, 768),flags=cv2.WARP_INVERSE_MAP)
                    
                    cv2.imwrite("outImg.jpg", im_out)
                   
                    # Timing loop
                    while(1):
                        # Get current system time
                        t_curr = time.clock()
                        
                        # Compare the current time step to the refresh rate, if larger then update the image
                        if (t_curr-t_last) >= refresh_rate:
                            print("Refreshing Image")
                            print("\tCurrent Time: "+ str(t_curr))
                            print("\tTime step: "+str(t_curr-t_last) + "\n")
                            f.write(str(t_curr-t_last)+"\n")

                            # Can the pi keep up with the given refresh rate
                            if abs(refresh_rate-(t_curr-t_last))>0.001:
                                print("\tCan't keep up. Slow the refresh rate.")
                            print('\n\n')
                            cv2.imshow('Homography Applied', im_out)
                            
                            # Set the new "Last updated" timer value
                            t_last = time.clock()
                            cv2.waitKey(1)
                            break
                if cv2.waitKey(1) & 0XFF == ord('q'): # If 'q' is pressed, break the helloWorld Test
                    break
  
if __name__=='__main__':
    
    # Parse command line arugments using DocOpt (one of the coolest python modules out there)
    arguments = docopt(__doc__, version='Swarm Host 0.1')
    
    # Determine which function we are going to run...
    
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
    
    # Test a homography matrix
    elif arguments["homoTest"] == True:
        homoTest()
    
    # Test data transmission
    elif arguments["helloWorld"] == True:
        helloWorld()
