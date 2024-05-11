/*
  >> This code allows user to independently control an array of BLDC motors connected to ESCs.
  >> The minimum and maximum pulse width of the PWM signal for ESCs are fixed at 1000 to 2000 micro-seconds.
  >> There are three inputs for this script:
      >> "ARM": first input to connect ESCs to respective digital-PWM pins.
      >> "CAL": second input to calibrate the connected ESCs with min and max pulse-width.
      >> Row,Col,speed: Repeating input, Row and Col is used as ID for which motor's speed is being updated.
  >> Connetion to Arduino UNO: 
      >> ESC's signal wires are connected to digital-pwm pins.
      >> Also the GND wire also needs to be connected to GND-Arduino.
  >> @Author: YASHWANTH M
  >> @date:   17/12/2023
*/
#include <Servo.h>

const int Baud_rate       = 9600; 
const int ROWS            = 1;    // Number of rows of ESC/Motors
const int COLS            = 2;    // Number of colums of ESC/Motors
const int Max_PulseWidth  = 2000;
const int Min_PulseWidth  = 1000;
int rise_time_ESC         = 500;  // 0.5s for ESC to set the RPM

// How to automate this?
const int pins[ROWS][COLS] = {{9,10}};  //pins[0][0] = 9; pins[0][1] = 10;

// 2D array of Servo objects/ 2D array of Servo class instances 
Servo ESCs[ROWS][COLS];


//---------------------------------------------------------------------------------------------------------//
void ESC_Arm(int rows, int cols){
    for (int i = 0; i < ROWS; i++) {
      for (int j = 0; j < COLS; j++) {
        ESCs[i][j].attach(pins[i][j]);
      }
    }
}

//---------------------------------------------------------------------------------------------------------//
void ESC_ArmingSequence(int rows, int cols){
    while (true) {
    if (Serial.available()) {
      String armCommand = Serial.readStringUntil('\n');
      if (armCommand.equals("ARM")) {
        // Send minimum throttle signal to calibrate all ESCs between max and min pulse width.
        ESC_Arm(rows,cols);
        delay(10);
        /*
          >>  Do not add delays randomly here.
          >>  Adding too much delay here would result in lack of calibration of ESCs (atlest one of'em).
          >>  In case calibration issuse exists, directly call the ESC_arm function insted of this sequence.
        */
        Serial.println("ESCs are armed.");
        break;  // Exit the loop after calibration
      }
      else {
        Serial.println("Invalid command. Please enter 'ARM' to arm ESCs.");
      }
    }
  } 
}
//---------------------------------------------------------------------------------------------------------//
void ESC_Calibrate(int rows, int cols, int pulse_width){
    
    for (int i = 0; i < ROWS; i++) {
      for (int j = 0; j < COLS; j++) {
        ESCs[i][j].writeMicroseconds(pulse_width);
      }
    }
}
//---------------------------------------------------------------------------------------------------------//
void ESC_CalibrationSequence(int rows, int cols, int max_pulse_width, int min_pulse_width){
  // Start with maximum throttle signal to all ESCs
  ESC_Calibrate(rows, cols, max_pulse_width);
  delay(1000);
  // Sequence calibrate after recieving Arming signal from user 
  while (true) {
    if (Serial.available()) {
      String CalCommand = Serial.readStringUntil('\n');
      if (CalCommand.equals("CAL")) {
        // Send minimum throttle signal to calibrate all ESCs between max and min pulse width.
        ESC_Calibrate(rows, cols, min_pulse_width);
        delay(2000);  // Wait for 2 seconds for ESC initialization
        
        Serial.println("ESC calibration complete.");
        break;  // Exit the loop after calibration
      }
      else {
        Serial.println("Invalid command. Please enter 'CAL' to calibrate ESCs.");
      }
    }
  } 
}
//---------------------------------------------------------------------------------------------------------//


void setup() {
  Serial.begin(Baud_rate);  // Set the baud rate for serial communication

  // Attach Servo objects to corresponding ESC signal wires
  ESC_ArmingSequence(ROWS, COLS);

  ESC_CalibrationSequence(ROWS, COLS, Max_PulseWidth, Min_PulseWidth);
}


//---------------------------------------------------------------------------------------------------------//


void loop() {
  String input; // Variable to store the serial input string

  // Check for serial input
  if (Serial.available() > 0) {
    input = Serial.readStringUntil('\n');  // Read the input string until newline character

    // Split the input string into ESC Rowindex, Columnindex, and speed
    int DelimiterIndex1 = input.indexOf(',');
    int DelimiterIndex2 = input.indexOf(',', DelimiterIndex1 + 1);

    if (DelimiterIndex1 != -1 && DelimiterIndex2 != -1) {
      String ESC_xID_Str  = input.substring(0, DelimiterIndex1);
      String ESC_yID_Str  = input.substring(DelimiterIndex1 + 1, DelimiterIndex2);
      String speed_Str    = input.substring(DelimiterIndex2 + 1);

      // Convert string ESC Rowindex, Columnindex, and speed to integers
      int ESC_xID = ESC_xID_Str.toInt();
      int ESC_yID = ESC_yID_Str.toInt();
      int speed   = speed_Str.toInt();

      // Check if the indices and speed are within the valid range
      if (ESC_xID >= 0 && ESC_xID < ROWS && ESC_yID >= 0 && ESC_yID < COLS &&
          speed >= Min_PulseWidth && speed <= Max_PulseWidth) {
        // Set the speed for the corresponding ESC:
        ESCs[ESC_xID][ESC_yID].writeMicroseconds(speed);
        Serial.print("Speed set for ESC[");
        Serial.print(ESC_xID);
        Serial.print(",");
        Serial.print(ESC_yID);
        Serial.print("]: ");
        Serial.println(speed);
      } 
      else {
        Serial.println("Invalid indices or speed. Please enter valid values.");
      }

      // Wait for the ESC to reach the desired speed
      delay(rise_time_ESC);
    }
  }
}


//---------------------------------------------------------------------------------------------------------//