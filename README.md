# SwarmBot
Swarm robot monitoring and control using OpenCV and solar panel data transmission.

## Better description here eventually
Also see the [wiki](https://github.com/behollan/SwarmBot/wiki)

# Theory
## Solar panel data transmission
_(Copied from the Spring 2017 paper)_
Once an individual robot's pose is known, the overhead projector can send data only to the specific location corresponding to that robot's solar panel.  This not only allows each robot to receive individualized commands, it also allows all communication to be done in parallel.

To send data to a specific robot, an overhead projector displays a white or dark circle centered on that bot's solar panel to create a voltage difference on the panels output. This change in intensity is small, and the digital inputs of the microcontroller are not able to discern the small $\Delta$V of the unconditioned panel voltage.  In order for the robot to interpret this signal, an inline filter is used to ensure a logic level output to the microcontroller.

The LT1013 is used to build a comparator circuit. To ensure the filter output is independent of the light intensity of the surroundings, a simple RC high pass filter is included before the signal goes to the LT1013. When a white square is ''written" to the solar panel, the voltage on its output increases. This change propagates through to the comparator, and if the filtered signal goes above the reference value, the amplifier saturates the output at V+. The other scenario (signal is smaller than reference) sets the output at V-. For our purpose, V+ is set at 3V and V- is ground, allowing the digital inputs of the microcontroller to read the message the projector is sending.

## Determining Robot Positions
_(Copied from the Spring 2017 paper)_
In order to send commands to individual robots, it is necessary to understand the robot's position and orientation. To determine robot position, each robot is equipped with a 1.25 inch AR tag with a unique identifier. An example of two AR tags is given in the figure below. These tags contain both a unique identifier and orientation.
 
![AR Tag 1](/images/ARTags.PNG)

A Logitech C270 webcam was placed over the robot arena and used to determine each robot's position and orientation. The frames from the camera are passed to a computer running OpenCV \cite{openCV}. This computer then determines the location of each tag, its orientation, and its unique identifier. Once this information is determined, the desired signal can be sent to only a specific location in the robot arena. 

Because the camera and the projector do not have the same field of view, a homography mapping was used to ensure the robot locations corresponded to the appropriate projector pixel location. The homography matrix is determined using the OpenCV function "FindHomography". A graphic of this mapping is shown in the figure below.

![Homography](/images/Homography.PNG)

The homography transformation allows the signals to be projected only to the solar panel location. This allows for individual robot communication and prevents the projected image from interfering with the AR tag detection. In addition, it ensures that the message is in the correct location regardless of discrepancies between to field of view.

# Demos
Eventually this section will be populated with Demo videos
