from serialport import SerialPort
from time import sleep
import pigpio
import re

class Fona800:
    
    def __init__(self):
        self.key_pin = 21   # FONA KEY: Output: Write a 0 to this pin to turn the FONA on.
        self.rcv_pin = 5    # FONA RCV: Input: Pull up, read a 0 when the FONA receives a call or SMS
        self.fona = SerialPort()
        self.gpio = pigpio.pi()
        
        self.gpio.set_mode(self.key_pin, pigpio.OUTPUT)
        self.gpio.write(self.key_pin, 0)
        self.gpio.set_mode(self.rcv_pin, pigpio.INPUT)
        self.gpio.set_pull_up_down(self.rcv_pin, pigpio.PUD_UP)

        sleep(1)
        if not self.fona.connect():
            raise "Error connecting"

        
    def toggle_power(self):
        self.gpio.write(self.key_pin, 1)
        sleep(.25)
        self.gpio.write(self.key_pin, 0)

    def send_sms(self, number, message):
        print "Sending SMS to '{}'\n{}".format(number, message) 
        self.fona.request('AT+CMGF=1', 'OK') # This asks the phone to put us into text mode
        self.fona.request('AT+CMGS="{}"'.format(number), '>') # This says "Send an SMS to..."
        print "Spooling message"
        for line in re.split("[\n\r]+", message): # And we enter one line of SMS at a time
            self.fona.request(line, '>')
        print "Sending..."
        self.fona.request(chr(26), 'OK') # The magic ^Z (ASCII character 26) tells the fona we're done entering text
        print "... done"
        
if __name__ == '__main__':
    test = Fona800()
    test.send_sms("17163521074", "This is a test!")
    #test.toggle_power()
    



