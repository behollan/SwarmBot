# SwarmBot
Swarm robot monitoring and control using OpenCV and solar panel data transmission.

## Better description here eventually
Also see the [wiki](https://github.com/behollan/SwarmBot/wiki)

# Theory
## Solar panel data transmission
(Copied from the Spring 2017 paper)


## Determining Robot Positions
In order to send commands to individual robots, it is necessary to understand the robot's position and orientation. To determine robot position, each robot is equipped with a 1.25 inch AR tag with a unique identifier. An example of two AR tags is given in the figure below. These tags contain both a unique identifier and orientation.
 
![AR Tag 1](/images/AR1.png) ![AR Tag 1](/images/AR.png)

A Logitech C270 webcam was placed over the robot arena and used to determine each robot's position and orientation. The frames from the camera are passed to a computer running OpenCV \cite{openCV}. This computer then determines the location of each tag, its orientation, and its unique identifier. Once this information is determined, the desired signal can be sent to only a specific location in the robot arena. 

Because the camera and the projector do not have the same field of view, a homography mapping was used to ensure the robot locations corresponded to the appropriate projector pixel location. The homography matrix is determined using the OpenCV function "FindHomography". A graphic of this mapping is shown in the figure below.

![Layout](/images/Layout.png)
![Homography](/iamges/Homography.png)

The homography transformation allows the signals to be projected only to the solar panel location. This allows for individual robot communication and prevents the projected image from interfering with the AR tag detection. In addition, it ensures that the message is in the correct location regardless of discrepancies between to field of view.

# Demos
Eventually this section will be populated with Demo videos
