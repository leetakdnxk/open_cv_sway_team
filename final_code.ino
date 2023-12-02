#include <SPI.h>
#include <MFRC522.h>
#include "WiFiEsp.h"
#include "SoftwareSerial.h"
#include <Servo.h>

#define SS_PIN 10
#define RST_PIN 9
#define BUTTON_PIN 2
#define SERVO_PIN A0
#define PIEZO_PIN 5

MFRC522 rfid(SS_PIN, RST_PIN); // RFID 모듈 초기화
MFRC522::MIFARE_Key key;

byte nuidPICC[4];

char ssid[] = "은주";     // 네트워크 SSID
char pass[] = "eunju0915!"; // 네트워크 비밀번호

char server[] = "13.124.66.245"; // 서버 주소
int status = WL_IDLE_STATUS; // 와이파이 상태

SoftwareSerial Serial1(3, 4); // RX, TX
WiFiEspClient client;

Servo myservo; // 서보 모터 객체

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

  pinMode(BUTTON_PIN, INPUT);
  SPI.begin(); 
  rfid.PCD_Init();
  pinMode (SERVO_PIN, OUTPUT);
}

unsigned long lastCheckTime = 0;
const long checkInterval = 10000;

void loop() {
  Serial.println(digitalRead(BUTTON_PIN));
  unsigned long currentMillis = millis();
  if (currentMillis - lastCheckTime >= checkInterval) {
    lastCheckTime = currentMillis;
    checkServerStatus();
  }
  
  if (readRFID()) {
    Serial.print("READ");
    tone(PIEZO_PIN, 1000, 1000);  
    delay(1000); 
    String path = (digitalRead(BUTTON_PIN) == HIGH ? "/api/output" : "/api/input");
    sendDataToServer(path, byteArrayToHexString(nuidPICC, 4));
  }
}

bool readRFID() {
  if (!rfid.PICC_IsNewCardPresent())
    return false;

  if (!rfid.PICC_ReadCardSerial())
    return false;

  for (byte i = 0; i < 4; i++) {
    nuidPICC[i] = rfid.uid.uidByte[i];
  }

  rfid.PICC_HaltA();
  rfid.PCD_StopCrypto1();
  return true;
}

void sendDataToServer(String path, String itemId) {
  String dataToSend = "item_id=" + itemId;

  if (client.connect(server, 80)) {
    Serial.println("Connected to server");
    client.println("GET " + path + "?" + dataToSend + " HTTP/1.1");
    client.println("Host: " + String(server));
    client.println("Connection: close");
    client.println();

    Serial.println("Data sent to server: " + dataToSend);

    delay(500);

    while (client.available()) {
      String line = client.readStringUntil('\r');
      Serial.print(line);
    }

    client.stop();
    rfid.PCD_Init(); 
  } else {
    Serial.println("Unable to connect to the server");
  }
}

void checkServerStatus() {
    if (client.connect(server, 80)) {
      client.println("GET /api/check HTTP/1.1");
      client.println("Host: " + String(server));
      client.println("Connection: close");
      client.println();
      int count = 0;
      while (client.available()) {
        String line = client.readStringUntil('\r');
        if (line == 0 || line == "0" || line == "\n0" || line == 1 || line == "1" || line == "\n1") {
          myservo.attach(SERVO_PIN);
          if (line == 0 || line == "0" || line == "\n0") {
            Serial.print("OPENS");
            myservo.write(70);
          } else if (line == 1 || line == "1" || line == "\n1") {
            Serial.print("CLOSEDS");
            myservo.write(10);
          }
          delay(1000);
          myservo.detach();
        }
        count++;
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
