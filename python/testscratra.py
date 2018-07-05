from scratra import update, broadcast, start
import scratra
import time

@start
def start(scratch):
  scratch.broadcast('yo')

@broadcast('hi')
def hi(scratch):
  print "HI!"
  scratch.sensor["thingie"] = 10000
  # scratch.broadcast("ahoyooooooooooooooooooo")

@update('test')
def test_updated(scratch, value):
  pass

scratra.run()
#scratra2.run()

