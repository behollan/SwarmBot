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
    SwarmHost [(-h | --help)]
    SwarmHost [(-v | --version)] 
    SwarmHost calibrate --outfile=<OUTFILE> [--infile=<INFILE>]
    SwarmHost homography [--matrix=<MATFILE>]
    SwarmHost listBots
    SwarmHost arucoTest [--calibFile=<CALIBFILE>] [(--dict|-d)=<DICTIONARY>]
    SwarmHost loadParams --calibFile=<CALIBFILE>
    
Options:
    --outfile=<OUTFILE>  	Location of output calibration file
    --infile=<INFILE>    	Location of input calibration file
    --matrix=<MATFILE>   	Homography matrix file, .CSV format
    --calibFile=<CALIBFILE>  	Path of calibration file
    --dict=<DICTIONARY>		Standard Aruco Dictionary Value, see wiki
"""

## New main console application, cause Python > C++
from docopt import docopt
import subprocess
import cv2
import cv2.aruco as aruco

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
	args = "aruco_detect_markers -d %s -c %s"%(dictionary, calibFile)
    # Dictionary only, no calibfile
    elif "--dict" in arguments:
        dictionary = arguments["--dict"]
        args = "aruco_detect_markers -d %s "%(dictionary)
    # No dict or calib file, use default
    else:
        args = "aruco_detect_markers -d %s "%(dictionary)

    # Execute the aruco detect script from OpenCV Modules
    print("Dictionary: %s, calibFile: %s"%(dictionary,calibFile))
    print(args)
    popen = subprocess.Popen(args, stdout = subprocess.PIPE)
    popen.wait()
    output = popen.stdout.read()
    print output
   
    return

def calibrate():
# Calibrate the camera using a ChAruco Board. Uses hardoced values for board right now.
#    Could be changed to be more adaptable in the future, though this process really only needs i
#    to be performed once for a give camera. 
    h = 5
    w = 7
    ml = 0.034  # 3.4 cm
    sl = 0.0355 # 3.5 cm
    d = 0       # 4x4_50

    print("To capture a frame for calibration, press 'c'\n")
    print("To finish capturing, press 'ESC' key and calibration starts.\n")
    outfile = arguments["--outfile"]

    args = "aruco_calibrate_camera_aruco -d %s %s "%(d, outfile)
    popen = subprocess.Popen(args, stdout = subprocess.PIPE)
    popen.wait()
    output = popen.stdout.read()
    print output
   
    return

def findHomo():

    return

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
	print("Calculating Homography transform.")
	print("Make sure the projector is on and the calibration window is full screen.")
	findHomo()


