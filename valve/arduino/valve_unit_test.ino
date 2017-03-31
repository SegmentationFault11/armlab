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

char rx_byte = 0;

void loop() {
  if (Serial.available() > 0) {    // is a character available?
    rx_byte = Serial.read();       // get the character
  
    // check if a number was received
    if ((rx_byte >= '1') && (rx_byte <= '9')) {
      Serial.print("Number received: ");
      Serial.println(rx_byte);

      if (rx_byte == '1') {
        digitalWrite(5, HIGH);   // turn the LED on (HIGH is the voltage level)
        delay(3000);              // wait for a second
        digitalWrite(5, LOW);    // turn the LED off by making the voltage LOW
        
      } else if (rx_byte == '2') {
        digitalWrite(6, HIGH);   // turn the LED on (HIGH is the voltage level)
        delay(3000);              // wait for a second
        digitalWrite(6, LOW);    // turn the LED off by making the voltage LOW
        
      } else if (rx_byte == '3') {
        digitalWrite(7, HIGH);   // turn the LED on (HIGH is the voltage level)
        delay(3000);              // wait for a second
        digitalWrite(7, LOW);    // turn the LED off by making the voltage LOW
        
      } else if (rx_byte == '4') {
        digitalWrite(8, HIGH);   // turn the LED on (HIGH is the voltage level)
        delay(3000);              // wait for a second
        digitalWrite(8, LOW);    // turn the LED off by making the voltage LOW
        
      } else if (rx_byte == '5') {
        digitalWrite(9, HIGH);   // turn the LED on (HIGH is the voltage level)
        delay(3000);              // wait for a second
        digitalWrite(9, LOW);    // turn the LED off by making the voltage LOW
        
      } else if (rx_byte == '6') {
        digitalWrite(10, HIGH);   // turn the LED on (HIGH is the voltage level)
        delay(3000);              // wait for a second
        digitalWrite(10, LOW);    // turn the LED off by making the voltage LOW
        
      } else if (rx_byte == '7') {
        digitalWrite(11, HIGH);   // turn the LED on (HIGH is the voltage level)
        delay(3000);              // wait for a second
        digitalWrite(11, LOW);    // turn the LED off by making the voltage LOW
        
      } else if (rx_byte == '8') {
        digitalWrite(12, HIGH);   // turn the LED on (HIGH is the voltage level)
        delay(3000);              // wait for a second
        digitalWrite(12, LOW);    // turn the LED off by making the voltage LOW
        
      } else if (rx_byte == '9') {
        digitalWrite(13, HIGH);   // turn the LED on (HIGH is the voltage level)
        delay(3000);              // wait for a second
        digitalWrite(13, LOW);    // turn the LED off by making the voltage LOW
      } 
    }
    else {
      Serial.println("Not a number.");
    }
  } // end: if (Serial.available() > 0)
}