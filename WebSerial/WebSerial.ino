/*
  Rui Santos
  Complete project details at https://RandomNerdTutorials.com/esp32-webserial-library/
  
  This sketch is based on the WebSerial library example: ESP32_Demo
  https://github.com/ayushsharma82/WebSerial
*/

#include <Arduino.h>
#include <WiFi.h>
#include <AsyncTCP.h> //Download dependencies (Zip)
#include <ESPAsyncWebServer.h> //Download dependencies (Zip)
#include <WebSerial.h> //Library manager: WebSerial library by Ayush Sharma

#define LED 2

AsyncWebServer server(80);

const char* ssid = "CAM";          // Your WiFi SSID
const char* password = "CAMERApass";  // Your WiFi Password

void recvMsg(uint8_t* data, size_t len) {
  WebSerial.println("Received Data...");
  String d = "";
  for (int i = 0; i < len; i++) {
    d += char(data[i]);
  }
  WebSerial.println(d);
  if (d == "ON") {
    digitalWrite(LED, HIGH);
  }
  if (d == "OFF") {
    digitalWrite(LED, LOW);
  }
}

void setup() {
  Serial.begin(115200);
  pinMode(LED, OUTPUT);
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  if (WiFi.waitForConnectResult() != WL_CONNECTED) {
    Serial.printf("WiFi Failed!\n");
    return;
  }
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());
  // WebSerial is accessible at "<IP Address>/webserial" in browser
  WebSerial.begin(&server);
  WebSerial.msgCallback(recvMsg);
  server.begin();
}

void loop() {
  WebSerial.println("Hello!");
  delay(2000);
}