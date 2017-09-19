Swarm Robots v 0.1

Currently only works on Arduino Uno.
Pin numbers can be found in the SWARMBOT header file

Public robot control functions to use

line(speed,duration)
spin(speed,duration)

-speed ranges from -7 (full speed backwards or CCW) to +7 (full speed forwards or CW)
-duration is positive int in number of milliseconds to do action

updateLED(color)

-color is a 3 byte CRGB datatype describing the color to set the LED to
- permissable values include CRGB::Green CRGB::Pink etc.

wheelTest()

-linearly increases the wheel speeds from 0-7 every 1 second to check for imbalance between right/left servos

checkSerial()

-if data is in the serial buffer, will parse it and execute the action sent


message format is an 8 bit number, with each bit describing a different part of action

bit #    meaning
0	action type (0=spin, 1 = line)
1	direction (0=backwards/CCW,1=forwards/CW)
2,3,4	speed (ranges from 0-7)
5,6,7	duration (ranges from 0-7 but then gets scaled by 100 to produce an output range of 0ms - 700ms)


To send messages over serial:
set baud to 9600
type 8-bit message followed by newline character (press Enter)

An example message is:
01100101

which means
0 = Spin
1 = CW
100 = Speed of 4
101 = Duration of 500ms

Another example message:
10001010

1 = Line
0 = Backwards
001 = Speed of 1
010 = Duration of 200ms


TODO:
Add ATTiny specific code
- soft servos
- no serial

Incorporate calibration values to allow for differences in left/right wheel.
-Write and access calibration vals in the EEPROM

Include low battery logic
Include charging logic