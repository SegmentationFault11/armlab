# Valve

## Structure

```
arduino.ino: Arduino C++ code.
valve.py: Valve controller Python code.
```

## Usage

Connect the Arduino board to the computer using a USB cable.
Then run `python valve.py`. 
The program waits for a signal from the Arduino 
board before it sends a command.
Unplug and plug if the connection cannot be established.
Available commands are: 1, 2, 3, 4 ,5 ,6 ,7, or 8.
Any other commands will be ignored.
To stop the valve controller, press 'Ctrl+C'.
