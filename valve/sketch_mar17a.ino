char curr_read;
bool on = false;

void setup() {                
// Turn the Serial Protocol ON
  Serial.begin(9600);
}

void loop() {
   /*  check if data has been sent from the computer: */
  if (Serial.available()) {
    /* read the most recent byte */
    curr_read = Serial.read();
    on = !on;
    if (on) {
      analogWrite(9, 0);
    } else {
      analogWrite(9, 1023);
    }
    /*ECHO the value that was read, back to the serial port. */
    Serial.write(curr_read);
  }
}
