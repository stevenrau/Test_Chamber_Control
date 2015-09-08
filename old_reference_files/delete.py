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

log1=[]
correct = 0
incorrect = 0

#move the levers into the box here. how??

# Initial random LED
randomOutput()

#Task 1 - button matched to light

while True:
    for button_pin, led_pin in PIN_PAIRS.iteritems():
        if checkInput(button_pin):
            if checkOutput(button_pin):
                log1.append(1)
                correct+=1
                #dispense food
                print "%s seconds" % getTimeTaken(led_pin)
                print "correct=%s" %correct
            else:
                log1.append(0)
                incorrect+=1
                print "%s seconds" % getTimeTaken(led_pin)
                print "incorrect=%s" % incorrect

            randomOutput()

    if len(log1)>=30:
        if sum(log1[len(log1)-31:len(log1)])>=25:
            print "Task 1 Complete"
            break
    time.sleep(0.01)

log2=[]
correct = 0
incorrect = 0

#Task 2 - right button correct

while True:
    for button_pin in PIN_PAIRS.iteritems():
        if checkInput(18):
            log2.append(1)
            correct +=1
            #dispense food
            print "%s seconds" % getTimeTaken(led_pin)
            print "correct=%s" %correct
            randomOutput()
        elif checkInput(23):
            log2.append(0)
            incorrect +=1
            print "%s seconds" % getTimeTaken(led_pin)
            print "incorrect=%s" %incorrect
            randomOutput()
    if len(log2)>=30:
        if sum(log2[len(log2)-31:len(log2)])>=25:
            print "Task 2 Complete"
            break

    time.sleep(0.01)

log3=[]
correct = 0
incorrect = 0

#Task 3 - Left button correct

while True:
    for button_pin in PIN_PAIRS.iteritems():
        if checkInput(23):
            log3.append(1)
            correct +=1
            #dispense food
            print "%s seconds" % getTimeTaken(led_pin)
            print "correct=%s" %correct
            randomOutput()
        elif checkInput(18):
            log3.append(0)
            incorrect +=1
            print "%s seconds" % getTimeTaken(led_pin)
            print "incorrect=%s" %incorrect
        
            randomOutput()
    if len(log3)>=30:
        if sum(log3[len(log3)-31:len(log3)])>=25:
            print "Task 3 Complete"
            break

log4=[]
correct = 0
incorrect = 0

#Task 4 - Button mismatched to light

while True:
    for button_pin, led_pin in PIN_PAIRS.iteritems():
        if checkInput(button_pin):
            if checkOutput(button_pin):
                log4.append(0)
                incorrect+=1
                print "%s seconds" % getTimeTaken(led_pin)
                print "incorrect=%s" %incorrect
            else:
                log4.append(1)
                correct+=1
                #dispense food
                print "%s seconds" % getTimeTaken(led_pin)
                print "correct=%s" % correct

            randomOutput()

    if len(log4)>=30:
        if sum(log4[len(log4)-31:len(log4)])>=25:
            print "Task 4 Complete"
            break
    time.sleep(0.01)

#retract levers

GPIO.cleanup()
