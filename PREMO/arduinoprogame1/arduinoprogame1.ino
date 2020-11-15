int sensor = 2;
int Pin3 = 3; // pin3 , pin4, pin5, pin8 các chân output
int Pin4 = 4;
int Pin5 = 5;
int Pin8 = 8;
unsigned long time;
boolean  lastsensorStatus = 0;
boolean  defaultSensorStatus = 0;
unsigned long lastChangedTime;
unsigned long waitTime = 100; // thời gian delay của nút nhấn
char data;

void setup() {
  Serial.begin(9600);   //Mở cổng Serial ở baudrate 9600 để giao tiếp với máy tính
  pinMode(sensor , INPUT_PULLUP);  //Cài đặt chân D2 ở trạng thái đọc dữ liệu và dùng trở kéo bên trong MCU
  pinMode(Pin3, OUTPUT);
  pinMode(Pin4, OUTPUT);
  pinMode(Pin5, OUTPUT);
  pinMode(Pin8, OUTPUT);
  digitalWrite(Pin3, LOW);
  digitalWrite(Pin4, LOW);
  digitalWrite(Pin5, LOW);
  digitalWrite(Pin8, LOW);
  digitalWrite(sensor, defaultSensorStatus);
  time = millis();
}

void loop() {
  boolean  sensorStatus = digitalRead(sensor);    //Đọc trạng thái sensor
  if (sensorStatus != lastsensorStatus)
  {
    lastsensorStatus = sensorStatus;      // cập nhật trang thái cuối cùng sensor
    lastChangedTime = millis();          // cập nhật thời gian nhấn nút
    defaultSensorStatus = sensorStatus; // Cập nhập trạng thái sensor
  }

  if (millis() - lastChangedTime > waitTime) {// đủ 100ms thì gửi Serial
    if (defaultSensorStatus == true) {
      Serial.println("SenSor In");
      defaultSensorStatus = false;
    }
    lastChangedTime = millis();
  }


  if (Serial.available() > 0)// kiểm tra bộ đệm serial
  {
    char data = Serial.read();
    Serial.println(data);

    if (data == '3') {
      digitalWrite(Pin3, HIGH);
    }
    if (data == '4') {
      digitalWrite(Pin4, HIGH);
    }
    if (data == '5') {
      digitalWrite(Pin5, HIGH);
    }
    if (data == '8') {
      digitalWrite(Pin8, HIGH);
    }


  }
  if ( (unsigned long) (millis() - time) > 100)// timer delay 100ms
  {
    digitalWrite(Pin3, LOW);
    digitalWrite(Pin4, LOW);
    digitalWrite(Pin5, LOW);
    digitalWrite(Pin8, LOW);
    time = millis();// cập nhật lại timer
  }
}

//Author: TNT