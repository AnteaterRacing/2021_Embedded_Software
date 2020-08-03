#ifndef _WHEELSPEED_
#define _WHEELSPEED_

#include "Wire.h"
#include "Energia.h"

void wheelspeedSetup();
float wheelspeedCalc(float time_difference_micro); //delete print statements after testing
float getwheelspeedData();
int Read_Hall();
int initiateTimer();
int end_Timer();
int wheel_speed();

#endif
