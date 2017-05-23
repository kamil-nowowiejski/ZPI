/*
 * PinController.h
 *
 *  Created on: 28.10.2016
 *      Author: TTYBISZE
 */

#ifndef PINCONTROLLER_H_
#define PINCONTROLLER_H_

#include "Arduino.h"

#define NUMBER_OF_PINS_AVIABLE (NUM_DIGITAL_PINS+NUM_ANALOG_INPUTS)

// PIN convention for Arduino Leonardo:
// Analog input pins A0-A5, A6 - A11 (on digital pins 4, 6, 8, 9, 10, and 12):
// #define PIN_A0   (18)
// #define PIN_A1   (19)
// #define PIN_A2   (20)
// #define PIN_A3   (21)
// #define PIN_A4   (22)
// #define PIN_A5   (23)
// #define PIN_A6   (24) // A6-A11 shared with digital pins
// #define PIN_A7   (25)
// #define PIN_A8   (26)
// #define PIN_A9   (27)
// #define PIN_A10  (28)
// #define PIN_A11  (29)
// Digital pins:
// numbers from 0 till 13
// in this special pins:
// 	pwm: 3, 5, 6, 9, 10, 11, 13
// 	interrupt : 0, 1, 2, 3, 7 (https://www.arduino.cc/en/Reference/AttachInterrupt)
// info based on pins_arduino.h and https://www.arduino.cc/en/Main/ArduinoBoardLeonardo
// or https://www.dfrobot.com/wiki/index.php/Romeo_V2-All_in_one_Controller_(R3)_(SKU:DFR0225)
// DIGITAL_INPUT type is with pullup resistor
// analog pins can be set to an output (https://www.arduino.cc/en/Tutorial/AnalogInputPins)
enum PIN_TYPE {
	NO_FUNC_PIN,
	DIGITAL_OUTPUT,
	DIGITAL_INPUT,
	DIGITAL_INPUT_NO_PULLUP,
	PWM_PIN,
	ANALOG_INPUT,
	ANALOG_OUTPUT
};

// Pinout configuration should be set at the beginning
// sent as a configuration data
// reserved pins cannot change their purpose - a reset and new configuration send needed
class PinController {
private:
	PIN_TYPE pinsUsage[NUMBER_OF_PINS_AVIABLE] = { NO_FUNC_PIN };
	static PinController *pinControllerInstance;
public:
	static PinController* getInstance();
	bool setPinUsage(uint8_t pinNumber,	PIN_TYPE pinType);
	bool setPinUsage(uint8_t pinNumber,	String pinType);
	PIN_TYPE getPinUsage(uint8_t pinNumber);
	int getNumberOfPinsAviable();
	bool setPinState(uint8_t pinNumber, uint8_t state);
	int getPinValue(uint8_t pinNumber);
	bool setPWM(uint8_t pinNumber, int value);
	const String getTypeAsString(PIN_TYPE type);
};

#endif /* PINCONTROLLER_H_ */
