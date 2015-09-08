import time
import random

import RPi.GPIO as GPIO

# BUTTON PIN : LED PIN
PIN_PAIRS= {
    18:17,
    23:22
    }

GPIO.setmode(GPIO.BCM)

output_states = {}
for button_pin, led_pin in PIN_PAIRS.iteritems():
    GPIO.setup(button_pin, GPIO.IN)

    GPIO.setup(led_pin, GPIO.OUT)
    output_states[led_pin] = {'value':False, 'time':0}

def checkInput(pin):
    return GPIO.input(pin)

def checkOutput(pin):
    return output_states[led_pin]['value']

def setOutput(pin):
    GPIO.output(pin, 1)
    output_states[pin]['time'] = time.time()
    output_states[pin]['value'] = True

def getTimeTaken(pin):
    return time.time() - output_states[pin]['time']

def resetOutputs():
    for button_pin, led_pin in PIN_PAIRS.iteritems():
        GPIO.output(led_pin, 0)
        output_states[led_pin]['value'] = False

def randomOutput():
    resetOutputs()
    time.sleep(random.uniform(1,5))
    setOutput(random.choice(PIN_PAIRS.values()))

correct = 0
incorrect = 0
n = 0

# Initial random LED
randomOutput()

while n < 30:
    for button_pin, led_pin in PIN_PAIRS.iteritems():
        if checkInput(button_pin):
            if checkOutput(button_pin):
                correct +=1
                print "It took you %s seconds" % getTimeTaken(led_pin)
                print "correct=%s" % correct
                n +=1               
            else:
                incorrect +=1
                print "incorrect=%s" % incorrect
                n +=1
                

            randomOutput()

    time.sleep(0.01)

GPIO.cleanup()
