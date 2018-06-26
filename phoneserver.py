from scratra import broadcast, start, update
import scratra

@start
def whenstart(scratch):
    print "Hello World"

@broadcast('hi')
def hi(scratch):
    print "Scratch Says Hi"

@broadcast('ping')
def ping(scratch):
    scratch.broadcast('pong')

@update('test')
def test_update(scratch, value):
    print "Updated variable to {}".format(value)

scratra.run()

