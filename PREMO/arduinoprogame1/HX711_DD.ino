#include <HX711.h>

/*
  Setup your scale and start the sketch WITHOUT a weight on the scale
  Once readings are displayed place the weight on the scale
  Press +/- or a/z to adjust the calibration_factor until the output readings match the known weight
  Arduino pin 6 -> HX711 CLK
  Arduino pin 5 -> HX711 DOUT
  Arduino pin 5V -> HX711 VCC
  Arduino pin GND -> HX711 GND
*/

#include "HX711.h"

HX711 scale(5, 6);

float calibration_factor = 1940; // this calibration factor is adjusted according to my load cell
float units;
float ounces;
int temp = 0;
String inputString = "";
bool completeStr = false;
void setup() {
  Serial.begin(19200);
  inputString.reserve(10);
  //Serial.println("HX711 calibration sketch");
  //Serial.println("Remove all weight from scale");
  //Serial.println("After readings begin, place known weight on scale");
  //Serial.println("Press + or a to increase calibration factor");
  //Serial.println("Press - or z to decrease calibration factor");

  scale.set_scale();
  scale.tare();  //Reset the scale to 0

  long zero_factor = scale.read_average(); //Get a baseline reading
  //Serial.print("Zero factor: "); //This can be used to remove the need to tare the scale. Useful in permanent scale projects.
  //Serial.println(zero_factor);
}

void loop() {

  scale.set_scale(calibration_factor); //Adjust to this calibration factor

  //Serial.print("Reading: ");
  units = scale.get_units(), 1;
  units = units / 10;
  if (units < 0)
  {
    units = 0.00;
  }
  ounces = units * 0.035274;
  Serial.println(units);
  delay(temp);
  //Serial.print(" grams");
  //Serial.print(" calibration_factor: ");
  //Serial.print(calibration_factor);
  //Serial.println();
  if (completeStr)
  {
    if (!inputString.indexOf("t"))
    {
      inputString = inputString.substring(1);
      temp = inputString.toInt();
      inputString = "";
    }
    else if (!inputString.indexOf("c"))
    {
      inputString = inputString.substring(1);
      calibration_factor = inputString.toInt();
      scale.set_scale(calibration_factor);
      inputString = "";
    }
    else if (!inputString.indexOf("z"))
    {
      scale.set_scale();
      scale.tare();  //Reset the scale to 
      inputString = "";
    }
  }
}

void serialEvent() {
  while (Serial.available()) {

    char inChar = (char)Serial.read();

    inputString += inChar;

    if (inChar == '\n') {
      completeStr = true;
    }
  }
}
