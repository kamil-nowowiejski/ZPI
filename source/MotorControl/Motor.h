/*
 * Motor.h
 *
 *  Created on: 25.10.2016
 *      Author: Tomek
 */

#ifndef MOTOR_H_
#define MOTOR_H_

#include <Arduino.h>

#include "../PinControl/PinController.h"

// https://www.dfrobot.com/wiki/index.php/Romeo_V2-All_in_one_Controller_(R3)_(SKU:DFR0225)
class Motor {

private:
	// only one drive direction PIN is sufficient due to logic gates mounted on board
	uint8_t pwmPin;
	uint8_t dirPin;
public:
	Motor(uint8_t pwm, uint8_t dir) {
		setMotorPins(pwm, dir);
		initializeMotorPins();
	}
	void setMotorPins(uint8_t pwm, uint8_t dir) {
		pwmPin = pwm;
		dirPin = dir;
	}
	void initializeMotorPins() {
		// pinMode(pwmPin, OUTPUT);
		// pinMode(dirPin, OUTPUT);
		// digitalWrite(dirPin, LOW); // default value, default direction
		PinController::getInstance()->setPinUsage(pwmPin, PWM_PIN);
		PinController::getInstance()->setPinUsage(dirPin, DIGITAL_OUTPUT);
		PinController::getInstance()->setPinState(dirPin, LOW);
		setDirectionForward();
	}
	void stopMotor() {
		analogWrite(pwmPin, 0);
	}
	void setMotorPWMvalue(int pwm) {
		analogWrite(pwmPin, pwm);
	}
	void changeDirection() {
		if (digitalRead(dirPin) == LOW)
			setDirectionForward();
		else
			setDirectionBackward();
	}
	void setDirectionForward() {
		PinController::getInstance()->setPinState(dirPin, LOW);
	}
	void setDirectionBackward() {
		PinController::getInstance()->setPinState(dirPin, HIGH);
	}
};

#endif /* MOTOR_H_ */
