/*
 * PinController.cpp
 *
 *  Created on: 28.10.2016
 *      Author: TTYBISZE
 */

#include "PinController.h"

PinController *PinController::pinControllerInstance = nullptr;

PinController* PinController::getInstance() {
	if (pinControllerInstance == nullptr) {
		pinControllerInstance = new PinController();
	}
	return pinControllerInstance;
}
// Sets pin usage:
// enum PIN_TYPE {NO_FUNC_PIN,DIGITAL_OUTPUT,DIGITAL_INPUT,DIGITAL_INPUT_NO_PULLUP,PWM_PIN,ANALOG_INPUT,ANALOG_OUTPUT}
bool PinController::setPinUsage(uint8_t pinNumber, PIN_TYPE pinType) {
	bool result = true;
	if (pinNumber < NUMBER_OF_PINS_AVIABLE) {
		pinsUsage[pinNumber] = pinType;
		switch (pinType) {
		case DIGITAL_OUTPUT: {
			pinMode(pinNumber, OUTPUT);
			break;
		}
		case DIGITAL_INPUT: {
			pinMode(pinNumber, INPUT);
			digitalWrite(pinNumber, HIGH);
			break;
		}
		case DIGITAL_INPUT_NO_PULLUP: {
			pinMode(pinNumber, INPUT);
			break;
		}
		case PWM_PIN: {
			pinMode(pinNumber, OUTPUT);
			break;
		}
		case ANALOG_INPUT: {
			// no setup needs to be done (https://www.arduino.cc/en/Reference/AnalogRead)
			break;
		}
		case ANALOG_OUTPUT: {
			pinMode(pinNumber, OUTPUT);
			break;
		}
		default: { // NO_FUNC_PIN
			// Serial.println("SEVERE! No function was assigned to the pin. Wrong type. setPinUsage failed");
			Serial.println("S|PC|sPU|wt"); // wrong type
			result = false;
			break;
		}
		}
		// Serial.print("INFO: Pin value was successfully set to ");
		// Serial.println(getTypeAsString(pinType));
		Serial.println("I|PC|sPU|succ"); // success
	} else {
		// Serial.println("SEVERE! Wrong pin number. There are not so many pins are available. setPinUsage failed");
		Serial.println("S|PC|sPU|pne"); // pin not exist
		result = false;
	}
	return result;
}
// Sets pin usage:
// enum PIN_TYPE {NO_FUNC_PIN,DIGITAL_OUTPUT,DIGITAL_INPUT,DIGITAL_INPUT_NO_PULLUP,PWM_PIN,ANALOG_INPUT,ANALOG_OUTPUT}
bool PinController::setPinUsage(uint8_t pinNumber, String pinType) {
	bool result = true;
	if (pinNumber < NUMBER_OF_PINS_AVIABLE) {
		if (pinType == "DIGITAL_OUTPUT") {
			pinsUsage[pinNumber] = DIGITAL_OUTPUT;
			pinMode(pinNumber, OUTPUT);
		} else if (pinType == "DIGITAL_INPUT") {
			pinsUsage[pinNumber] = DIGITAL_INPUT;
			pinMode(pinNumber, INPUT);
			digitalWrite(pinNumber, HIGH);
		} else if (pinType == "DIGITAL_INPUT_NO_PULLUP") {
			pinsUsage[pinNumber] = DIGITAL_INPUT_NO_PULLUP;
			pinMode(pinNumber, INPUT);
		} else if (pinType == "PWM_PIN") {
			pinsUsage[pinNumber] = PWM_PIN;
			pinMode(pinNumber, OUTPUT);
		} else if (pinType == "ANALOG_INPUT") {
			pinsUsage[pinNumber] = ANALOG_INPUT;
			// no setup needs to be done (https://www.arduino.cc/en/Reference/AnalogRead)
		} else if (pinType == "ANALOG_OUTPUT") {
			pinsUsage[pinNumber] = ANALOG_OUTPUT;
			pinMode(pinNumber, OUTPUT);
		} else { // NO_FUNC_PIN
			// Serial.println("SEVERE! No function was assigned to the pin. Wrong type. setPinUsage failed");
			Serial.println("S_PC_sPU_wt"); // wrong type
			result = false;
		}
		// Serial.print("INFO: Pin value was successfully set to ");
		// Serial.println(pinType);
		Serial.println("S_PC_sPU_succ"); // success
	} else {
		// Serial.println("SEVERE! Wrong pin number. There are not so many pins are available. setPinUsage failed");
		Serial.println("S_PC_sPU_pne"); // pin not exist
		result = false;
	}
	return result;
}
// Returns pin usage:
// enum PIN_TYPE {NO_FUNC_PIN,DIGITAL_OUTPUT,DIGITAL_INPUT,DIGITAL_INPUT_NO_PULLUP,PWM_PIN,ANALOG_INPUT,ANALOG_OUTPUT}
PIN_TYPE PinController::getPinUsage(uint8_t pinNumber) {
	if (pinNumber < NUMBER_OF_PINS_AVIABLE) {
		return pinsUsage[pinNumber];
	} else {
		// Serial.println("SEVERE! Wrong pin number. There are not so many pins are available. getPinUsage failed");
		Serial.println("S|PC|gPU|pne"); // pin not exist
	}
	return NO_FUNC_PIN;
}
// Returns number of pins aviable
int PinController::getNumberOfPinsAviable() {
	return NUMBER_OF_PINS_AVIABLE;
}
// Pin needs to be initialized firstly by function setPinUsage(uint8_t pinNumber, PIN_TYPE pinType)
// Sets pin value. State can be LOW or HIGH.
bool PinController::setPinState(uint8_t pinNumber, uint8_t state) {
	if (pinNumber < NUMBER_OF_PINS_AVIABLE) {
		if (pinsUsage[pinNumber] != DIGITAL_OUTPUT) {
			// Serial.print("WARNING! Changing pin ");
			// Serial.print(pinNumber);
			// Serial.print(" value from ");
			// Serial.print(getTypeAsString(pinsUsage[pinNumber]));
			// Serial.println(" to DIGITAL_OUTPUT.");
			// setPinUsage(pinNumber, DIGITAL_OUTPUT);
			Serial.print("W|PC|sPS|ch");
			Serial.print(pinsUsage[pinNumber]);
			Serial.print('|');
			Serial.println(DIGITAL_OUTPUT);

			pinsUsage[pinNumber] = DIGITAL_OUTPUT;
		}
		digitalWrite(pinNumber, state);
		return true;
	}
	// Serial.print("SEVERE! Wrong pin number. There are not so many pins are available. setPinState failed");
	Serial.println("S_PC_sPS_pne"); // pin not exist
	return false;
}

