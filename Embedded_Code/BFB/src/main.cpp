#include <Arduino.h>

const int FAULT_PIN = 21;
const int INPUT_PINS[] = {14,15,16,17,18,19,20,21,22,23,31,32,33,34,35,36,37,38,39};

bool shouldTurnLedOn;

void setup() {
	// the FAULT_PIN is the pin where the output signal is high
	// if any of the temperatures are above the threshold.
	pinMode(FAULT_PIN, OUTPUT);

	// set analog pins to input
	for(int pin: INPUT_PINS) {
		pinMode(pin, INPUT);
	}
}


// this analog value ranges from 0-1023
// it corresponds to a temperature value
// if this value is over the threshold, set
// shouldTurnLedOn to true
//
// according to the datasheet, the voltage is
// is 2.17 at 0  degC and increases as C decreases
// is 1.51 at 60 degC and decreases as C increases
// therefore if voltage > 2.17 or voltage < 1.51, then
// we have a temperature fault
void checkThreshold(unsigned int analogVal) {
	double voltage = 3.3 * (analogVal / 1023.0);
	if(voltage < 1.51 || voltage > 2.17) {
		shouldTurnLedOn = true;
	}
}


// checks all 26 lines. If any of them are not in
// proper operating range, a fault LED is enabled
void loop() {
	shouldTurnLedOn = false;
	for(int pinNum: INPUT_PINS) {
		unsigned int value = analogRead(pinNum);
		checkThreshold(value);
	}
	// if there is a fault, output low
	digitalWrite(FAULT_PIN, shouldTurnLedOn? LOW: HIGH);
}