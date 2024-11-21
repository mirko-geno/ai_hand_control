#include <Servo.h>

#define BAUDRATE 9600 

#define SERVOS 5
#define SERVO1 3  // Thumb
#define SERVO2 5  // Index finger
#define SERVO3 6  // Middle finger
#define SERVO4 9  // Ring finger
#define SERVO5 10 // Pinky finger

#define OPEN 0
#define CLOSE 180
Servo myservo[SERVOS];  // Create an array of servo objects to control the servos

void open_finger(byte);
void close_finger(byte);
void inicializacion(void);

void setup() {
  // Attach each servo to a unique pin
  Serial.begin(BAUDRATE);

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
  inicializacion();

  Serial.begin(BAUDRATE);
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, HIGH);
  Serial.println("LISTO!!!"); 
}

void loop() {
  
  if (Serial.available() > 0) {
     
    Serial.println("recibi algo");
    byte message = Serial.read();  // Read the 5-bit message from Serial
    Serial.println(message);

    if (message == 0x01){
      digitalWrite(LED_BUILTIN, HIGH);
    }
    else {
      digitalWrite(LED_BUILTIN, LOW);
    }
  
      for(int i=0x01,finger_count=0;i<0x20;i<<=1,finger_count++){
        open_finger(finger_count);
          Serial.print("Dedo ");
          Serial.print(finger_count);
        if((message&i)==i){
          Serial.println("Abierto");
        }else{
          close_finger(finger_count);
          Serial.println("Cerrado");
        }
      }
     delay(100);  // Small delay for stability
   }
}


void open_finger(byte finger){
  if (finger == 2 || finger == 4) {
    myservo[finger].write(CLOSE);
  } else {
    myservo[finger].write(OPEN);
  }
}

void close_finger(byte finger){
  if (finger == 2 || finger == 4) {
    myservo[finger].write(OPEN);
  } else {
    myservo[finger].write(CLOSE);
  }
}

void inicializacion(void){
   int pos=0;
       for (pos = 0; pos <= 180; pos += 1) { // goes from 0 degrees to 180 degrees
        // in steps of 1 degree
        for(int i=0;i<SERVOS;i++){
          if(i==1 || i==3)myservo[i].write(180-pos);  
          else myservo[i].write(pos);              // tell servo to go to position in variable 'pos'
        }
        delay(15);                       // waits 15ms for the servo to reach the position
      }
      for (pos = 180; pos >= 0; pos -= 1) { // goes from 180 degrees to 0 degrees
        for(int i=0;i<SERVOS;i++){
        if(i==1 || i==3)myservo[i].write(180-pos);  
          else myservo[i].write(pos);              // tell servo to go to position in variable 'pos'
        }
        
        delay(15);                       // waits 15ms for the servo to reach the position
      }
   
  }