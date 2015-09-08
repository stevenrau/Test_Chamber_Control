#!/usr/bin/python

import time
import random
import RPi.GPIO as GPIO
from collections import namedtuple

#-----------------------------------------------------------------------
# Pin defs
#-----------------------------------------------------------------------

LEFT_LIGHT_PIN = 17
LEFT_LEVER_PIN = 18   #TODO: Change to lever operation instead of button
RIGHT_LIGHT_PIN = 22
RIGHT_LEVER_PIN = 23  #TODO: Change to lever operation instead of button

# Create tuples for the left and right light/lever pairs
Light_Lever_Pair = namedtuple('Light_Lever_Pair', 'name light_pin lever_pin')
left_pair = Light_Lever_Pair("Left", LEFT_LIGHT_PIN, LEFT_LEVER_PIN)
right_pair = Light_Lever_Pair("Right", RIGHT_LIGHT_PIN, RIGHT_LEVER_PIN)

pair_list = [left_pair, right_pair]

#-----------------------------------------------------------------------
# Task defs. The order/numbering of the tasks doesn't matter. It only matters
# that the strings match the appropriate function and that they are stored 1-4
# in the task list
#-----------------------------------------------------------------------

TASK_1_STRING = "Lever matched to light"
TASK_2_STRING = "Lever mismatched to light"
TASK_3_STRING = "Right lever is correct"
TASK_4_STRING = "Left lever is correct"

def task_1_lever_and_light_match():
	print "Task 1: Lever and light match"

def task_2_lever_and_light_mismatch():
	print "Task 2: Lever and light are mismatched"

def task_3_right_lever_correct():
	print "Task 3: Right lever is correct"

def task_4_left_lever_correct():
	print "Task 4: Left lever is correct"

Task = namedtuple('Task', 'index function string')
task_1 = Task(1, task_1_lever_and_light_match, TASK_1_STRING)
task_2 = Task(2, task_2_lever_and_light_mismatch, TASK_2_STRING)
task_3 = Task(3, task_3_right_lever_correct, TASK_3_STRING)
task_4 = Task(4, task_4_left_lever_correct, TASK_4_STRING)

# Create a dictionary for the tasks where index is key.
task_collection = {1:task_1, 2:task_2, 3:task_3, 4:task_4}

#-----------------------------------------------------------------------
#
#-----------------------------------------------------------------------

# Use Broadcom pin number scheme
GPIO.setmode(GPIO.BCM)

for current_pair in pair_list:
	GPIO.setup(current_pair.light_pin, GPIO.OUT)
	GPIO.setup(current_pair.lever_pin, GPIO.IN)

print "Test complete."

GPIO.cleanup()
