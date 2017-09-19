#include "SWARMBOT.h"

SWARMBOT swarmbot;

void setup(){
  swarmbot.setupBot();
}

void loop(){
  //swarmbot.checkSerial();
  //swarmbot.checkSolar();

  swarmbot.line(100,1000);
  delay(1000);
  swarmbot.line(-100,1000);
  delay(1000);
}


