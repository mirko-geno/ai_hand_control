#include <Servo.h>

#define SERVOS 5
#define SERVO1 3  // Thumb
#define SERVO2 5  // Index finger
#define SERVO3 6  // Middle finger
#define SERVO4 9  // Ring finger
#define SERVO5 10 // Pinky finger

Servo myservo[SERVOS];  // Create an array of servo objects to control the servos

void setup() {
  // Attach each servo to a unique pin
  myservo[0].attach(SERVO1);  // Thumb attached to pin 3
  myservo[1].attach(SERVO2);  // Index finger attached to pin 5
  myservo[2].attach(SERVO3);  // Middle finger attached to pin 6
  myservo[3].attach(SERVO4);  // Ring finger attached to pin 9
  myservo[4].attach(SERVO5);  // Pinky finger attached to pin 10

  // Initialize servos to neutral positions
  myservo[0].write(0);  // Thumb at 0 degrees (open)
  myservo[1].write(180);  // Index at 180 degrees (closed)
  myservo[2].write(0);  // Middle at 0 degrees (open)
  myservo[3].write(180);  // Ring at 180 degrees (closed)
  myservo[4].write(0);  // Pinky at 0 degrees (open)

  delay(1000);  // Wait for servos to reach positions
}

void loop() {
  if (Serial.available() > 0) {
    byte message = Serial.read();  // Read the 5-bit message from Serial

    // Thumb (bit 0)
    if (bitRead(message, 0) == 1) {
      myservo[0].write(0);  // Thumb open
    } else {
      myservo[0].write(180);  // Thumb closed
    }

    // Index (bit 1)
    if (bitRead(message, 1) == 1) {
      myservo[1].write(0);  // Index open
    } else {
      myservo[1].write(180);  // Index closed
    }

    // Middle (bit 2)
    if (bitRead(message, 2) == 1) {
      myservo[2].write(0);  // Middle open
    } else {
      myservo[2].write(180);  // Middle closed
    }

    // Ring (bit 3)
    if (bitRead(message, 3) == 1) {
      myservo[3].write(0);  // Ring open
    } else {
      myservo[3].write(180);  // Ring closed
    }

    // Pinky (bit 4)
    if (bitRead(message, 4) == 1) {
      myservo[4].write(0);  // Pinky open
    } else {
      myservo[4].write(180);  // Pinky closed
    }

    delay(100);  // Small delay for stability
  }
}
