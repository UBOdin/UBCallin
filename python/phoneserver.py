from scratra2 import broadcast, start, update
import scratra2
from fona800 import Fona800
import fona800
import easygui
import re
import pigpio
import sys
import threading
from time import sleep

###### GLOBAL CONFIGURATION
BUTTON_PINS = [27, 23, 22, 17]
LED_PIN = 6

###### Placeholder variables for communicating between different components.
gpio = pigpio.pi()
global_scratch = None

###### Handler for responding to incoming phone calls
def incoming_call(phone, caller):
    global global_scratch
    global_scratch["incoming-number"] = caller
    global_scratch.broadcast("incoming-call")

###### Define the phone interface itself
phone = Fona800(
    call_handler = incoming_call,
    gpio = gpio
)

###### Scratch API handlers
@start
def on_start(scratch):
    print "Connected to scratch!"
    global global_scratch
    global phone
    global gpio
    global_scratch = scratch
    if connect_to_phone_if_needed():
        phone.set_audio(fona800.FONA_AUDIO_EXTERNAL)
    else: 
        easygui.msgbox("Error connecting to FONA")

@broadcast('hi')
def hi(scratch):
    connect_to_phone_if_needed()
    global phone
    status_string = "Pi Phone is Not Connected"
    connection = phone.check_phone()
    if connection != None:
        status_string = "Pi Phone is Connected to {}".format(connection)
    easygui.msgbox(
        status_string,
        title = "Hi from Pi-Phone"
    )

@broadcast('toggle-power')
def toggle_power(scratch):
    global phone
    phone.toggle_power()

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

@broadcast('audio-speaker')
def audio_speaker(scratch):
    global phone
    phone.set_audio(fona800.FONA_AUDIO_EXTERNAL)

@broadcast('audio-headphones')
def audio_headphones(scratch):
    global phone
    phone.set_audio(fona800.FONA_AUDIO_HEADSET)

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

###### Handlers for the PiTFT display
def button_pushed(which):
    global global_scratch
    print "Button {} pressed".format(which)
    global_scratch.broadcast("button-{}-pressed".format(which))

for i in range(0, len(BUTTON_PINS)):
    v = i+1
    gpio.set_mode(BUTTON_PINS[i], pigpio.INPUT)
    gpio.set_pull_up_down(BUTTON_PINS[i], pigpio.PUD_UP)
    print "Setting up button on GPIO-{}".format(BUTTON_PINS[i])
    gpio.callback(
        BUTTON_PINS[i],
        pigpio.FALLING_EDGE,
        lambda pin, level, tick, button=i+1: button_pushed(button)
    )

###### Support for controlling an LED on GPIO-6
gpio.set_mode(LED_PIN, pigpio.OUTPUT)
gpio.write(LED_PIN, 0)

@broadcast('turn-led-on')
def turn_led_on(scratch):
    global gpio
    print "LED On"
    gpio.write(LED_PIN, 1)

@broadcast('turn-led-off')
def turn_led_off(scratch):
    global gpio
    print "LED Off"
    gpio.write(LED_PIN, 0)

####### Finally, asynchronously connect to the FONA and Scratch
class FonaConnectThread(threading.Thread):
    def __init__(self, phone):
        self.phone = phone
        threading.Thread.__init__(self)

    def run(self):
        print "Attempting to connect to FONA..."
        while not phone.try_connect():
            print "... FONA connection failed.  Will try again in 5 seconds."
            sleep(5)
            print "Re-attempting to connect to FONA..."
        print "... FONA connection successful!"

FonaConnectThread(phone).start()
scratra2.run()

