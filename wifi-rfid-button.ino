#include <SPI.h>
#include <MFRC522.h>
#include "WiFiEsp.h"
#include "SoftwareSerial.h"

#define SS_PIN 10
#define RST_PIN 9
#define BUTTON_PIN 2

MFRC522 rfid(SS_PIN, RST_PIN);
MFRC522::MIFARE_Key key;

byte nuidPICC[4];

char ssid[] = "은주";     // your network SSID (name)
char pass[] = "eunju0915!"; // your network password

char server[] = "13.124.66.245";
int status = WL_IDLE_STATUS; // the WiFi radio's status

SoftwareSerial Serial1(3, 4); // RX, TX
WiFiEspClient client;

String byteArrayToHexString(byte *array, byte size) {
  String hexString = "";
  for (byte i = 0; i < size; i++) {
    hexString += (array[i] < 0x10 ? "0" : "") + String(array[i], HEX);
  }
  return hexString;
}

void setup() {
  Serial.begin(9600);
  Serial1.begin(9600);
  WiFi.init(&Serial1);

  if (WiFi.status() == WL_NO_SHIELD) {
    Serial.println("WiFi shield not present");
    while (true);
  }

  while (status != WL_CONNECTED) {
    Serial.print("Attempting to connect to WPA SSID: ");
    Serial.println(ssid);
    status = WiFi.begin(ssid, pass);
  }

  Serial.println("You're connected to the network");
  printWifiStatus();

  pinMode(BUTTON_PIN, INPUT_PULLUP);
  SPI.begin(); 
  rfid.PCD_Init(); 
}

void loop() {
   if (readRFID()) { 

  // Check if the button is pressed
  if (digitalRead(BUTTON_PIN) == HIGH) {
    // Button is pressed, treat it as item checkout
    Serial.println("Item checkout");
    // RFID 태그 값을 서버의 /api/output에 전송
    sendDataToServer("/api/output", byteArrayToHexString(nuidPICC, 4));

    // Other logic for item checkout
   
  } else {
    // Button is not pressed, treat it as item checkin
    Serial.println("Item checkin");
    // RFID 태그 값을 서버의 /api/input에 전송
    sendDataToServer("/api/input", byteArrayToHexString(nuidPICC, 4));

    // Other logic for item checkin
    
  }
   }

  // Other loop logic as needed
}

bool readRFID() {
  if (!rfid.PICC_IsNewCardPresent())
    return false; // 카드가 감지되지 않음

  if (!rfid.PICC_ReadCardSerial())
    return false; // 카드 읽기 실패

  for (byte i = 0; i < 4; i++) {
    nuidPICC[i] = rfid.uid.uidByte[i];
  }

  rfid.PICC_HaltA();
  rfid.PCD_StopCrypto1();

  return true; // 카드가 성공적으로 읽혔음
}


void sendDataToServer(String path, String itemId) {
  String dataToSend = "item_id=" + itemId;

  if (client.connect(server, 80)) {
    Serial.println("Connected to server");
    // 변경된 부분: path를 URL에 포함
    client.println("GET " + path + "?" + dataToSend + " HTTP/1.1");  
    client.println("Host: 13.124.66.245");
    client.println("Connection: close");
    client.println();

    Serial.println("Data sent to server: " + dataToSend);

    delay(500);

    while (client.available()) {
      String line = client.readStringUntil('\r');
      Serial.print(line);
    }

    client.stop();
  } else {
    Serial.println("Unable to connect to the server");
  }
}

void printWifiStatus() {
  Serial.print("SSID: ");
  Serial.println(WiFi.SSID());

  IPAddress ip = WiFi.localIP();
  Serial.print("IP Address: ");
  Serial.println(ip);

  long rssi = WiFi.RSSI();
  Serial.print("Signal strength (RSSI):");
  Serial.print(rssi);
  Serial.println(" dBm");
}
