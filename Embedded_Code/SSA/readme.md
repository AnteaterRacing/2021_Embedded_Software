## Name: Suspension Sensor Array
### Engineers: 
Andrew Kettle, Jada Berenguer, Leslie Uribe, and Micheal Barbosa

## Description:
- Data acquisition module for Ampeater v1. Integrates 3 IR sensors, 1 IMU, and a hall effect sensor.
- IR sensors are used for reading tire temperatures. The tire is measured at three different points; the inside, middle, and outside. 
- The IMU is used to measure acceleration and gyro data. 
- The hall effect sensor is used with 2 magnets to estimate tire speed. 




## Getting Started:
1) Install Visual Studio Code
2) Install Platformio extension 
   1) click the extension icon on the left
   2) find platformio ide
   3) click install
   - ![platformio installation](readme_src/platformio-installation.png)
3) Open the Platformio project 
   1) click the platformio icon on the left
   2) click open (under PIO home)
   3) click open project, and navigate to SSA root directory
   4) Platformio should install the necessary dependencies for you
   - ![image](readme_src/platformio-interface.png)
4) Build with tick button in the bottom left 
   - ![image](readme_src/build-button.png)