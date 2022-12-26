#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <ESPAsyncWebServer.h>
#include "AsyncJson.h"
#include "ArduinoJson.h"
#include <Adafruit_SHT31.h>

const char *ssid = "SSID"; //SSID of the Wifi Network
const char *password = "PASSWORD"; //Password of the Wifi Network.
const char *roomName = "ROOM NAME"; //Name of the room the sensor is in.
IPAddress staticIP(192, 168, 0, 35); //Change the fixed IP of the Sensor.
IPAddress staticGateway(192, 168, 0, 1);
IPAddress staticSubnet(255, 255, 255, 0);

AsyncWebServer server(80);
Adafruit_SHT31 sht31 = Adafruit_SHT31();

void notFound(AsyncWebServerRequest *request) {
  request->send(404, "application/json", "{\"message\":\"Not found\"}");
}

void setup() {
  Serial.begin(9600);

  sht31.begin();

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  WiFi.config(staticIP, staticGateway, staticSubnet);

  while (WiFi.waitForConnectResult() != WL_CONNECTED) {
    Serial.printf("WiFi Failed!\n");
  }
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());

  server.on("/", HTTP_GET, [](AsyncWebServerRequest *request) {
    float humidity = sht31.readHumidity();
    float temperature = sht31.readTemperature();
    request->send(200, "application/json", "{\"Temperature\":\"" + String(temperature) + "\",\"Humidity\":\"" + String(humidity) + "\",\"Room\":\"" + roomName + "\"}");
  });

  server.onNotFound(notFound);
  server.begin();
}

void loop() {
}