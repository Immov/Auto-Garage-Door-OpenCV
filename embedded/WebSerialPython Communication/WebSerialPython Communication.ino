#include "http_server.h"

void setup(){
     Serial.begin(9600);  // setup serial communication
     // Set WiFi to station(STA) and access point (AP) mode simultaneously 
     WiFi.mode(WIFI_AP_STA);
     delay(100); // Recommended delay
     WiFi.softAP("choose_some_ssid", "choose_some_password");

     // Remember to configure the previous server
     setup_http_server();  // starts the asyncronus https server*/
}

void loop(){
     delay(1000);
}