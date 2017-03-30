from time import sleep
from lcm import LCM
import serial, sys, os, inspect

VALID_INPUTS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', \
'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']

ser = serial.Serial('/dev/tty.usbmodem1421', 9600, timeout=2)
ser.isOpen()

def main():
    if len(sys.argv) >= 2:
        if sys.argv[1] == 'test':
            interactive_mode()
        else:
            print 'Unrecognzied option', sys.argv[1]
    else:
        lcm_mode()

def interactive_mode():
    while ready():
        if ser.read() == 'r': # check ready
            input = raw_input(">> ")
            if not valid_input(input):
                print 'Invalid command'
                continue
            ser.write(input)

def lcm_mode():
    import_lcm_python()
    lc = LCM()
    subscription = lc.subscribe('VALVE', valve_handler)
    print 'Subscribed to the VAVLE channel, waiting for command...'
    while True:
        lc.handle()

def valve_handler(channel, data):
    msg = valve_command_t.decode(data)
    if ready():
        if ser.read() == 'r': # check ready
            input = msg.cmd
            if not valid_input(input):
                print 'Invalid command'
                return
            ser.write(input)

def import_lcm_python():
    currentdir = os.path.dirname(os.path.abspath(inspect.getfile(
        inspect.currentframe())))
    parentdir = os.path.dirname(currentdir)
    sys.path.insert(0,parentdir) 
    from lcm_python import valve_command_t

def ready():
    while True:
        if ser.read() == 'r':
            return True
        else:
            print 'No ready signal. Unplug and plug the USB cable.'

def valid_input(input):
    return input in VALID_INPUTS

if __name__ == '__main__':
    try:
        main()
    except:
        ser.close()
