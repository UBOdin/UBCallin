from scratra import broadcast, start, update
import scratra
from fona800 import Fona800
import easygui
import re

phone = None

def incoming_call(phone, caller, scratch):
    scratch.sensor["incoming-number"] = caller
    scratch.broadcast("incoming-call")

@start
def on_start(scratch):
    global phone
    phone = Fona800(
        call_handler = lambda local_phone, caller: incoming_call(local_phone, caller, scratch)
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

@update('outgoing-number')
def new_outgoing_number(scratch, value):
    pass;
    
@broadcast('start-call')
def dial(scratch):
    global phone
    target_number = str(scratch.var("outgoing-number"))
    target_number = re.sub('[^0-9]', "", target_number)
    if(len(target_number) != 10):
        msg = "Invalid Phone Number: '{}'".format(target_number)
        print msg
        scratch.sensor["error_message"] = msg
        scratch.broadcast('error')
    else:
        print "Dialing... '{}'".format(target_number)
        phone.call_phone(target_number)
    
scratra.run()

