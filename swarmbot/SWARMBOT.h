#include<Arduino.h>
#include "FastLED.h"

#if defined (__AVR_ATtiny85__)
       #include <Adafruit_SoftServo.h>  // SoftwareServo (works on non PWM pins)
       #define BOARDTYPE 0
#else
       //Arduino
       #include <Servo.h>
       #define BOARDTYPE 1
#endif


#define NUM_LEDS 1
#define LED_PIN  3
#define SOLAR_PIN  0 n
#define MSG_LENGTH  8
#define BATT_PIN   1
#define MSG_DELAY 100
#define SERVO1PIN  10   // Servo control line (orange) on Trinket Pin #0
#define SERVO2PIN  11   // Servo control line (orange) on Trinket Pin #1
#define LED_BRIGHTNESS 10

#define interpretColor CRGB::Purple
#define actionColor CRGB::Blue
#define lowBatteryColor CRGB::Red
#define receivingMessageColor CRGB::White
#define idleColor CRGB::Yellow
#define chargingColor CRGB::Orange
#define startupColor CRGB::Red

class SWARMBOT {
  public:
    SWARMBOT();
    //~SWARMBOT();
    void setupBot();
    void spin(int spinSpeed, int spinTime);
    void updateLed(CRGB color);
    void wheelTest();
    void line(int lineSpeed,int lineTime);
    void checkSolar();
    
    #if BOARDTYPE
    bool checkSerial();
    void printMsgSerial(int commandType, int sSpeed, int sDuration);
    //#else
    //static void refreshServos();
    #endif
    
    unsigned int message;

    
   

  private:

    int mapSpeed(int speedIn);
    void stopServos();
    void writeServos(int speed1,int speed2);
    int readSolar();
    void checkBattery();
    void interpretMessage(int msgIn);

    #if BOARDTYPE
      int receiveSerialMessage();
      Servo lWheel,rWheel;  // create servo object to control a servo
    #else 
      Adafruit_SoftServo lWheel, rWheel;  //create TWO servo objects
   #endif

    boolean messageComplete = false;  // whether the string is complete
    boolean lowBatt = false;

    CRGB leds[NUM_LEDS]; // This is an array of leds.  One item for each led in your strip.

};

