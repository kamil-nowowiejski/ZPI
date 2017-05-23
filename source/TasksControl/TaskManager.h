/*
 * TaskManager.h
 *
 *  Created on: 30.10.2016
 *      Author: Tomek
 */

#ifndef TASKMANAGER_H_
#define TASKMANAGER_H_

// edit carefully to do not to run out of Arduino memory
#define MAX_NUMBER_OF_TASKS 5

#include "ScheduledTask.h"
#include "ScheduledTaskWithIntParam.h"

class TaskManager {
private:
	static uint8_t taskCounter;
	ScheduledTask tasks[MAX_NUMBER_OF_TASKS];
	static TaskManager *taskManagerInstance;

	uint8_t checkIfTaskExists(uint8_t id);
public:
	static TaskManager* getInstance();
	bool addTask(uint8_t id, unsigned long sampleTime, void (*taskFunction)(void));
	bool addTask(uint8_t id, unsigned long sampleTime, void (*taskFunction)(uint8_t), uint8_t intParam);
	bool deactivateTask(uint8_t id);
	void realizeTasks();
};

#endif /* TASKMANAGER_H_ */
