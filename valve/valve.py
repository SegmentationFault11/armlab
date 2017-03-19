from time import sleep
import serial, sys, os

VALID_INPUTS = ['1', '2', '3', '4', '5', '6', '7', '8']

def main(ser):
    while ready(ser):
        if ser.read() == 'r': # check ready
            input = raw_input(">> ")
            if not valid_input(input):
                print 'Invalid command'
                continue
            ser.write(input)

def ready(ser):
    while True:
        if ser.read() == 'r':
            return True
        else:
            print 'Waiting for Arduino to be ready'

def valid_input(input):
    return input in VALID_INPUTS

if __name__ == '__main__':
    try:
        ser = serial.Serial('/dev/tty.usbmodem1421', 9600, timeout=2)
        main(ser)
    except KeyboardInterrupt:
        ser.close()
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
