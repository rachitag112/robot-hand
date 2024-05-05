#include <ESP32Servo.h>

#define SERVO_PIN1 26
#define SERVO_PIN2 13
#define SERVO_PIN3 32

Servo ind_mid;
Servo rin_pin;
Servo thum;

int incomingByte = 0;

void setup() {
  Serial.begin(9600);
  Serial.println("I'm LIVE");

  ind_mid.attach(SERVO_PIN1);
  rin_pin.attach(SERVO_PIN2);
  thum.attach(SERVO_PIN3);
}

void loop() {
  
  // ind_mid.write(180);
  // rin_pin.write(0);
  // thum.write(0);

  incomingByte = Serial.parseInt();

  switch(incomingByte) {
    case 1:
      Serial.println("stone");

      ind_mid.write(0);
      rin_pin.write(180);
      thum.write(60);

      break;
    case 2:
      Serial.println("scissor");
      
      ind_mid.write(180);
      rin_pin.write(180);
      thum.write(60);

      break;
    case 3:
      Serial.println("paper");

      ind_mid.write(180);
      rin_pin.write(0);
      thum.write(0);   
      break;
  }
}
