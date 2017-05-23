/*
 * Encoder.h
 *
 *  Created on: 27.10.2016
 *      Author: Tomek
 */

#ifndef ENCODER_H_
#define ENCODER_H_

#include <Arduino.h>
#include "../Defines.h"

class Encoder {
private:
	volatile unsigned long *counterValue;

	static uint8_t encoderInstanceCounter;

	Encoder(uint8_t a, uint8_t b, volatile unsigned long &cv);
public:
	friend Encoder* initializeEncoder(uint8_t encoderPinA, uint8_t encoderPinB,
			volatile unsigned long &counterValue);
	volatile unsigned long getCounterValue() const;
};

Encoder* initializeEncoder(uint8_t a, uint8_t b,
		volatile unsigned long &counterValue);

#endif /* ENCODER_H_ */
