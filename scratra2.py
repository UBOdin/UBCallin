# scratra ~ 0.3
# greatdane ~ easy python implementation with scratch
# inspired by sinatra(sinatrarb.com) ~ code snippets from scratch.py(bit.ly/scratchpy)
# modified by Oliver Kennedy (okennedy@buffalo.edu)

import socket
from errno import *
from array import array
import threading
from time import sleep
from struct import unpack

# Errors from scratch.py
class ScratchConnectionError(Exception): pass   
class ScratchNotConnected(ScratchConnectionError): pass
class ScratchConnectionRefused(ScratchConnectionError): pass
class ScratchConnectionEstablished(ScratchConnectionError): pass

class ScratchInvalidValue(Exception): pass

broadcast_map = {}
update_map = {}
start_list = []
end_list = []
scratchSocket = None

# For general convenience, scratch interface
class Scratch:

  def __init__(self):
    # Variables interface
    self.var_values = {}
  
  # Broadcast interface
  def broadcast(self, *broadcasts):
    global scratchSocket
    print scratchSocket
    for broadcast_name in broadcasts:
      scratchSocket.send(toScratchMessage('broadcast "' + broadcast_name + '"'))

  def __setitem__(self, var_name, value):
    global scratchSocket
    print scratchSocket
    if isinstance(value, str):
      scratchSocket.send(toScratchMessage('sensor-update "' + var_name +'" "'+value+'"'))
      self.var_values[var_name] = value
    elif isinstance(value, int) or isinstance(value, float):
      self.var_values[var_name] = value
      scratchSocket.send(toScratchMessage('sensor-update "' + var_name +'" ' + str(value)))
    else:
      raise ScratchInvalidValue(var_name + ': Incorrect attempted value')

  # Variable interface
  def __getitem__(self, var_name):
    return self.var_values[var_name]

  def receive(self, msg):
    fields = msg.split(' ')
    command = fields[0]
    if command == 'broadcast':
      msg = fields[1][1:-1]
      if msg in broadcast_map:
        for func in broadcast_map[msg]:
          func(self)
    elif command == 'sensor-update':
      msg = fields[1:]
      i = 0
      while i < len(msg)-1:
        self.var_values[atom(msg[i])] = atom(msg[i+1])
        if atom(msg[i]) in update_map:
          for func in update_map[atom(msg[i])]:
            func(self, atom(msg[i+1]))
        i+=2
    else:
      print "Unsupported message from scratch: {}".format(msg)


def run(host = "localhost",
        port = 42001,
        poll = True,
        reconnect = True, 
        scratchInterface = Scratch()):
  global scratchSocket
  attempt_connection = True
  while attempt_connection:
    print "Attempting Connection to Scratch"
    while True:
      try: 
        scratchSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        scratchSocket.connect((host, port))
      except socket.error as error:
        (err, msge) = error
        if err == EISCONN:
          raise ScratchConnectionEstablished('Already connected to Scratch')
        elif poll == True:
          sleep(1)
          continue
        elif err == ECONNREFUSED:
          raise ScratchConnectionRefused('Connection refused, try enabling remote sensor connections')
        else:
          raise ScratchConnectionError(msge)
      break

    print "Connected to Scratch"

    for func in start_list:
      func(scratchInterface)

    while True:
      try:
        msg_size_data = ""
        while len(msg_size_data) < 4:
          new_data = scratchSocket.recv(4 - len(msg_size_data))
          if len(new_data) > 0:
            msg_size_data = msg_size_data + new_data
          else:
            print "Connection failed."
            break
          #print "Size now {}:{}/{}/{}/{}".format(len(msg_size_data), ord(msg_size_data[0]), ord(msg_size_data[1]), ord(msg_size_data[2]), ord(msg_size_data[3]))
        if len(msg_size_data) < 4:
          break
        msg_size = 0
        for i in range(0, 4):
          msg_size *= 256
          msg_size += ord(msg_size_data[i])
        print "Reading {} bytes".format(msg_size)
        msg = ""
        while len(msg) < msg_size:
          msg = msg + scratchSocket.recv(msg_size - len(msg))
        print "Got {}".format(msg)
      except socket.error as (errno, message):
        print "Error {}: {}\nEnding current connection".format(errno, message)
        scratchSocket.close()
        break
      scratchInterface.receive(msg)

    for func in end_list:
      func(scratchInterface)

    attempt_connection = reconnect

def toScratchMessage(cmd):
  print "Sending '{}'".format(cmd)
  # Taken from chalkmarrow
  n = len(cmd)
  a = array('c')
  a.append(chr((n >> 24) & 0xFF))
  a.append(chr((n >> 16) & 0xFF))
  a.append(chr((n >>  8) & 0xFF))
  a.append(chr(n & 0xFF))
  return a.tostring() + cmd

def atom(msg):
  try:
    return int(msg)
  except:
    try:
      return float(msg)
    except:
      return msg.strip('"')

# For user convenience, decorator methods

# When Scratch broadcasts this...
# @broadcast('scratch_broadcast')
# def func(scratch): ....
class broadcast:
    
    def __init__(self, broadcast):
        self.b = broadcast
        
    def __call__(self, func):
        if self.b in broadcast_map:
            broadcast_map[self.b].append(func)
        else:
            broadcast_map[self.b] = [func]
        
# When this variable is updated...
# @update('variable')
# def func(scratch, value): ...
class update:
    
    def __init__(self, update):
        self.u = update
        
    def __call__(self, func):
        if self.u in update_map:
            update_map[self.u].append(func)
        else:
            update_map[self.u] = [func]

# When we start listening...
# @start
# def func(scratch): ...
def start(func):
    if func not in start_list:
        start_list.append(func)

# When we stop listening
# @end
# def func(scratch): ...
def end(func):
    if func not in end_list:
        end_list.append(func)
