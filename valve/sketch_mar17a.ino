char curr_read = 'x';
char prev_read = 'y';
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
    if (curr_read != prev_read) {
      on = !on;
    }
    if (on) {
      analogWrite(9, 1023);
    } else {
      analogWrite(9, 0);
    }
    /*ECHO the value that was read, back to the serial port. */
    Serial.write(curr_read);
    prev_read = curr_read;
  }
}
