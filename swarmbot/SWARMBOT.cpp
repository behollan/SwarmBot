#include "SWARMBOT.h"

/* Constructor */

SWARMBOT::SWARMBOT(){
}

//setup function
void SWARMBOT::setupBot(){
  FastLED.addLeds<WS2812B, LED_PIN, GRB>(leds, NUM_LEDS);  //setup the LED
  FastLED.setBrightness(LED_BRIGHTNESS); // set the led brightness
  
  pinMode(SOLAR_PIN,INPUT);  //setup the solar panel pin for input

  #if BOARDTYPE
  Serial.begin(9600);
  #else
  //ONLY FOR THE ATTINY - Set up the interrupt that will refresh the servo for us automagically
    OCR0A = 0xAF;            // any number is OK
    TIMSK |= _BV(OCIE0A);    // Turn on the compare interrupt (below!)
  #endif
  
  lWheel.attach(SERVO1PIN);   // Attach the servo for the left wheel
  rWheel.attach(SERVO2PIN);   // Attach the servo for the right wheel
  stopServos();  //kill them at startup

  updateLed(startupColor);  //set initial color to red
  
}

/* LED Functions */

//writes to the LED pin to change the color
void SWARMBOT::updateLed(CRGB color){
  for (int i=0;i<NUM_LEDS;i++){leds[i] = color;}  //set the color
   FastLED.show();  //update led to show it
}

/* Servo Functions */

//turns an input speed of -7 to 7 to the servo bounds (0 to 179)
int SWARMBOT::mapSpeed(int speedIn){
  int zeroSpeed = 90;  
  int deadband = 10;  

  if (speedIn>7) speedIn = 7;  //saturate if it's too big
  if (speedIn<-7) speedIn = -7;  
  
  if (speedIn>0) return map(speedIn,0,7,zeroSpeed+deadband,179);
  if (speedIn<0) return map(-speedIn,0,7,zeroSpeed-deadband,0);
  if (speedIn==0) return zeroSpeed;
}

//maps input speeds from -7 to 7 for both wheels and writes the servos
void SWARMBOT::writeServos(int speed1,int speed2){
  updateLed(actionColor);
  lWheel.write(mapSpeed(speed1));
  rWheel.write(mapSpeed(speed2)); 
}

//Turns both servos off
void SWARMBOT::stopServos(){
  writeServos(0,0);
  updateLed(idleColor);
}

/* Robot functions */

//runs the wheels at increasingly faster speeds to check for imbalance
void SWARMBOT::wheelTest(){
  int delayTime = 1000;  //1 second between speedups
  for (int i=0;i<7;i++){
    line(i,100);
    delay(delayTime);
  }
}

//moves robot in straight line at set speed from -7 (full backwards) to 7 (full forwards) for spinTime milliseconds
void SWARMBOT::line(int lineSpeed,int lineTime){
  writeServos(lineSpeed,-lineSpeed);
  delay(lineTime);
  stopServos();
}

//moves robot in circle at speed from -7 (full CCW) to 7 (full CW) for spinTime milliseconds
void SWARMBOT::spin(int spinSpeed, int spinTime){
  writeServos(spinSpeed,spinSpeed);
  delay(spinTime);
  stopServos();
}

/* Communication functions */

// reads a message on the message pin, with delays
void SWARMBOT::checkSolar(){
  if (digitalRead(SOLAR_PIN)){
    interpretMessage(readSolar());
  }
}

int SWARMBOT::readSolar(){
  updateLed(receivingMessageColor);
  int msg = 0;
  for (int i=0;i<MSG_LENGTH;i++){
    msg += pow(2,i) * digitalRead(SOLAR_PIN);  //bitshift each reading and update the 1byte msg variable
    delay(MSG_DELAY);  //wait for the projector to change
  }
  return msg;
}


//given an 16-bit message in in the form of an int, parse the bits to determine the meaning
void SWARMBOT::interpretMessage(int msgIn){
  updateLed(interpretColor);
  
  bool commandType = bitRead(msgIn,0);  //extract first bit for spin/line
  int dir = bitRead(msgIn,1);  //2nd bit is direction (f/b or ccw/cw)
  int sSpeed = 4*(bitRead(msgIn,2)) + 2*(bitRead(msgIn,3)) + (bitRead(msgIn,4)); //get speed from 0-7, bits 1-3
  if (dir) sSpeed=-sSpeed;  //flip speed sign if direction is negative
  
  int sDuration = 4*(bitRead(msgIn,5)) + 2*(bitRead(msgIn,6)) + (bitRead(msgIn,7));  //get duration from 0-7, bits 5-7
  sDuration = sDuration*100; //scale the delay time by 100
  
  if (commandType) spin(sSpeed,sDuration);
  else line(sSpeed,sDuration);
}

//reads the LOWBAT pin and changes the low batt flag accordingly
void SWARMBOT::checkBattery(){
  if (digitalRead(BATT_PIN)==1) {
    lowBatt = true;
    updateLed(lowBatteryColor);  //turn LED to red if low battery
    return;
  }
}

#if BOARDTYPE  //Enable serial for unos

//once a message is parsed, can print it to the serial monitor for debugging
void SWARMBOT::printMsgSerial(int commandType, int sSpeed, int sDuration){
  if (commandType) Serial.print("Spin:  ");
  else Serial.print("Line:");
  
  Serial.print("Duration: "); Serial.print(sDuration);
  Serial.print("  Speed: ");  Serial.println(sSpeed);
}

//check if there is data in the serial buffer
bool SWARMBOT::checkSerial() {
  if (Serial.available()){
    interpretMessage(receiveSerialMessage());
  }
}

//receive a stream of serial data and update the message variable
int SWARMBOT::receiveSerialMessage(){
  updateLed(receivingMessageColor);  //change LED to indicate receiving message

  int message = 0;
  int index = 0;
  while (Serial.available()) { // if there's any serial available, read it:
    Serial.println((int)Serial.peek()-0x30);
    message += (1<<index)* (int)(Serial.read() - 0x30);
    index++;
    delay(2);
  }
  messageComplete=true;
  return message;
}

#else

void SWARMBOT::refreshServos(){
    lWheel.refresh();
    rWheel.refresh();
}

volatile uint8_t counter = 0;
//take advantage of the built in millis() time to keep track of time and refresh the servo every 20 milliseconds
SIGNAL(TIMER0_COMPA_vect) {
  // this gets called every 2 milliseconds

  counter += 2;
  // every 20 milliseconds, refresh the servos!
  if (counter >= 20) {
    counter = 0;
    SWARMBOT::refreshServos();
  }
}
#endif

