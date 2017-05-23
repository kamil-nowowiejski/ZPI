/*
 * MotorSpeedController.h
 *
 *  Created on: 25.10.2016
 *      Author: Tomek
 */

#ifndef MOTORSPEEDCONTROLLER_H_
#define MOTORSPEEDCONTROLLER_H_

#include "Encoder.h"
#include "Motor.h"

#define outMax 250
#define outMin 0

class MotorSpeedController {
private:
	// ControlState for MotorSpeedController
	// when CONTROL_DISABLED function controllSpeed() does nothing
	enum ControlState {
		CONTROL_ENABLED, CONTROL_DISABLED
	};

	ControlState controlState = CONTROL_DISABLED;

	unsigned long lastTime;
	unsigned long encoderPreviousValue = 0;
	double lastMeasuredSpeed;
	double ITerm;

	int ds = 0; // distance change in time dt (since the last )

	// Regulation Parameters (double>=0)
	double Kp = 0.01;
	double Kd = 0.05;
	double Ki = 0.002;

	int sampleTime = 100; // a default value the same like in PID.h

	double measuredSpeed = 0; // [imp/s]
	double motorOutput = 0; // PWM [0-255]
	double setSpeed = 0;

	Encoder* encoder = nullptr;
	Motor* motor;
public:
	void initializeController(uint8_t encPinA, uint8_t encPinB,
			volatile unsigned long &encoderCounter, uint8_t motPinPWM,
			uint8_t motPinDIR, double kp, double ki, double kd, int sampleTime);
	void controlSpeed();
	unsigned long getEncoderCounterValue() const;
	double getKd() const;
	void setKd(double kd);
	double getKi() const;
	void setKi(double ki);
	double getKp() const;
	void setKp(double kp);
	void setPIDParameters(double kp, double ki, double kd);
	void setSampleTime(int sampleTime);
	double getMeasuredSpeed() const;
	double getMotorOutput() const;
	double getSetSpeed() const;
	void setSetSpeed(double setSpeed);
	void setMotorPWMvalue(int val);
	void changeMotorDirection();
	void stopMotor();
	String getControlState();
	void enableController();
	void disableController();
	int getDs() const;
	void clearITerm();
};

#endif /* MOTORSPEEDCONTROLLER_H_ */
