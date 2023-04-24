#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <HTTPClient.h>
#include <WiFiMulti.h>

const char* ssid = "ss";
const char* password = "ss";


  
WiFiMulti wifiMulti;
 
void setup() {
  Serial.begin(9600);
   
  delay(4000);
  wifiMulti.addAP(ssid, password);
 
  postDataToServer();
}
 
void loop() {
  // Not used in this example
}
 
void postDataToServer() {
 
  Serial.println("Posting JSON data to server...");
  // Block until we are able to connect to the WiFi access point
  if (wifiMulti.run() == WL_CONNECTED) {
     
    HTTPClient http;   
     
    http.begin("https://flaskapidemo.azurewebsites.net/sendjson");  
    http.addHeader("Content-Type", "application/json");         
     
    StaticJsonDocument<200> jsonfile;
    // Add values in the document
    //
    jsonfile["signal"] = "peak";
    // jsonfile["signal2"] = "reading2";
    // jsonfile["signal3"] = "reading3";
   
    // Add an array.
    //
    // JsonArray data = doc.createNestedArray("data");
    // data.add(48.756080);
    // data.add(2.302038);
     
    String requestBody;
    serializeJson(jsonfile, requestBody);
     
    int httpResponseCode = http.POST(requestBody);
 
    if(httpResponseCode>0){
       
      String response = http.getString();                       
       
      Serial.println(httpResponseCode);   
      Serial.println(response);
     
    }

  }
}