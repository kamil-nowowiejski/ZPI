/*
 * TaskManager.cpp
 *
 *  Created on: 30.10.2016
 *      Author: Tomek
 */

#include "TaskManager.h"

uint8_t TaskManager::taskCounter = 0;
TaskManager *TaskManager::taskManagerInstance = nullptr;

TaskManager* TaskManager::getInstance() {
	if (taskManagerInstance == nullptr) {
		taskManagerInstance = new TaskManager();
	}
	return taskManagerInstance;
}

// adds task to the task list performed every sampleTime in milliseconds
// a function has no parameter
bool TaskManager::addTask(uint8_t id, unsigned long sampleTime,
		void (*taskFunction)(void)) {
	bool result = false;
	int indexOfExistingTask = checkIfTaskExists(id);
	if ((indexOfExistingTask >= 0) && (indexOfExistingTask < taskCounter)) {
		tasks[indexOfExistingTask] = ScheduledTask(id, sampleTime,
				taskFunction);
		Serial.println("I|TM|aT|tu"); // Task has been updated
		result = true;
	} else if (taskCounter < MAX_NUMBER_OF_TASKS) {
		tasks[taskCounter] = ScheduledTask(id, sampleTime, taskFunction);
		Serial.print("I|TM|aT|tc"); // Task has been created
		Serial.println(id);
		taskCounter++;
		result = true;
	} else {
		Serial.print("I|TM|at|nt");
		Serial.println(MAX_NUMBER_OF_TASKS); // No more than MAX_NUMBER_OF_TASKS can be added
	}
	return result;
}

// To use this function please have a look into comment in ScheduledTaskWithIntParam class file
// adds a task to the task list performed every sampleTime in milliseconds
// a function has int parameter
bool TaskManager::addTask(uint8_t id, unsigned long sampleTime,
		void (*taskFunction)(uint8_t), uint8_t intParam) {
	bool result = false;
	/*int indexOfExistingTask = checkIfTaskExists(id);
	// already existing task or new but with already used id
	if ((indexOfExistingTask >= 0) && (indexOfExistingTask < taskCounter)) {
		tasks[indexOfExistingTask] = ScheduledTaskWithIntParam(id, sampleTime,
				taskFunction, intParam);
		Serial.println("I|TM|aT|tu"); // Task has been updated
		result = true;
	} else if (taskCounter < MAX_NUMBER_OF_TASKS) { // new task
		tasks[taskCounter] = ScheduledTaskWithIntParam(id, sampleTime, taskFunction, intParam);
		Serial.print("I|TM|aT|tc"); // Task has been created
		Serial.println(id);
		taskCounter++;
		result = true;
	} else {
		Serial.print("I|TM|at|nt");
		Serial.println(MAX_NUMBER_OF_TASKS); // No more than MAX_NUMBER_OF_TASKS can be added
	}*/
	return result;
}

//removes task from a list
bool TaskManager::deactivateTask(uint8_t id) {
	bool result = false;
	uint8_t indexOfExistingTask = checkIfTaskExists(id);
	if ((indexOfExistingTask >= 0) && (indexOfExistingTask < taskCounter)) {
		tasks[indexOfExistingTask].setActivated(false);
		result = true;
	}
	return result;
}

// realizes all previously added tasks
void TaskManager::realizeTasks() {
	for (int i = 0; i < taskCounter; ++i) {
		if (tasks[i].isActivated() == true) {
			tasks[i].realizeTask();
		}
	}
}

// if the task with provided id already exists, its parameters will be updated, while adding task
uint8_t TaskManager::checkIfTaskExists(uint8_t id) {
	for (int i = 0; i < taskCounter; ++i) {
		if (tasks[i].getId() == id) {
			Serial.print("I|TM|ct|te"); // Task exists on index
			Serial.println(id);
			return i;
		}
	}
	Serial.println("I|TM|ct|nf"); // No task with provided id was found
	return -1;
}
