void setup() {
  Serial.begin(9600);
   pinMode(8, OUTPUT);
   pinMode(9, OUTPUT);
   pinMode(10, OUTPUT);
   pinMode(11, OUTPUT);
}

void loop() {
  Serial.print('r'); // signal ready
  if (Serial.available()) {
    char c = Serial.read();
    if (c == '1') {
      digitalWrite(8, HIGH);
    } else if (c == '2') {
      digitalWrite(8, LOW);
    } else if (c == '3') {
      digitalWrite(9, HIGH);
    } else if (c == '4') {
      digitalWrite(9, LOW);
    } else if (c == '5') {
      digitalWrite(10, HIGH);
    } else if (c == '6') {
      digitalWrite(10, LOW);
    } else if (c == '7') {
      digitalWrite(11, HIGH);
    } else if (c == '8') {
      digitalWrite(11, LOW);
    }
  }
}
