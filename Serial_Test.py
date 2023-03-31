# Unit Tests :-)
#
# Get data from Arduino!

from __future__ import print_function
from quickserial import QSerial

import serial
import thread
import time
import util


# Some global variables
s = None            # The Serial connection
serial_read_thread = True   # While true, keep reading serial data.
led1 = 255    # Brightness of LED2
led2 = 255  # Brightness of LED2

# This function will be run inside of its own thread
# A thread is like a process, that runs independently of the rest of your program.
def serial_read(threadname, a_port):
    global serial_read_thread, led1, led2
    print "Entering Thread - Opening Serial Connection"
    s = serial.Serial(a_port, 9600)
    time.sleep(1) # give the serial connection a second to do it's thing
    while serial_read_thread:
        if s.inWaiting() == 0:
            s.write(chr(65) + chr(led1) + chr(led2)) # ask the Arduino for more data
            time.sleep(0.01)  # wait ten milliseconds
        if s.inWaiting() > 2:
            chars = s.read(3)  # read three bytes
            print ord(chars[0]), ord(chars[1]), ord(chars[2])
    # When the while loop exits, so does the thread.
    print "Exit thread - Closing Serial Connection"
    s.close()

# This function creates the thread.
def start_serial(port):
    global serial_read_thread
    serial_read_thread = True
    return thread.start_new_thread(serial_read, ("SerialThread", theport))

# Gives the signal for the thread to stop.
def stop_serial():
    global serial_read_thread
    serial_read_thread = False

# A convenience function for setting the brightness of the two leds
def set_leds(l1, l2):
    global led1, led2
    led1 = l1
    led2 = l2


# This function is the main entry point for your program.
def main():
    ports = util.list_serial_ports()  # Get a list of available serial ports
    print "Available serial ports: "
    i = 0
    for p in ports:
        print i, " --- " + p
        i += 1
    port_pick = raw_input("Which port would you like to connect to (pick a number)?: ")
    theport = ports[int(port_pick)]
    start_serial(theport)  #

set_leds(127, 255)
stop_serial()
start_serial(theport)