int PinController::getPinValue(uint8_t pinNumber) {
	if (pinNumber < NUMBER_OF_PINS_AVIABLE) {
		if ((pinsUsage[pinNumber] == DIGITAL_OUTPUT)
				|| (pinsUsage[pinNumber] == DIGITAL_INPUT_NO_PULLUP)) {
			return digitalRead(pinNumber);
		} else if ((pinsUsage[pinNumber] == PWM_PIN)
				|| (pinsUsage[pinNumber] == ANALOG_OUTPUT)) {
			return analogRead(pinNumber);
		} else {
			Serial.print("S|PC|gPV|wt"); // wrong type
			Serial.println(pinsUsage[pinNumber]);
		}
		return -1;
	}
	// Serial.print("SEVERE! Wrong pin number. There are not so many pins are available. setPinState failed");
	Serial.println("S_PC_gPV_pne"); // pin not exist
	return false;
}

// Pin needs to be initialized firstly by function setPinUsage(uint8_t pinNumber, PIN_TYPE pinType)
// Sets pin pwm output.
bool PinController::setPWM(uint8_t pinNumber, int value) {
	if (pinNumber < NUMBER_OF_PINS_AVIABLE) {
		if (!((pinsUsage[pinNumber] == PWM_PIN)
				|| (pinsUsage[pinNumber] == ANALOG_OUTPUT))) {
			// Serial.print("WARNING! Changing pin ");
			// Serial.print(pinNumber);
			// Serial.print(" value from ");
			// Serial.print(getTypeAsString(pinsUsage[pinNumber]));
			// Serial.print(" to PWM_PIN.");
			Serial.print("W|PC|sPWM|ch");
			Serial.print(pinsUsage[pinNumber]);
			Serial.print('|');
			Serial.println(PWM_PIN);

			setPinUsage(pinNumber, PWM_PIN);
		}
		analogWrite(pinNumber, value);
		return true;
	}
	// Serial.print("SEVERE! Wrong pin number. There are not so many pins are available. setPWM failed");
	Serial.println("S|PC|sPWM|pne"); // pin not exist
	return false;
}

const String PinController::getTypeAsString(PIN_TYPE type) {
	switch (type) {
	case NO_FUNC_PIN: {
		return "NO_FUNC_PIN";
	}
	case DIGITAL_OUTPUT: {
		return "DIGITAL_OUTPUT";
	}
	case DIGITAL_INPUT: {
		return "DIGITAL_INPUT";
	}
	case DIGITAL_INPUT_NO_PULLUP: {
		return "DIGITAL_INPUT_NO_PULLUP";
	}
	case PWM_PIN: {
		return "PWM_PIN";
	}
	case ANALOG_INPUT: {
		return "ANALOG_INPUT";
	}
	case ANALOG_OUTPUT: {
		return "ANALOG_OUTPUT";
	}
	default: {
		return "";
	}
	}
	return "";
}
