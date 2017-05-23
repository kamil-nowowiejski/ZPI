/*
 * distanceSensor.h
 *
 *  Created on: 20.11.2016
 *      Author: Tomek
 */

#ifndef SOURCE_DISTANCESENSOR_H_
#define SOURCE_DISTANCESENSOR_H_

#include <Arduino.h>
#include "Defines.h"

//////////////// For Ultrasonic distance sensor //////////////////////

// converts microseconds from distance sensor measurement to centimeters
float microsecondsToCentimeters(long microseconds) {
	// The speed of sound is 340 m/s or 29 microseconds per centimeter.
	// The ping travels out and back, so to find the distance of the
	// object we take half of the distance travelled.
	//return ((float)microseconds) / 29 / 2;
	return ((float)microseconds) / 50;
}

// the function that triggers the distance measurement
// should not be triggered more often than 150 ms
// measurement can last up to 100 ms!
void triggerDistanceSensorSignal() {
	PinController::getInstance()->setPinState(distanceSensorSignalPin, LOW); // Send low pulse
	PinController::getInstance()->setPinState(distanceSensorSignalPin, HIGH); // Send high pulse
}

// the function that triggers the distance measurement
// should not be triggered more often than 150 ms
// measurement can last up to 100 ms!
void triggerDistanceSensor2AndMeasure() {
	PinController::getInstance()->setPinState(distanceSensor2TrgPin, LOW); // Send low pulse
	delayMicroseconds(2); // Wait for 2 microseconds
	PinController::getInstance()->setPinState(distanceSensor2TrgPin, HIGH); // Send high pulse
	delayMicroseconds(10); // Wait for 10 microseconds
	PinController::getInstance()->setPinState(distanceSensor2TrgPin, LOW); // Holdoff

	long result;
	digitalWrite(12, LOW);
	delayMicroseconds(2);
	digitalWrite(12, HIGH);
	delayMicroseconds(10);
	digitalWrite(12, LOW);

	result = pulseIn(13, HIGH); // time
	result = result / 58; // distance in cm
	Serial.print("Dist2: ");
	Serial.println(result);
}

// attaches interrupt to the sensor
void initializeDistanceSensor() {
	pinMode(distanceSensorSignalPin, OUTPUT);
	pinMode(distanceSensorInterruptPin, INPUT);
	attachInterrupt(digitalPinToInterrupt(distanceSensorInterruptPin),
			distanceSensorInterrupt, CHANGE);
}

// attaches interrupt to the sensor
void initializeDistanceSensor2() {
	pinMode(distanceSensor2TrgPin, OUTPUT);
	pinMode(distanceSensor2EchoPin, INPUT_PULLUP);
}

// when the data are ready (measurement has finished), prints the distance out
// watch out that measurement needs to be triggered with function triggerDistanceSensorSignal()
void getDistanceSensorMeasurement() {
	if (isDistanceSensorDataReady) {
		// convert the time into a distance
		Serial.print("Dist1: ");
		Serial.println(microsecondsToCentimeters(distanceSensorSignalDuration));
		isDistanceSensorDataReady = false;
	}
	/*else
		Serial.println("no result");*/
}

#endif /* SOURCE_DISTANCESENSOR_H_ */
