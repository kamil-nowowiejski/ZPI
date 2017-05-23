/*
 * MotorSpeedController.cpp
 *
 *  Created on: 12.11.2016
 *      Author: TTYBISZE
 */

#include "MotorSpeedController.h"

void MotorSpeedController::initializeController(uint8_t encPinA,
		uint8_t encPinB, volatile unsigned long &encoderCounter,
		uint8_t motPinPWM, uint8_t motPinDIR, double kp, double ki, double kd,
		int sampleTime) {
	encoder = initializeEncoder(encPinA, encPinB, encoderCounter);
	motor = new Motor(motPinPWM, motPinDIR);

	Kp = kp;
	Kd = ki;
	Ki = kd;

	this->sampleTime = sampleTime;

	ITerm = 0;

	lastTime = millis() - sampleTime;
	// Serial.println("INFO: Motor controller was successfully initialized!");
	Serial.println("I|MSC|iC|succ");
}

void MotorSpeedController::controlSpeed() {
	if (controlState == CONTROL_ENABLED) {
		unsigned long now = millis();
		int timeChange = (now - lastTime);
		if (timeChange >= sampleTime) {
			unsigned long encoderCounterValue = encoder->getCounterValue();

			if (timeChange > (1.5 * sampleTime)) {
				// Serial.println("WARNING! dt for control speed was higher than (1,5 * sampleTime).");
				Serial.print("W|MSC|cS|dth"); // dt to long
				Serial.println(timeChange);
			}

			ds = encoderCounterValue - encoderPreviousValue;
			if(ds < 0) {
				ds = (-1) * ds;
			}
			measuredSpeed = (ds) * (1000.0 / timeChange); // [imp/s]

			lastTime = now;

			encoderPreviousValue = encoderCounterValue;

			// Real PID regulation calculation:
			double error = setSpeed - measuredSpeed;

			if(error > 0) {
				ITerm += (Ki * error);
				if (ITerm > outMax) {
					ITerm = outMax;
				} else if (ITerm < outMin) {
					ITerm = outMin;
				}

				// Compute PID Output:
				motorOutput = Kp * error + ITerm
						- Kd * (measuredSpeed - lastMeasuredSpeed);

				if (motorOutput > outMax) {
					motorOutput = outMax;
				} else if (motorOutput < outMin) {
					motorOutput = outMin;
				}

				lastMeasuredSpeed = measuredSpeed;
			}
			else {
				motorOutput = 0;
			}

			motor->setMotorPWMvalue(motorOutput);
		}
	}
}

unsigned long MotorSpeedController::getEncoderCounterValue() const {
	return encoder->getCounterValue();
}

double MotorSpeedController::getKd() const {
	return Kd;
}

void MotorSpeedController::setKd(double kd) {
	Kd = kd;
}

double MotorSpeedController::getKi() const {
	return Ki;
}

void MotorSpeedController::setKi(double ki) {
	Ki = ki;
}

double MotorSpeedController::getKp() const {
	return Kp;
}

void MotorSpeedController::setKp(double kp) {
	Kp = kp;
}

void MotorSpeedController::setPIDParameters(double kp, double ki, double kd) {
	Kp = kp;
	Ki = ki;
	Kd = kd;
	/*Serial.println("INFO: Parameters set to ");
	 Serial.print(kp);
	 Serial.print(", ");
	 Serial.print(ki);
	 Serial.print(", ");
	 Serial.print(kd);
	 Serial.println('.');*/
	Serial.println("I|MSC|sPID|succ"); // parameters set successfully
}

// sets the frequency, in Milliseconds, with which
// the PID calculation is performed.  default is 100
void MotorSpeedController::setSampleTime(int sampleTime) {
	this->sampleTime = sampleTime;
}

double MotorSpeedController::getMeasuredSpeed() const {
	return measuredSpeed;
}

double MotorSpeedController::getMotorOutput() const {
	return motorOutput;
}

double MotorSpeedController::getSetSpeed() const {
	return setSpeed;
}

void MotorSpeedController::setSetSpeed(double setSpeed) {
	if (setSpeed >= 0) {
		motor->setDirectionForward();
		this->setSpeed = setSpeed;
	} else {
		motor->setDirectionBackward();
		this->setSpeed = (-1) * setSpeed;
	}
}

void MotorSpeedController::setMotorPWMvalue(int val) {
	disableController();
	motor->setMotorPWMvalue(val);
}

void MotorSpeedController::changeMotorDirection() {
	motor->changeDirection();
}

void MotorSpeedController::stopMotor() {
	motor->stopMotor();
}

String MotorSpeedController::getControlState() {
	if (controlState == CONTROL_ENABLED) {
		return "CONTROL_ENABLED";
	}
	return "CONTROL_DISABLED";
}

void MotorSpeedController::enableController() {
	//encoderPreviousValue = encoder->getCounterValue();
	//lastMeasuredSpeed = measuredSpeed; // because, when controller is disabled, motor speed is 0
	//ITerm = motorOutput;
	controlState = CONTROL_ENABLED;
}

void MotorSpeedController::disableController() {
	controlState = CONTROL_DISABLED;
}

int MotorSpeedController::MotorSpeedController::getDs() const {
	return ds;
}

void MotorSpeedController::clearITerm() {
	ITerm = 0;
	lastMeasuredSpeed = 0;
	ds = 0;
	measuredSpeed = 0;
	motorOutput = 0;
}
