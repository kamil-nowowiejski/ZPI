/*
 * Defines.cpp
 *
 *  Created on: 28.10.2016
 *      Author: TTYBISZE
 */

#include "Defines.h"

#include "Arduino.h"

volatile unsigned long leftEncoderCounter = 0;
volatile unsigned long rightEncoderCounter = 0;

volatile bool isDistanceSensorDataReady = false;
volatile unsigned long distanceSensorSignalDuration = 0;
volatile unsigned long distanceSensorTriggerTime;

void countImpulsesInterrupt0() {
	// If pinA and pinB are both high or both low, it is spinning forward.
	// If they're different, it's going backward.

	(digitalRead(encoder0PinA) ^ digitalRead(encoder0PinB)) ?
			leftEncoderCounter-- : leftEncoderCounter++;
}

void countImpulsesInterrupt1() {
	// If pinA and pinB are both high or both low, it is spinning forward.
	// If they're different, it's going backward.

	(digitalRead(encoder1PinA) ^ digitalRead(encoder1PinB)) ?
			rightEncoderCounter-- : rightEncoderCounter++;
}

void distanceSensorInterrupt() {
	if (digitalRead(distanceSensorInterruptPin) == LOW) {
		distanceSensorTriggerTime = micros();
	} else {
		isDistanceSensorDataReady = true;
		distanceSensorSignalDuration = (micros() - distanceSensorTriggerTime);
	}
}
