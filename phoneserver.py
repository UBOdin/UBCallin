from scratra2 import broadcast, start, update
import scratra2
from fona800 import Fona800
import easygui
import re
import pigpio

BUTTON_PINS = [27, 23, 22, 17]
LED_PIN = 6

gpio = pigpio.pi()
phone = None
global_scratch = None

def incoming_call(phone, caller):
    global global_scratch
    global_scratch["incoming-number"] = caller
    global_scratch.broadcast("incoming-call")

@start
def on_start(scratch):
    global global_scratch
    global phone
    global gpio
    global_scratch = scratch
    if phone == None:
        phone = Fona800(
            call_handler = incoming_call(local_phone, caller),
            gpio = gpio
        ) 
    print "Phone is running"

@broadcast('hi')
def hi(scratch):
    global phone
    connection = phone.check_phone()
    status_string = "Pi Phone is Not Connected"
    if connection != None:
        status_string = "Pi Phone is Connected to {}".format(connection)
    easygui.msgbox(
        status_string,
        title = "Hi from Pi-Phone"
    )

@broadcast('ping')
def ping(scratch):
    scratch.broadcast('pong')

@broadcast('hang-up')
def hang_up(scratch):
    global phone
    print "Hanging Up"
    phone.hang_up()

@broadcast('pick-up')
def pick_up(scratch):
    global phone
    print "Picking Up"
    phone.receive_call()

@broadcast('turn-led-on')
    global gpio
    print "LED On"
    gpio.write(LED_PIN, 1)

@broadcast('turn-led-off')
    global gpio
    print "LED Off"
    gpio.write(LED_PIN, 0)

@update('outgoing-number')
def new_outgoing_number(scratch, value):
    pass;
    
@broadcast('start-call')
def dial(scratch):
    global phone
    target_number = str(scratch["outgoing-number"])
    target_number = re.sub('[^0-9]', "", target_number)
    if(len(target_number) != 10):
        msg = "Invalid Phone Number: '{}'".format(target_number)
        print msg
        scratch["error_message"] = msg
        scratch.broadcast('error')
    else:
        print "Dialing... '{}'".format(target_number)
        phone.call_phone(target_number)
    
def button_pushed(which):
    global global_scratch
    global_scratch.broadcast("button-{}-pressed".format(which))

for i in range(0, len(BUTTON_PINS)):
    v = i+1
    gpio.set_mode(BUTTON_PINS[i], pigpio.INPUT)
    gpio.callback(
        BUTTON_PINS[i],
        pigpio.RISING_EDGE,
        lambda pin, level, tick: button_pushed(v)
    )
gpio.set_mode(LED_PIN, pigpio.OUTPUT)
gpio.write(LED_PIN, 0)



scratra2.run()

