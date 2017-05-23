/*
 * serialInterpreter.h
 *
 *  Created on: 04.11.2016
 *      Author: Tomek
 */

#ifndef SOURCE_SERIALINTERPRETER_H_
#define SOURCE_SERIALINTERPRETER_H_

#include "Arduino.h"

bool interpreteMessage(String &json);
//bool interpreteMessage(String &asd);
bool interpretePinCTRL(const String &json, uint8_t &pos, String &key, String &value);
bool interpreteTask(const String &json, uint8_t &pos, String &key, String &value);
bool interpreteAgentCTRL(const String &json, uint8_t &pos, String &key, String &value);
bool interpreteMotorCTRL(const String &json, uint8_t &pos, String &key, String &value, bool leftMotor);
bool interpreteQuestion(const String &json, uint8_t &pos, String &key, String &value);

#endif /* SOURCE_SERIALINTERPRETER_H_ */
