# Valve

## Structure

```
arduino.ino: Arduino C++ code.
valve.py: Valve controller Python code.
```

## Usage

Connect the Arduino board to the computer using a USB cable.

-LCM Mode

Run `python valve.py` in the LCM mode (default mode).

- Interactive Mode

Run `python valve.py test` for debugging in the interactive mode. 
Available commands are: `1, 2, 3, 4 ,5 ,6 ,7, or 8`.
Any other commands will be ignored.
To stop the valve controller, press `Ctrl+C`.

- Debugging

The program waits for a ready signal from the Arduino board.
Unplug and plug if the connection cannot be established.
