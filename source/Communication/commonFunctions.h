/*
 * commonFunctions.h
 *
 *  Created on: 05.11.2016
 *      Author: Tomek
 */

#ifndef SOURCE_COMMONFUNCTIONS_H_
#define SOURCE_COMMONFUNCTIONS_H_

#include "../PinControl/PinController.h"
#include "../MotorControl/MotorSpeedController.h"
#include "../Simplot/Simplot.h"

void blinkLed();
void printEncoderValues();
void plotEncoderValues();
void printPIDcontrol();
void plotPIDcontrol();
void printFreeMemory();
void printPIDParamsL();
void printPIDParamsR();
void printPinValue(uint8_t pinNumber);

void getNumberOfPinsAviableToSet();

#endif /* SOURCE_COMMONFUNCTIONS_H_ */
