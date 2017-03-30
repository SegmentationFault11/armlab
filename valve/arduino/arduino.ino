void setup() {
  Serial.begin(9600);
   pinMode(5, OUTPUT);
   pinMode(6, OUTPUT);
   pinMode(7, OUTPUT);
   pinMode(8, OUTPUT);
   pinMode(9, OUTPUT);
   pinMode(10, OUTPUT);
   pinMode(11, OUTPUT);
   pinMode(12, OUTPUT);
   pinMode(13, OUTPUT);
}

void loop() {
  Serial.print('r'); // signal ready
  if (Serial.available()) {
    char c = Serial.read();
    if (c == '0') {
      digitalWrite(5, HIGH);
    } 
    else if (c == 'a') {
        digitalWrite(5, LOW);
    } 
    else if (c == '1') {
      digitalWrite(6, HIGH);
    } 
    else if (c == 'b') {
      digitalWrite(6, LOW);
    } 
    else if (c == '2') {
      digitalWrite(7, HIGH);
    } 
    else if (c == 'c') {
      digitalWrite(7, LOW);
    } 
    else if (c == '3') {
      digitalWrite(8, HIGH);
    } 
    else if (c == 'd') {
      digitalWrite(8, LOW);
    } 
    else if (c == '4') {
      digitalWrite(9, LOW);
    } 
    else if (c == 'e') {
      digitalWrite(9, LOW);
    } 
    else if (c == '5') {
      digitalWrite(10, LOW);
    } 
    else if (c == 'f') {
      digitalWrite(10, LOW);
    }
    else if (c == '6') {
      digitalWrite(11, LOW);
    } 
    else if (c == 'g') {
      digitalWrite(11, LOW);
    } 
    else if (c == '7') {
      digitalWrite(12, LOW);
    } 
    else if (c == 'h') {
      digitalWrite(12, LOW);
    } 
    else if (c == '8') {
      digitalWrite(13, LOW);
    } 
    else if (c == 'i') {
      digitalWrite(13, LOW);
    }
  }
}
