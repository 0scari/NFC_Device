from NFC_Device import NFC_Device
import unittest
import serial
import os
import time
import sys



class MyTestCase(unittest.TestCase):
    def tearDown(self):
        NFC_Device.closeCommunication()
        NFC_Device._NFC_Device__bufferHistory = []

    # def testNfcDeviceConn(self):
    #     try:
    #         NFC_Device._NFC_Device__establishSerialConnOrExit(
    #             "/dev/tty.usbmodem1411", 115200)
    #         self.assertTrue(True)
    #     except SystemExit:
    #         self.assertTrue(False)
    #     pass
    #
    # def testInputFile(self):
    #     try:
    #         NFC_Device._NFC_Device__openFileOrExit("input.txt")
    #     except SystemExit:
    #         print "Input file not found"
    #         self.assertTrue(False)
    #
    # def testIfInputFileEmptied(self):
    #     self.writeToInputFile("test")
    #     NFC_Device.setCommunicationTimer(2)
    #     NFC_Device.startCommunication(
    #         "input.txt", "/dev/tty.usbmodem1411", 115200)
    #     f = open("input.txt", "r")
    #     self.assertTrue(len(f.read()) == 0)
    #
    # def testSerialRead(self):
    #     NFC_Device._NFC_Device__establishSerialConnOrExit(
    #         "/dev/tty.usbmodem1411", 115200)
    #     NFC_Device._NFC_Device__readlnSerialBuffer()
    #     self.assertTrue(len(NFC_Device._NFC_Device__bufferHistory) > 0)
    #
    # def testSerialWrite(self):
    #     NFC_Device._NFC_Device__establishSerialConnOrExit(
    #         "/dev/tty.usbmodem1411", 115200)
    #     try:
    #         NFC_Device._NFC_Device__serialConn.write("qwerty")
    #         self.assertTrue(True)
    #     except Exception:
    #         self.assertTrue(False)
    #
    # def testNfcWrite(self):
    #     str = self.writeToInputFile("test_token")
    #     NFC_Device.setCommunicationTimer(5)
    #     NFC_Device.startCommunication(
    #         "input.txt", "/dev/tty.usbmodem1411", 115200)
    #     try:
    #         self.assertTrue(str in NFC_Device._NFC_Device__bufferHistory[2])
    #         self.assertTrue("Data was written" in
    #                             NFC_Device._NFC_Device__bufferHistory[3])
    #     except KeyError:
    #         self.assertTrue(False)

    def testNfcOverwritingProtection(self):
        NFC_Device.startCommunication(
            "input.txt", "/dev/tty.usbmodem1411", 115200)
        print NFC_Device._NFC_Device__bufferHistory

        # stop = False
        # pid = os.fork()
        # if pid:
        #     while (not stop):
        #         NFC_Device.setCommunicationTimer(2)
        #         NFC_Device.startCommunication(
        #             "input.txt", "/dev/tty.usbmodem1411", 115200)
        #     sys.exit(0)
        #
        # else:
        #     time.sleep(6)
        #     raw_input("Tag overwritten?: ")
        #     stop = True
        #     time.sleep(10)
        #     print NFC_Device._NFC_Device__bufferHistory


    def writeToInputFile(self, str):
        f = open("input.txt", "w")
        f.write(str)
        f.close()
        return str

if __name__ == '__main__':
    unittest.main()
