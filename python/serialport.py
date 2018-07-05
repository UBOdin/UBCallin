# -*- coding: utf-8 -*-
#TYOS Serial Interface with Fona
#copyright (c) 2015 Tyler Spadgenske
# Adapted from https://raw.githubusercontent.com/spadgenske/TYOS/master/src/serialport.py
# Used under MIT License.

import serial, time
from datetime import datetime, timedelta

class SerialPort():
    def __init__(self):
        self.serialport = None
        self.baud_rate = 115200
        self.device = "/dev/serial0"

    def connect(self, skip_check = False):
        #open connection
        print "Connecting..."
        self.serialport = serial.Serial(self.device, self.baud_rate, timeout=0.5)
        if skip_check:
            return True
        #Send test command
        print "Checking connection..."
        self.serialport.write('AT\r')
        #get reply
        print "Waiting for modem response..."
        reply = self.receive()

        #Check for good return
        if 'OK' in reply:
            return True;
        else:
            self.serialport = None
            return False

    def is_connected(self):
        return self.serialport != None
    
    def transmit(self, data):
        if self.serialport == None:
            raise "Not Connected"
        print "Writing: {}".format(data)
        self.serialport.write(data + '\r')

    def receive(self, end_marker = None, timeout = datetime.now() + timedelta(seconds=3)):
        if self.serialport == None:
            raise "Not Connected"
        response = []

        while (len(response) <= 0) or ((end_marker != None) and (end_marker not in response)):
            print "Reading..."
            feed = self.serialport.readlines()
            print "Read {} lines".format(len(feed))
            for i in range(len(feed)):
                feed[i] = feed[i].rstrip()
                print "Read: '{}'".format(feed[i])
            response = response + feed
            if "ERROR" in feed:
                return response
            if datetime.now() > timeout:
                return response
        return response

    def request(self, data, end_marker = None):
        self.transmit(data)
        return self.receive(end_marker)

    def check(self):
        self.model = self.request('ATI', 'OK')
        print self.model
        return self.model
    
    def close(self):
        self.serialport.close()
        self.serialport = None
        
if __name__ == '__main__':
    test = SerialPort()
    if test.connect(skip_check = True):
        print "Connected to FONA!"
        test.transmit(chr(26))
    else:
        print "Error connecting"
    
