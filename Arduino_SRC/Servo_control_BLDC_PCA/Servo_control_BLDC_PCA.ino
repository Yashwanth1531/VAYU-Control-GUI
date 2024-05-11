/*
  >>  This is a code to send PWM signals to each ESCs connected to PCA9685 boards.
  >>  The minimum and maximum pulse width of the PWM signal for ESCs are fixed at 1000 to 2000 micro-seconds.
  >>  There are tow inputs for this script:
      >> "Arm": first input to arms and calibrates ESCs to respective max and min pulse_width.
      >> BoardID,ChannelID,speed: BoardID is used to index PCA_board object, ChannelID is used to index the 16-pwm_channels on each PCA_board.
  >>  @Author:  Yashwanth M
  >>  @Date:    17/12/2023
*/
#include <Adafruit_PWMServoDriver.h>

const int Baud_rate                 = 9600;   // Data transfer rate (Bits per second).
const int Max_PulseWidth            = 2000;   // Maximum pulse-width in micro-seconds.
const int Min_PulseWidth            = 1000;   // Minimum pulse-width in micro-seconds
const int PCA_Boards                = 1;      // Number of PCA9685 boards.
const int Channel_num               = 16;     // Number of channels on each boards.
const int PWM_freq                  = 50;     // Simonk30a ESCs have 50-60 Hz PWM frequency compatability. 
const int Max_throttle              = 100;
const int Min_throttle              = 0;
const int Board_address[PCA_Boards] = {0x40};  // 0x40, 0x41...
int rise_time_ESC                   = 500;    // 0.5s for ESC to set the RPM.

// Creating an object/instance of PCA9685 board1: Addressed->(0x40). 
// Default is considered even without explicit board1 address input.
// For daisy chain connections solder the address jumpers on the PCA9685 board2: Addressed->(0x41)...
 Adafruit_PWMServoDriver pwm0 = Adafruit_PWMServoDriver(Board_address[0]);

// 2D-Array of pin numbers for each PCA_Boards:
const int pins[PCA_Boards][Channel_num] = {{0}}; 
//--------------------------------------------------------------------------------------------------------------------------------------------
void PWM_begin(int PWM_freq){
  pwm0.begin();
  /* 
    >>  Set this value untill desired (ESC_FREQ or pwm-freq) is actully observed in the PWM pins of the PCA9685 board through oscilloscope.
    >>  The clock in the PCA9685 board is not accurate enough to achieve the desired set ESC_FREQ (pwm-freq).
  */
  pwm0.setOscillatorFrequency(27000000);    
  pwm0.setPWMFreq(PWM_freq);              // Set the ESC operating frequency.
  // delay(10);
  yield();
}
//--------------------------------------------------------------------------------------------------------------------------------------------
void ESC_Calibrate(int Channel_num, int PulseWidth){
  for(int pin_number=0; pin_number<Channel_num; pin_number++){  
    pwm0.writeMicroseconds(pin_number, PulseWidth);
  }
}
//--------------------------------------------------------------------------------------------------------------------------------------------
void ESC_CalibrationSequence(int Channel_num, int min_pulse_width, int max_pulse_width){
  // Start with maximum throttle signal to all ESCs
  ESC_Calibrate(Channel_num, max_pulse_width);
  delay(1000);
  // Sequence calibrate after recieving Arming signal from user 
  while (true) {
    if (Serial.available()>0) {
      String CalCommand = Serial.readStringUntil('\n');
      if (CalCommand.equals("Arm")) {
        // Send minimum throttle signal to calibrate all ESCs between max and min pulse width.
        ESC_Calibrate(Channel_num, min_pulse_width);
        delay(2000);  // Wait for 2 seconds for ESC initialization
        
        Serial.println("ESC calibration complete.");
        break;  // Exit the loop after calibration
      }
      else {
        Serial.println("Invalid command. Please enter 'Arm' to calibrate ESCs.");
      }
    }
  } 
}
//--------------------------------------------------------------------------------------------------------------------------------------------

void setup() {
  Serial.begin(Baud_rate);
  PWM_begin(PWM_freq);
  ESC_CalibrationSequence(Channel_num, Min_PulseWidth, Max_PulseWidth);
  yield();
}

//--------------------------------------------------------------------------------------------------------------------------------------------

void loop() {
  int pwm_width;

  if(Serial.available()>0){
    String input = Serial.readStringUntil('\n'); // Read the input string until newline character
    // Split the input string into ESC Rowindex, Columnindex, and speed
    int DelimiterIndex1 = input.indexOf(',');
    int DelimiterIndex2 = input.indexOf(',', DelimiterIndex1 + 1);

    if (DelimiterIndex1 != -1 && DelimiterIndex2 != -1) {
      String Board_ID_Str     = input.substring(0, DelimiterIndex1);
      String Channel_ID_Str   = input.substring(DelimiterIndex1 + 1, DelimiterIndex2);
      String Speed_Str        = input.substring(DelimiterIndex2 + 1);

      // Convert string ESC Rowindex, Columnindex, and speed to integers
      int Board_ID    = Board_ID_Str.toInt();
      int Channel_ID  = Channel_ID_Str.toInt();
      int speed       = Speed_Str.toInt();
      if (Board_ID >= 0 && Board_ID < PCA_Boards && Channel_ID >= 0 && Channel_ID < Channel_num && speed >= Min_throttle && speed <= Max_throttle) {
          // Mapping the speed (throttle percentage) to PWM-pulse width:
          pwm_width = map(speed, Min_throttle, Max_throttle, Min_PulseWidth, Max_PulseWidth);
          // Set the speed for the corresponding ESC:
          switch (Board_ID) {
            case 0:
              pwm0.writeMicroseconds(Channel_ID, pwm_width); 
              break;
            case 1:
              //When second PCA board is adde: Board_ID equals 2
              break;
          }
            
          Serial.print("Throttle for Motor["); Serial.print(Board_ID); Serial.print(","); Serial.print(Channel_ID); Serial.print("]: "); Serial.print(speed); Serial.println("%");
      }
      // Case to Stop all the motors immediatedly !
      else if (Board_ID == -1 && Channel_ID == -1 && speed == -1) {
        Serial.println("! STOP ALL !");
        pwm_width = 1000;
        for(int i=0; i<Channel_num; i++){
          pwm0.writeMicroseconds(i, pwm_width);
          // pwm1.writeMicroseconds(i, speed);...set motors to zero for all boards.
        }
      }
      else {
        Serial.println("Enter valid numbers: BoardID (0-N), ChannelID (0-16), speed (1000-2000)micro-seconds");
      }
      delay(rise_time_ESC);
    }
  }
}

//--------------------------------------------------------------------------------------------------------------------------------------------