/***************************************************************************
  This is an example program for the sending a counter to Adafruit IO using
  an ESP8266 WiFi module.  You will need to correct the WiFi SSID and password
  and add your Adafruit IO username and Key.

  written by Theo Fleck and Rick Martin
  03/25/2020
 ***************************************************************************/
#include "Arduino.h"
#include <SoftwareSerial.h>		          //Allows us to use two GPIO pins for a second UART

#include "LIS3DHTR.h"//ADDED
#include <Wire.h>
LIS3DHTR<TwoWire> LIS; //IIC
#define WIRE Wire
int buzzer = 9;

////SoftwareSerial espSerial(11,10);	      //Create software UART to talk to the ESP8266
SoftwareSerial espSerial(10,11);	      //Create software UART to talk to the ESP8266
//String IO_USERNAME = "satorres";
String IO_USERNAME = "torrseba";
String IO_KEY  =     "aio_hSVK99L1uO2OTRZGlgEmPAYwo8W3"; //torrseba
//String IO_KEY  =     "aio_htWs85t4TccvpX3y2YM2bdUAbiEc"; //satorres
String WIFI_SSID = "UD Devices"; 	    //Only need to change if using other network, eduroam won't work with ESP8266
String WIFI_PASS = ""; 		            //Blank for open network
float num = 1.0; 			                  //Counts up to show upload working
int pinx = 0;
int piny = 0;
int pinz = 0;



void setup() {
	Serial.begin(9600);		// set up serial monitor with 9600 baud rate
	espSerial.begin(9600);		// set up software UART to ESP8266 @ 9600 baud rate
	Serial.println("setting up");
	String resp = espData("get_macaddr",2000,true);	//get MAC address of 8266
	resp = espData("wifi_ssid="+WIFI_SSID,2000,true);	//send Wi-Fi SSID to connect to
	resp = espData("wifi_pass="+WIFI_PASS,2000,true);	//send password for Wi-Fi network
	resp = espData("io_user="+IO_USERNAME,2000,true);	//send Adafruit IO info
	resp = espData("io_key="+IO_KEY,2000,true);
	resp = espData("setup_io",15000,true);			//setup the IoT connection

  //pinMode(6, OUTPUT);

	if(resp.indexOf("connected") < 0) {
		Serial.println("\nAdafruit IO Connection Failed");
		while(1);
  }

	resp = espData("setup_feed=1,x1",2000,false);	//start the data feed  //RENAME FOR DIFFERENT FEED
  String respy = espData("setup_feed=2,y1",2000,false);	//start the data feed  //RENAME FOR DIFFERENT FEED //***************************************
  String respz = espData("setup_feed=3,z1",2000,false);	//start the data feed  //RENAME FOR DIFFERENT FEED //***************************************
	Serial.println("------ Setup Complete ----------");

  while (!Serial)
  {
  };
  LIS.begin(WIRE, LIS3DHTR_ADDRESS_UPDATED); //IIC init
  delay(100);
  LIS.setOutputDataRate(LIS3DHTR_DATARATE_50HZ);
 

}

void loop() {

	// free version of Adafruit IO only allows 30 uploads/minute, it discards everything else
	  if(LIS.getAccelerationZ() < 0){
    Serial.print("BUZZER");
    analogWrite(buzzer, 150);

  }
  else if(LIS.getAccelerationZ() > 0){
    //Serial.print("BUZZEROFF");
    analogWrite(buzzer, 0);

  }
  
	///Serial.print("Num is: ");
	//Serial.println(num);
	///String resp = espData("send_data=1,"+String(num),2000,false); //send feed to cloud
	///num = num +0.5;			// Count by 0.5 increments
  Serial.print("x:"); Serial.print(LIS.getAccelerationX()); Serial.print("  ");
  Serial.print("y:"); Serial.print(LIS.getAccelerationY()); Serial.print("  ");
  Serial.print("z:"); Serial.println(LIS.getAccelerationZ());
	  if(LIS.getAccelerationZ() < 0){
    Serial.print("BUZZER");
    analogWrite(buzzer, 150);

  }
  else if(LIS.getAccelerationZ() > 0){
    //Serial.print("BUZZEROFF");
    analogWrite(buzzer, 0);

  }
  delay(5000);			// Wait 5 seconds between uploads
  String resp = espData("send_data=1,"+String(LIS.getAccelerationX()),2000,false);

	  if(LIS.getAccelerationZ() < 0){
    Serial.print("BUZZER");
    analogWrite(buzzer, 150);

  }
  else if(LIS.getAccelerationZ() > 0){
    //Serial.print("BUZZEROFF");
    analogWrite(buzzer, 0);

  }

  String respy = espData("send_data=2,"+String(LIS.getAccelerationY()),2000,false); ///******************************************

	  if(LIS.getAccelerationZ() < 0){
    Serial.print("BUZZER");
    analogWrite(buzzer, 150);

  }
  else if(LIS.getAccelerationZ() > 0){
    //Serial.print("BUZZEROFF");
    analogWrite(buzzer, 0);

  }

  String respz = espData("send_data=3,"+String(LIS.getAccelerationZ()),2000,false); ///******************************************


}

String espData(String command, const int timeout, boolean debug) {
	String response = "";
	espSerial.println(command);	//send data to ESP8266 using serial UART
	long int time = millis();
	while ( (time + timeout) > millis()) {	//wait the timeout period sent with the command
		while (espSerial.available()) {	//look for response from ESP8266
			char c = espSerial.read();
			response += c;
			Serial.print(c);	//print response on serial monitor
		}
	}
	if (debug) {
		Serial.println("Resp: "+response);
	}
	response.trim();
	return response;
}
