/*
   Written and maintained by: 
   Andrew Kettle
   November 14th, 2019
*/

//headers:

#include "Wire.h"

//Functions:
void I2C_init();
void getI2CData();
int16_t convert_16bit(int8_t high, int8_t low);
float accel_conversion(int16_t rawaccel);
float gyro_conversion(int16_t rawgyro);
void printData(float accelx, float accely, float accelz, float gyrox, float gyroy, float gryox);

//pin declerations
int sda = P2_2; //I2C pins
int scl = P2_1;

//registers
#define lsm9ds1_ag 0x6B //device reg

#define gyro_control1 0x10 //Control of the gyro reg
#define accel_control4 0x1E //Control of the accel reg4
#define accel_control5 0x1F //Control of the accel reg5
#define accel_control7 0x21 //Control of the accel reg5
#define mag_pwr 0x16 //the register that powers the mangetometer
//#define strt (0xD4>>1)
#define strtw 0xD6 //send before write?
#define strtr 0xD5

#define gyroX0 0x18 //accel output registerss
#define gyroX1 0x19
#define gyroY0 0x1A
#define gyroY1 0x1B
#define gyroZ0 0x1C
#define gyroZ1 0x1D

#define accelX0 0x28 //accel output registerss
#define accelX1 0x29
#define accelY0 0x2A
#define accelY1 0x2B
#define accelZ0 0x2C
#define accelZ1 0x2D

void setup() {

  I2C_init(); //initialize I2C transmission
  Serial.begin(9600);
}

void loop() {

  //Reading IMU
  getI2CData();
  Serial.flush();
}

void I2C_init()
{ 
  pinMode(scl, INPUT_PULLUP);
  pinMode(sda, INPUT_PULLUP);
  Wire.begin(); //initialize i2c transmission
  Wire.beginTransmission(lsm9ds1_ag);
  //init power modes
  Wire.write(gyro_control1); //Control register for gyro
  Wire.write(193); //Powers and set to 952 HZ, stock settings elsewhere, trial and error with filtering currently
  Wire.write(accel_control4);
  Wire.write(56); //Makes sure accel output is turned on
  Wire.write(accel_control5);
  Wire.write(56); 
  Wire.write(accel_control7);
  Wire.write(164);
	
  Wire.endTransmission();
}

void getI2CData() 
{

  int16_t rawaccelx, rawaccely, rawaccelz, rawgyrox, rawgyroy, rawgyroz;
  float convaccelx, convaccely, convaccelz, convgyrox, convgyroy, convgyroz;
  int8_t gX0, gX1, gY0, gY1, gZ0, gZ1, aX0, aX1, aY0, aY1, aZ0, aZ1;

  Wire.beginTransmission(lsm9ds1_ag);
  
  Wire.write(gyroX0); //getting data from gyro registers
  Wire.write(gyroX1);
  Wire.write(gyroY0);
  Wire.write(gyroY1);
  Wire.write(gyroZ0);
  Wire.write(gyroZ1);
  
  Wire.write(accelX0); //getting data from accelerometer registers
  Wire.write(accelX1);
  Wire.write(accelY0);
  Wire.write(accelY1);
  Wire.write(accelZ0);
  Wire.write(accelZ1);

  Wire.endTransmission(true); //continue transmission until reading is done

  Wire.requestFrom(lsm9ds1_ag, 12); //requesting 12 bytes, 12 8 bit #'s, or 6 16 bit #'s
  
  if(Wire.available()<=12) 
  { 
    gX0 = Wire.read();
    gX1 = Wire.read();
    gY0 = Wire.read();
    gY1 = Wire.read();
    gZ0 = Wire.read();
    gZ1 = Wire.read();

    aX0 = Wire.read();
    aX1 = Wire.read();
    aY0 = Wire.read();
    aY1 = Wire.read();
    aZ0 = Wire.read();
    aZ1 = Wire.read();
  }

  Wire.endTransmission();

  rawgyrox = convert_16bit(gX0, gX1);
  rawgyroy = convert_16bit(gY0, gY1);
  rawgyroz = convert_16bit(gZ0, gZ1);
 
  rawaccelx = convert_16bit(aX0, aX1);
  rawaccely = convert_16bit(aY0, aY1);
  rawaccelz = convert_16bit(aZ0, aZ1);

  convgyrox = gyro_conversion(rawgyrox);
  convgyroy = gyro_conversion(rawgyroy);
  convgyroz = gyro_conversion(rawgyroz);

  convaccelx = accel_conversion(rawaccelx);
  convaccely = accel_conversion(rawaccely);
  convaccelz = accel_conversion(rawaccelz);

  printData(convaccelx, convaccely, convaccelz, convgyrox, convgyroy, convgyroz);	
}

//converts to 16 bit number
int16_t convert_16bit(int8_t high, int8_t low)
{
	int16_t sixteenbit = (high << 8) | low; 
	return sixteenbit;
}

//converts the 16 bit int into human understandable data
float accel_conversion(int16_t rawaccel)
{
	//raw unit is millig's/LSB (mg/LSB)
	//default sampling is +-2g, list of conversion factors on page 12 of datasheet

	float conv_factor = .061; //conversion factor for +-2g
	return (rawaccel * conv_factor) / 1000; //ouputs in standard g's
	
}

float gyro_conversion(int16_t rawgyro)
{
	//raw unit is millidps/LSB (mdps/LSB)
	//default sampling is +-245dps, list of conversion factors on page 12 of datasheet

	float conv_factor = 8.75; //conversion factor for +-2g
	return (rawgyro * conv_factor) / 1000; //ouputs in standard dps
	
}

void printData(float accelx, float accely, float accelz, float gyrox, float gyroy, float gyroz)
{
/*
  Serial.print("Gyro X = ");
  Serial.println(gyrox, 3); //prints 3 decimal places
  Serial.print("Gyro Y = ");
  Serial.println(gyroy, 3); //prints 3 decimal places
  Serial.print("Gyro Z = ");
  Serial.println(gyroz, 3); //prints 3 decimal places
*/

  //if((accelx > .500 || accelx < -.500) || (accely > .500 || accely < -.500) || (accelz > .500 || accelz < -.500)) //temporary filter for bad data
  //{
 	  Serial.print("Accel X = ");
  	Serial.println(accelx, 3); //prints 3 decimal places
  	Serial.print("Accel Y = ");
  	Serial.println(accely, 3); //prints 3 decimal places
  	Serial.print("Accel Z = ");
  	Serial.println(accelz, 3); //prints 3 decimal places
  	Serial.println("\n\n");
  //}

}
