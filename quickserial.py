"""
QuickSerial module
Communicates with Arduino fast & easy.


"""

from __future__ import print_function
import serial
import platform
import glob
from threading import Thread

class QSerialThread(Thread):
    def __init__(self, threadfunc=None):
        super(QSerialThread, self).__init__()
        self.callback = threadfunc


    #contains the code that runs inside the thread
    def run(self):
        # Do something!



class QSerial:
    def __init__(self, callback=None, dataids=None):
        self.thread = None
        self.callback = callback
        self.exitFlag = False
        if dataids is None:
            dataids = []
        self.dataCodes = dataids

    def connect(self, port=None, baud=9600):
        self.close()
        if port is None:
            # Get default port
            port = QSerial.getDefaultSerialPort()

        # set up a serial read thread
        #self.thread = threading.Thread(target=self.callback, args=(x,y))
        self.thread = threading.Thread(target=self.serial_read)


    def serial_read(self):
        # Make connection
        self.ser = serial.Serial(port, baud)
        terminator = ord('\n')

        vals = [None, None, None] # 3 last incoming bytes
        while self.exitFlag is False:
            # Read serial data here!
            if self.ser.inWaiting() > 0:
                newval = self.ser.read(1) # read 1 bytes
                if (newval == terminator) && (vals[0] in dataids):
                    # new datapoint
                    newdata = (vals[1] << 8) + vals[2]
                    # RUN CALLBACK WITH NEW DATAPOINT
                    self.callback(newdata)

                    # Reset the values
                    vals = [None, None, None]
                else:
                    # Add to the array of previous bytes
                    vals = vals[1:] + [newval]
        self.ser.close()



    def close(self):
        if self.thread is not None:
            self.exitFlag = True
            self.thread = None



    # Gets the default Serial Port
    @staticmethod
    def getDefaultSerialPort():
        devs = QSerial.getDevices()
        theport = None
        system_name = platform.system()
        if system_name == "Darwin":
            for dev in devs:
                if "usbserial" in dev:
                    theport = dev
            if theport is None:
                theport = devs[0]
        else:
            theport = devs[0]
        return theport

    # A function that tries to list serial ports on most common platforms
    @staticmethod
    def getDevices():
        system_name = platform.system()
        if system_name == "Windows":
            # Scan for available ports.
            available = []
            for i in range(256):
                try:
                    s = serial.Serial(i)
                    available.append(i)
                    s.close()
                except serial.SerialException:
                    pass
            return available
        elif system_name == "Darwin":
            # Mac
            return glob.glob('/dev/tty.*')
            #return glob.glob('/dev/tty*') + glob.glob('/dev/cu*')
        else:
            # Assume Linux or something else
            return glob.glob('/dev/ttyS*') + glob.glob('/dev/ttyUSB*')




if __name__ == "__main__":
    # Run some tests
    print("Testing QuickSerial...")
    print("Available Serial Ports: ", QuickSerial.getDevices())
    print("Default Serial Port is: ", QuickSerial.getDefaultSerialPort())


