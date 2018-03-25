#!/usr/bin/python2.7
import serial
import time
import sys

class NFC_Device:
    """The class that encapsulates data and methods about communication with
    the NFC Device.
    @cvar __bufferHistory: History of data read from the serial buffer
    @type List
    @cvar __serialConn: A variable to store the serial connection object
    @type PySerial
    @cvar __timer: Used to set the time limit for the loop in the startCommunication method
    (infinity by default)
    @type integer"""
    __bufferHistory = []
    __serialConn = None
    __timer = float("inf")

    @staticmethod
    def setCommunicationTimer(seconds):
        """
        A method to set a timescale for the serial communication with the NFC Device to be carried out in.
        @param seconds: Amount of time
        @type integer seconds
        """
        NFC_Device.__timer = seconds

    @staticmethod
    def startCommunication(inputFileName, portName, baudRate):
        """
        The function that repetitively reads the input file where the back-end system writes
        input data. Input is a string token that must be transferred to the device and written
        to the tag in it.
        @todo once the complete back-end is implemented, the class must be changed to accept
        the input in it's instantiation method
        @param inputFileName: Name of the input file
        @type string
        @param portName: Name of the serial port
        @type string
        @param baudRate: Baud rate on the port
        @type integer
        """
        NFC_Device.__establishSerialConnOrExit(portName, baudRate)
        ellapsedSeconds = 0
        while ellapsedSeconds < NFC_Device.__timer:
            # inputFile = NFC_Device.__openFileOrExit(inputFileName)
            newToken  = NFC_Device.readUrl() #inputFile.read()
            NFC_Device.__readlnSerialBuffer() # Has side effect: printing
            if (newToken):
                print "Mac: new token " + newToken
                # inputFile.truncate(0) # reset input.txt to "/0"
                NFC_Device.__serialConn.write("{0}\n".format(newToken))
                # ! ARDUINO MUST BE RESETTING NOW
                NFC_Device.__readlnSerialBuffer()
            time.sleep(1)
            ellapsedSeconds += 1
        NFC_Device.closeCommunication()

    @staticmethod
    def __establishSerialConnOrExit(port, baud):
        """
        The method that attempts to establish serial connection
        on the given port. If it fails, the process will terminate.
        @param port: Port name
        @type string
        @param baud: Port's baud rate
        @type integer
        @return: Exit on failure
        """
        try:
            NFC_Device.__serialConn = serial.Serial(port, baud, timeout=5)
            time.sleep(4) # time it takes to set up the device
        except Exception as e:
            print "Unable to establish serial connection.\nMessage: ", e
            sys.exit(1)

    @staticmethod
    def __openFileOrExit(fileName):
        """
        A function to safely open the input file if such exists, otherwise shut the process down.
        @param fileName: Path to file to be opened.
        @type string
        """
        try:
            f = open(fileName, "r+")
            return f
        except IOError as err:
            print "Input file not found, shutting down"
            sys.exit(1)

    @staticmethod
    def readUrl():
        """
        Read from the server.
        @return: string token
        """
        import urllib, json
        url = "https://mozamilrasouli.000webhostapp.com/oscar.php"
        response = urllib.urlopen(url)
        token = response.read()
        if token:
            return token
        else:
            return ""


    @staticmethod
    def __readlnSerialBuffer():
        """
        Reads every line from the data buffer in the established connection object and
        appends to the __bufferHistory list.
        """
        data = "" # must be predefined, or error
        while NFC_Device.__serialConn.in_waiting:
            data = NFC_Device.__serialConn.readline()
            NFC_Device.__bufferHistory.append(data)
            print "Arduino: {0}".format(data)

    @staticmethod
    def closeCommunication():
        """
        A method to close the serial communication and reset the connection variable to None.
        """
        if NFC_Device.__serialConn:
            NFC_Device.__serialConn.close()
            NFC_Device.__serialConn = None

if __name__ == '__main__':
    # NFC_Device.setCommunicationTimer(15) # Set timer to run next method
    NFC_Device.startCommunication("input.txt", "/dev/tty.usbmodem1411", 115200)