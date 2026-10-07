#include "ibus.h"
#include <MPU6050_tockn.h>
#include <Wire.h>


//Inicialize Gyro
MPU6050 mpu6050(Wire);


//vJoySerialFeeder comunication update,dont mess here.
#define UPDATE_INTERVAL 10 

//Serial Comunication baud rate
#define BAUD_RATE 115200 

//Total of channels for the vJoySerialFeeder to read 
#define NUM_CHANNELS 1 

//E aqui esse valor informa quantos canais vão receber os dados dos botões e analógicos por voce controlados
IBus ibus(NUM_CHANNELS);

//Inicialize angle y reads
float zeroY=180;
float zeroX = 180;

void setup()
{
//Serial comunication Starts
  Serial.begin(BAUD_RATE);
  //I2C Accel/Gyro comunication with Arduino Starts
  Wire.begin();
  mpu6050.begin();
 //Autocalibration for the sensor,optional
  mpu6050.calcGyroOffsets(false);
}


void loop()

{
 
//Accel/Gyro Readings

   mpu6050.update();
   float y=mpu6050.getAngleY(); //Movement Axis measured is Y
   y+=zeroY;
   //Serial.println(y);

   float x = mpu6050.getAngleX();
   x += zeroX;


//Serial Comunication Intensifies...
int i, bm_ch = 0;
  unsigned long time = millis();
       ibus.begin();
  
//State of buttons,and analog readings are delivered to the vJoySerialFeeder
     ibus.write(y);
     ibus.write(x);
     ibus.end();

    time = millis() - time; // time elapsed in reading the inputs
    if(time < UPDATE_INTERVAL)
    // sleep till it is time for the next update
    delay(UPDATE_INTERVAL  - time);

}
  
