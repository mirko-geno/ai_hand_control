#include <Servo.h>
#define SERVOS 5
#define SERVO1 3
#define SERVO2 5
#define SERVO3 6
#define SERVO4 9
#define SERVO5 10

Servo myservo[SERVOS];  // create servo object to control a servo

int pos = 0;    // variable to store the servo position

void setup() {
  Serial.begin(9600);  // Start the serial communication at 9600 baudrate
  myservo[0].attach(SERVO1);  
  myservo[1].attach(SERVO2);
  myservo[2].attach(SERVO3);
  myservo[3].attach(SERVO4);
  myservo[4].attach(SERVO5);
}

void loop() {
  if (Serial.available() > 0) {
    String fingerStates = Serial.readStringUntil('\n'); // Read incoming data
    Serial.println("Received data: " + fingerStates);  // Print received data for debugging
    
    // Split the received data into individual states for each finger
    int fingerStatesArray[5];
    int i = 0;
    int val = 0;
    for (char &ch : fingerStates) {
      if (ch == ',') {
        fingerStatesArray[i] = val;
        i++;
        val = 0;
      } else {
        val = val * 10 + (ch - '0');
      }
    }
    fingerStatesArray[i] = val;  // To account for the last value

    // Map the received states to servo positions
    for (int i = 0; i < 5; i++) {
      if (fingerStatesArray[i] == 1) {
        myservo[i].write(0);  // Open position for the finger
      } else {
        myservo[i].write(180);  // Closed position for the finger
      }
    }
  }
}
