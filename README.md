# VAYU-Control-GUI
A windows application for controlling BLDC motors using serial communication via PWM signals from Arduino


This is a dir of two files:
	VAYU_GUI: 	Container for helper functions and GUI classes.
	GUI_Master:	This is the main file and only this needs to be executed. ("python GUI_Master.py")

Arduino_Src dir contains two more dir, each containing one file:
	Servo_Control_BLDC_Ardino: 	is for controlling BLDC motors directly from built-in PWM-pins.
	Servo_Control_BLDC_PCA:	is a source code for controlling BLDC motors using a PCA9685 board along with Arduino.'
	NOTE: 
		1. There is a minor change in the definition of arming and calibrating sequence for ESCs when using without a PCA board.
		  Only the user input definition needs to be updated. While there should be no problem in running with the PCA board.	
		2. The GUI does not yet have the feature to select COM port, hence the COMPort needs to be hard-coded manually.
		
@Date:   17/12/2023		


