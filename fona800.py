from serialport import SerialPort
from time import sleep
import pigpio
import re

FONA_AUDIO_HEADSET = 0
FONA_AUDIO_EXTERNAL = 1

def split_csv(data):
    response = []
    temp = ""
    while(len(data) > 0):
        if data[0] == '"':
            data = data[1:]
            while data[0] != '"' and len(data) > 0:
                temp = temp + data[0]
                data = data[1:]
        elif data[0] == ',':
            response = response + [temp]
            temp = ""
        else:
            temp = temp + data[0]
        data = data[1:]
    return response + [temp]

def split_response(data, cmd):
    cmd = "+{}: ".format(cmd)
    for line in data:
        if line.startswith(cmd):
            line = line[len(cmd):]
            return split_csv(line)
    return None

class Fona800:
    
    def __init__(self,
                 call_handler = None,
                 sms_handler = None,
                 key_pin = 21,
                 rcv_pin = 5):
        self.key_pin = key_pin   # FONA KEY: Output: Write a 0 to this pin to turn the FONA on.
        self.rcv_pin = rcv_pin   # FONA RCV: Input: Pull up, read a 0 when the FONA receives a call or SMS
        self.call_handler = call_handler
        self.sms_handler = sms_handler
        self.fona = SerialPort()
        self.gpio = pigpio.pi()

        # Set the KEY pin up.  Normally we don't really want to twiddle this bit... but we should
        # tie it down to 0 so the FONA powers up.
        self.gpio.set_mode(self.key_pin, pigpio.OUTPUT)
        self.gpio.write(self.key_pin, 0)

        # Set up a PIGPIO trigger to call receive_event when this pin gets pulled to ground.
        # That means we're getting a Phone call (or an SMS)
        self.gpio.set_mode(self.rcv_pin, pigpio.INPUT)
        self.gpio.set_pull_up_down(self.rcv_pin, pigpio.PUD_UP)
        self.gpio.callback(
            self.rcv_pin,
            pigpio.FALLING_EDGE,
            lambda pin, level, tick: self.receive_event(pin, level, tick)
        )

        sleep(1)
        if not self.fona.connect():
            raise "Error connecting"

        # The following asks the FONA to provide Caller ID details
        self.fona.request('AT+CLIP=1', 'OK')

    def toggle_power(self):
        self.gpio.write(self.key_pin, 1)
        sleep(.25)
        self.gpio.write(self.key_pin, 0)

    def battery_status(self):
        status = self.fona.request('AT+CBC', 'OK')
        for line in status:
            if line.startswith('+CBC:'):
                line = line[6:].split(",")
                if line[0] == "0":
                    status = "No Charge"
                elif line[0] == "1":
                    status = "Charging"
                elif line[1] == "2":
                    status = "Fully Charged"
                return (status, int(line[1]), int(line[2]))
        raise "Error reading battery status"
            
    def send_sms(self, number, message):
        # This asks the phone to put us into text mode
        print "Sending SMS to '{}'\n{}".format(number, message)
        self.fona.request('AT+CMGF=1', 'OK') 

        # This says "Send an SMS to..."
        self.fona.request('AT+CMGS="{}"'.format(number), '>') 

        # And we enter one line of SMS at a time
        print "Spooling message"
        for line in re.split("[\n\r]+", message): 
            self.fona.request(line, '>')

        # The magic ^Z (ASCII character 26) tells the fona we're done entering text
        print "Sending..."
        self.fona.request(chr(26), 'OK') 
        print "... done"

    def call_phone(self, number):
        self.fona.request(number, 'OK')

    def receive_call(self):
        self.fona.request('ATA', 'OK')

    def hang_up(self):
        self.fona.request('ATH0', 'OK')

    def set_audio(self, mode):
        self.fona.request('AT+CHFA={}'.format(mode), 'OK')

    def set_volume(self, vol):
        self.fona.request('AT+CLVL={}'.format(mode), 'OK')

    def num_sms(self):
        self.fona.request('AT+CMGF=1', 'OK')
        fields = split_response(
            self.fona.request('AT+CPMS?', 'OK'),
            "CPMS"
        )
        return {
            "used" : int(fields[1]),
            "total" : int(fields[2])
        }
        
    def get_sms(self, idx, skip_cmgf = False):
        if not skip_cmgf:
            self.fona.request('AT+CMGF=1', 'OK') 
        self.fona.transmit('AT+CMGR={}'.format(idx))
        response = self.fona.receive()
        while(len(response) > 0):
            line = response[0]
            if line.startswith("+CMGR:"):
                metadata_fields = split_csv(line[7:])
                return {
                    "message": "\n".join(response[1:len(response)-1]),
                    "status": metadata_fields[0],
                    "caller": metadata_fields[1],
                    "date": metadata_fields[3]
                }
            print
            response = response[1:]
        return None

    def delete_sms(self, idx):
        self.fona.request('AT+CMGF=1', 'OK')
        self.fona.request("AT+CMGD={:03d}".format(idx), 'OK')
        
    def receive_event(self, pin, level, tick):
        print "Receiving event"
        event = self.fona.receive()
        if 'RING' in event:
            print "Ring Ring Ring!"
            caller = "Unknown"
            for line in event:
                if line.startswith("+CLIP:"):
                    caller = line[7:]
                    caller = caller.split(",")[0].replace('"', "")
            print "Call from {}".format(caller)
            print event
        else:
            print "Unknown Event: {}".format(event)
        
if __name__ == '__main__':
    test = Fona800()
    #test.send_sms("17163521074", "This is a test!")
    #test.toggle_power()
    for i in range(0, test.num_sms()["total"]):
        print test.get_sms(i+1, skip_cmgf = True)
    #test.delete_sms(1)
    #while True:
    #    print test.battery_status()
    #    sleep(60)
    #sleep(1000)



