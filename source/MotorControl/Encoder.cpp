/*
 * Encoder.cpp
 *
 *  Created on: 28.10.2016
 *      Author: TTYBISZE
 */

#include "Encoder.h"

#include "../PinControl/PinController.h"

uint8_t Encoder::encoderInstanceCounter = 0;

Encoder* initializeEncoder(uint8_t a, uint8_t b, volatile unsigned long &counterValue) {
	return new Encoder(a, b, counterValue);
}

Encoder::Encoder(uint8_t encoderPinA, uint8_t encoderPinB, volatile unsigned long &cv) {
	counterValue = &cv;

	PinController::getInstance()->setPinUsage(encoderPinA, DIGITAL_INPUT);
	PinController::getInstance()->setPinUsage(encoderPinB, DIGITAL_INPUT);

	Serial.print("Encoder no counter: ");
	Serial.println(encoderInstanceCounter );

	switch (encoderInstanceCounter) {
	case 0: {
		attachInterrupt(1, countImpulsesInterrupt0, CHANGE);
		break;
	}
	case 1: {
		attachInterrupt(0, countImpulsesInterrupt1, CHANGE);
		encoderInstanceCounter++;
		break;
	}
	default: {
		// Serial.println("SEVERE! No more encoders can be added!");
		Serial.println("S|E|E|nme"); // no more encoders
	}
	}
	encoderInstanceCounter++;
}

volatile unsigned long Encoder::getCounterValue() const {
	return *counterValue;
}

