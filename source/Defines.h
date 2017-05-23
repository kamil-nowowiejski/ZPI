/*
 * Defines.h
 *
 *  Created on: 28.10.2016
 *      Author: TTYBISZE
 */

#ifndef DEFINES_H_
#define DEFINES_H_

#define MAX_RECEIVED_STRING_LEN 100

#define encoder0PinA  2
#define encoder0PinB  8

#define encoder1PinA  3
#define encoder1PinB  9

extern volatile unsigned long leftEncoderCounter;
extern volatile unsigned long rightEncoderCounter;

void countImpulsesInterrupt0();
void countImpulsesInterrupt1();

// only one direction PIN is sufficient due to logic gates mounted on board
#define motorLPWMPin 5 // from schematic to ROMEO D5
#define motorLDirPin 4 // from schematic to ROMEO D4

#define motorRPWMPin 6 // from schematic to ROMEO D6
#define motorRDirPin 11 // from schematic to ROMEO D7


// Ultrasonic distance sensor:
#define distanceSensorInterruptPin 7
#define distanceSensorSignalPin 10

// Ultrasonic distance sensor2:
#define distanceSensor2EchoPin 13
#define distanceSensor2TrgPin 12

extern volatile bool isDistanceSensorDataReady;
extern volatile unsigned long distanceSensorSignalDuration;
extern volatile unsigned long distanceSensorTriggerTime;

void distanceSensorInterrupt();

#endif /* DEFINES_H_ */
