#ifndef _SD_
#define _SD_
/*
   Written and maintained by: 
   Andrew Kettle
   September 27th, 2020
*/
#include <stdint.h>
#include "SdFat.h"
#include "imu.h"

class SD {

   // static members and methods
   public:
      const static char* file_count_name;

   public:
      SD();

      bool initSD();
      void SdRemove();
      bool SdWriteHeader();
      bool SdWrite(IMU imu, float t1, float t2, float t3, float ws);
   
   private:    // private helper functions
      void createNewDataFile();
      int getNumFiles();
      // this function allows writing of various types
      template<typename T> bool writeElements(const T* elements, int num_elements);

   private:    // private member variables
      SdFatSdio SDCARD;          //SD card object
      bool file_has_data;        //state boolean
      char file_name[13];        //small buffer size
};
#endif