#include <Servo.h>

// Define servo objects
Servo servo1;
Servo servo2;
Servo servo3;
Servo servo4;
Servo servo5;

// Define pins for each servo
const int servoPin1 = 5;
const int servoPin2 = 4;
const int servoPin3 = 0;
const int servoPin4 = 16;
const int servoPin5 = 14;

// Current angles for each servo
int angle1 = 90;
int angle2 = 90;
int angle3 = 90;
int angle4 = 90;
int angle5 = 90;

// Amount to change per key press
const int step = 1;

// Calibrate pulse widths (microseconds) for full servo travel.
// Adjust these if your servo needs different endpoints (typical ~500..2500).
const int servoMinPulse = 500;
const int servoMaxPulse = 2500;

void setup() {
  // Attach servos to pins (use calibrated min/max pulse to ensure full 0-180
  // range)
  servo1.attach(servoPin1, servoMinPulse, servoMaxPulse);
  servo2.attach(servoPin2, servoMinPulse, servoMaxPulse);
  servo3.attach(servoPin3, servoMinPulse, servoMaxPulse);
  servo4.attach(servoPin4, servoMinPulse, servoMaxPulse);
  servo5.attach(servoPin5, servoMinPulse, servoMaxPulse);

  // Initialize to midpoint
  servo1.write(angle1);
  servo2.write(angle2);
  servo3.write(angle3);
  servo4.write(angle4);
  servo5.write(angle5);

  // Start serial for keyboard control 
  Serial.begin(115200);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB boards
  }

  Serial.println("Ready. Use keys to control servos:");
  Serial.println("d/a = servo1 -/+ , s/w = servo2 -/+ , i/k = servo3 -/+ ");
  Serial.println("l/o = servo4 -/+ , q/e = servo5 -/+");

  // Hardware reminder: if servos don't reach full travel, ensure servos have a
  // proper power supply (external 5V source for many servos) and a common
  // ground with the microcontroller.
}

void printAngles() {
  Serial.print("Angles -> ");
  Serial.print("S1:");
  Serial.print(angle1);
  Serial.print(" ");
  Serial.print("S2:");
  Serial.print(angle2);
  Serial.print(" ");
  Serial.print("S3:");
  Serial.print(angle3);
  Serial.print(" ");
  Serial.print("S4:");
  Serial.print(angle4);
  Serial.print(" ");
  Serial.print("S5:");
  Serial.println(angle5);
}

// Clamp helper
int clampAngle(int a) {
  if (a < 5)
    return 5;
  if (a > 175)
    return 175;
  return a;
}

void loop() {
  if (Serial.available() > 0) {
    char c = Serial.read();

    switch (c) {
    // Servo 1: decrease 'a', increase 'd'
    case 'd':
      angle1 = clampAngle(angle1 - step);
      servo1.write(angle1);
      break;
    case 'a':
      angle1 = clampAngle(angle1 + step);
      servo1.write(angle1);
      break;

    // Servo 2: decrease 's', increase 'w'
    case 's':
      angle2 = clampAngle(angle2 - step);
      servo2.write(angle2);
      break;
    case 'w':
      angle2 = clampAngle(angle2 + step);
      servo2.write(angle2);
      break;

    // Servo 3: decrease 'k', increase 'i'
    case 'i':
      angle3 = clampAngle(angle3 - step);
      servo3.write(angle3);
      break;
    case 'k':
      angle3 = clampAngle(angle3 + step);
      servo3.write(angle3);
      break;

    // Servo 4: decrease 'l', increase 'o'
    case 'l':
      angle4 = clampAngle(angle4 - step);
      servo4.write(angle4);
      break;
    case 'o':
      angle4 = clampAngle(angle4 + step);
      servo4.write(angle4);
      break;

    // Servo 5: decrease 'q', increase 'e'
    case 'q':
      angle5 = clampAngle(angle5 - step);
      servo5.write(angle5);
      break;
    case 'e':
      angle5 = clampAngle(angle5 + step);
      servo5.write(angle5);
      break;

    // Ignore CR/LF
    case '\r':
    case '\n':
      break;
    }

    // After any change, print the new angles
    printAngles();
  }
}
