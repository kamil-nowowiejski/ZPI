/*
 * commonFunctions.cpp
 *
 *  Created on: 29.10.2016
 *      Author: TTYBISZE
 */
#include "commonFunctions.h"
#include "../MemoryFree/MemoryFree.h"

#include "Arduino.h"

extern MotorSpeedController leftWheel;
extern MotorSpeedController rightWheel;

/////////////// REPEATED FUNCTIONS FOR TASKS ///////////////////////

void blinkLed() {
	PinController::getInstance()->setPinState(LED_BUILTIN, !PinController::getInstance()->getPinValue(LED_BUILTIN));
}

void printEncoderValues() {
	// Serial.print("Encoder counter values: L: ");
	Serial.print("ECV L: ");
	Serial.print(leftWheel.getEncoderCounterValue(), DEC);
	Serial.print("\tR: ");
	Serial.println(rightWheel.getEncoderCounterValue(), DEC);
}

void plotEncoderValues() {
	plot2(Serial, leftWheel.getEncoderCounterValue(), rightWheel.getEncoderCounterValue());
}

void printPIDcontrol() {
	Serial.print("PID: ");
	Serial.print(leftWheel.getDs());
	Serial.print('\t');
	Serial.print(leftWheel.getMeasuredSpeed());
	Serial.print('\t');
	Serial.print(leftWheel.getMotorOutput());
	Serial.print("\t|\t");
	Serial.print(rightWheel.getDs());
	Serial.print('\t');
	Serial.print(rightWheel.getMeasuredSpeed());
	Serial.print('\t');
	Serial.println(rightWheel.getMotorOutput());
}

void plotPIDcontrol() {
	plot6(Serial, leftWheel.getDs(), (int ) leftWheel.getMeasuredSpeed(),
			(int ) leftWheel.getMotorOutput(), rightWheel.getDs(),
			(int ) rightWheel.getMeasuredSpeed(),
			(int ) rightWheel.getMotorOutput());
}

void printPinValue(uint8_t pinNumber) {
	Serial.print("PV: ");
	Serial.println(PinController::getInstance()->getPinValue(pinNumber));
}

///////////////////////// ONE CALL FUNCTIONS /////////////////////////

void getNumberOfPinsAviableToSet() {
	// Serial.print("Number of pins available (software coded) to set is: ");
	Serial.print("NPA: ");
	Serial.println(PinController::getInstance()->getNumberOfPinsAviable());
}

void printFreeMemory() {
	Serial.print("I|cF|fm|FM");
	Serial.println(freeMemory());
}

void printPIDParamsL() {
	Serial.print("PIDp: ");
	Serial.print(leftWheel.getKp());
	Serial.print(" ");
	Serial.print(leftWheel.getKd());
	Serial.print(" ");
	Serial.println(leftWheel.getKi());
}

void printPIDParamsR() {
	Serial.print("PIDp: ");
	Serial.print(rightWheel.getKp());
	Serial.print(" ");
	Serial.print(rightWheel.getKd());
	Serial.print(" ");
	Serial.println(rightWheel.getKi());
}
