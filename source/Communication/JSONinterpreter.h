/*
 * JSONinterpreter.h
 *
 *  Created on: 12.11.2016
 *      Author: TTYBISZE
 */

#ifndef SOURCE_JSONINTERPRETER_H_
#define SOURCE_JSONINTERPRETER_H_

bool getNext(const String &json, uint8_t &pos, String &key, String &value) {
	bool nextPairOK = false;
	bool readingValue = false;

	key = "";
	value = "";

	while ((pos >= 0) && (pos < json.length()) && !nextPairOK) {
		char c = json[pos];
		if (!(c == ' ')) {
			if (c == ':') {
				readingValue = true; // set readingValue to true
			} else {
				if ((c == '}') || (c == ',')) {
					nextPairOK = true;
				} else {
					if (!((c == '{') || (c == '\"'))) {
						if (!readingValue) { // reading key
							key += c;
						} else {
							value += c;
						}
					}
				}
			}
		}
		pos++;
	}

	if ((key == "") || (value == "")) {
		nextPairOK = false;
	}
	//Serial.println(key);
	//Serial.println(value);

	return nextPairOK;
}

#endif /* SOURCE_JSONINTERPRETER_H_ */
