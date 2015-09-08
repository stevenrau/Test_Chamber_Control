#!/usr/bin/python

import time
import random
import RPi.GPIO as GPIO
from collections import namedtuple

# Pin defs
LEFT_LIGHT_PIN = 17
LEFT_LEVER_PIN = 18   #TODO: Change to lever operation instead of button
RIGHT_LIGHT_PIN = 22
RIGHT_LEVER_PIN = 23  #TODO: Change to lever operation instead of button

# Create tuples for the left and right light/lever pairs
Light_Lever_Pair = namedtuple('Light_Lever_Pair', 'name light_pin lever_pin')
left_pair = Light_Lever_Pair("Left", LEFT_LIGHT_PIN, LEFT_LEVER_PIN)
right_pair = Light_Lever_Pair("Right", RIGHT_LIGHT_PIN, RIGHT_LEVER_PIN)

pair_list = [left_pair, right_pair]

# Use Broadcom pin number scheme
GPIO.setmode(GPIO.BCM)

for current_pair in pair_list:
	GPIO.setup(current_pair.light_pin, GPIO.OUT)
	GPIO.setup(current_pair.lever_pin, GPIO.IN)

print "Test complete."

GPIO.cleanup()
