void setup() {
  Serial.begin(9600);
}

void loop() {
  Serial.print('r'); // signal ready
  if (Serial.available()) {
    char c = Serial.read();
    if (c == '1') {
      analogWrite(9, 1023);
    } else if (c == '2') {
      analogWrite(9, 0);
    } else if (c == '3') {
      analogWrite(9, 1023);
    } else if (c == '4') {
      analogWrite(9, 0);
    } else if (c == '5') {
      analogWrite(9, 1023);
    } else if (c == '6') {
      analogWrite(9, 0);
    } else if (c == '7') {
      analogWrite(9, 1023);
    } else if (c == '8') {
      analogWrite(9, 0);
    }
  }
}
