#include "Arduino.h"

#include "source/Defines.h"

#include "source/MotorControl/MotorSpeedController.h"
#include "source/TasksControl/TaskManager.h"

MotorSpeedController leftWheel;
MotorSpeedController rightWheel;

#include "source/Communication/commonFunctions.h"
#include "source/distanceSensor.h"

#include "source/Communication/SerialInterpreter.h"


// !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
// !!!!!!!!!!!!!!!! IMPORTANT BEFORE YOU RUN THE PROGRAM !!!!!!!!!!!!!!!!!!
// !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
// PLEASE EDIT FILE HardwareSerial.h EDITING THE FOLLOWING LINE:
// #define SERIAL_RX_BUFFER_SIZE 100 // 64
// BIGGER BUFFER IS NEEDED WHILE JSON MESSAGES ARE LONGER THAN 64 CHARACTERS
// MAX_RECEIVED_STRING_LEN set to 100
// program accepts only jsons with elements in a right order
// !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

volatile uint8_t counter = 0;

void setup() {

	Serial.begin(38400);

	delay(1000); // delay the start of the program for a while

	//PinController::getInstance()->setPinUsage(LED_BUILTIN, DIGITAL_OUTPUT);

	leftWheel.initializeController(encoder0PinA, encoder0PinB,
			leftEncoderCounter, motorLPWMPin, motorLDirPin, 0.32, 0.0, 0.0, 50);
	leftWheel.setSetSpeed(0);

	rightWheel.initializeController(encoder1PinA, encoder1PinB,
			rightEncoderCounter, motorRPWMPin, motorRDirPin, 0.3, 0.0, 0.0, 50);
	rightWheel.setSetSpeed(0);

	printFreeMemory();

	initializeDistanceSensor();
	initializeDistanceSensor2();

	//TaskManager::getInstance()->addTask(0, 50, plotPIDcontrol);
	//TaskManager::getInstance()->addTask(1, 170, printPIDcontrol);
	TaskManager::getInstance()->addTask(2, 1000, triggerDistanceSensorSignal);
	TaskManager::getInstance()->addTask(3, 1000, triggerDistanceSensor2AndMeasure);

	delay(500); // delay the start of the program for a while

	leftWheel.enableController();
	rightWheel.enableController();
}

void loop() {

	leftWheel.controlSpeed();
	rightWheel.controlSpeed();

	TaskManager::getInstance()->realizeTasks();

	getDistanceSensorMeasurement();

	if (counter == 0) {
		printFreeMemory();
		counter++;
	}

	serialRead();
}

// reads and interpretes messages sent via Serial
// accepts only jsons with elements in a right order
void serialRead() {
	while (Serial.available()) {
		String inputString;
		inputString = Serial.readString();
		int length = inputString.length();
		if (length >= MAX_RECEIVED_STRING_LEN) {
			// Serial.println("JSON message too long! Over 100 chars!");
			Serial.println("S|MA|sE|tl"); // to long
		} else if (length > 2) { // 2 is the minimum length
			Serial.println(inputString);
			if (inputString.startsWith("SS")) { //setSpeed
				setSpeed(atoi(inputString.substring(2).c_str()));
			} else if (interpreteMessage(inputString)) {
				Serial.println("I|MA|sE|OK");
			} else {
				Serial.println("S|MA|sE|NOK"); // not ok
				printFreeMemory();
			}
			inputString = "";
		}
	}
}

// sets speed to an agent
// is a shorter command to set speed instead of json message
void setSpeed(int val) {
	if (val == 0) {
		leftWheel.stopMotor();
		rightWheel.stopMotor();
		leftWheel.disableController();
		rightWheel.disableController();
		leftWheel.clearITerm();
		rightWheel.clearITerm();
		leftWheel.setSetSpeed(0);
		rightWheel.setSetSpeed(0);
	} else {
		leftWheel.setSetSpeed(val);
		rightWheel.setSetSpeed(val);
		leftWheel.enableController();
		rightWheel.enableController();
	}
}
