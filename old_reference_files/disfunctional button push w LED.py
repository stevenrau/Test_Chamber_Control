import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN)
GPIO.setup (23, GPIO.IN)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)

import time

correct = 0
incorrect = 0


def LED17_is_on():
    GPIO.output(17, 1)
    GPIO.output(22, 0)
    return
def LED22_is_on():
    GPIO.output(22, 1)
    GPIO.output(17, 0)
    return

while 1:
         
    if LED17_is_on and GPIO.input(18):
        correct = correct + 1
        print "correct1=" +str(correct)
        time.sleep(0.2)
        LED22_is_on()
    time.sleep (0.1)

    if LED17_is_on and GPIO.input(23):
        incorrect = incorrect + 1
        print "incorrect1=" + str(incorrect)
        time.sleep(0.2)
        LED17_is_on()
    time.sleep (0.1)
    while 2:
        if LED22_is_on and GPIO.input(23):
            correct = correct + 1
            print "correct2=" +str(correct)
            time.sleep(0.2)
            LED17_is_on()
        time.sleep(0.1)
        
        if LED22_is_on and GPIO.input(18):
            incorrect = incorrect + 1
            print "incorrect2=" + str(incorrect)
            time.sleep(0.2)
            LED22_is_on()
        time.sleep(0.1)
    
    

    


GPIO.cleanup()
