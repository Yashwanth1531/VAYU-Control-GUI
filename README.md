# VAYU-Control-GUI
A windows application for controlling BLDC motors using serial communication via PWM signals from Arduino

/*
>> This is a dir of two files:
	>> VAYU_GUI: 	Container for helper functions and GUI classes.
	>> GUI_Master:	Is the main file and only this needs to be executed. ("python GUI_Master.py")

>> Arduino_Src dir contains two more dir, each containing one file:
	>> Servo_Control_BLDC_Ardino: 	is for controlling BLDC motors directly from built-in pwm-pins.
	>> Servo_Control_BLDC_PCA:	is a source code for controlling BLDC motors using PCA9685 board along with Arduino.'
	>> NOTE: 
		1.There is minor change in the definition of arming and calibrating sequence for ESCs when using without PCA board.
		  Only the user input definition needs to be updated. While there should be not no problem in running with PCA board.	
		2.The GUI does not yet have the feature to select COM port, hence the COMPort needs to be hard-coded manually.
		
>> @Author: Yashwanth M
>> @Date:   17/12/2023		

*/
