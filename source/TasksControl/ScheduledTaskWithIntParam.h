/*
 * ScheduledTask.h
 *
 *  Created on: 29.10.2016
 *      Author: TTYBISZE
 */

#ifndef SCHEDULEDTASKWITHINTPARAM_H_
#define SCHEDULEDTASKWITHINTPARAM_H_

#include "Arduino.h"
#include "ScheduledTask.h"

// to use this class:
// 1. method realizeTask needs to be virtual
// 2. TaskManager needs to operate on array of pointers to ScheduledTask
// 3. Memory management in cases of deleting and creating tasks needs to be implemented
class ScheduledTaskWithIntParam : public ScheduledTask {
private:
	uint8_t id;
	bool activated;
	unsigned long sampleTime; // sampling time in milliseconds
	void (*functionPointer)(uint8_t);
	uint8_t intParam; // only needed for tasks with reading pin value

	unsigned long lastTime;
public:

	/*ScheduledTaskWithIntParam() {
		id = -1;
		sampleTime = -1;
		functionPointer = nullptr;
		lastTime = -1;
		activated = false;
		intParam = 0;
	}
	ScheduledTaskWithIntParam(uint8_t id, unsigned long sampleTime, void (*taskFunction)(uint8_t), uint8_t intParam) {
		this->id = id;
		this->sampleTime = sampleTime;
		functionPointer = taskFunction;

		activated = true;
		lastTime = millis() - sampleTime;
		this->intParam = intParam;
	}
	bool realizeTask() {
		unsigned long now = millis();
		unsigned long timeChange = (now - lastTime);
		if (timeChange >= sampleTime) {
			lastTime = now;
			functionPointer(intParam);
			return true;
		}
		return false;
	}
	uint8_t getId() const{
		return id;
	}

	bool isActivated() const {
		return activated;
	}

	void setActivated(bool activated = true) {
		this->activated = activated;
	}*/
};

#endif /* SCHEDULEDTASK_H_ */
