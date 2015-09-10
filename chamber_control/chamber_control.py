#!/usr/bin/python

import time
import random
import RPi.GPIO as GPIO
from collections import namedtuple

#-----------------------------------------------------------------------
# Global var defs
#-----------------------------------------------------------------------

total_num_trials = 0
task_0_num_trials = 0
task_1_num_trials = 0
task_2 num_trials = 0
task_3_num_trials = 0

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
# Task defs.
#
# NOTE: The order/numbering of the tasks doesn't matter. It only matters
# that the strings match the appropriate function and that they are
# stored 0-3 in the task list
#-----------------------------------------------------------------------

NUM_TASKS = 4
TASK_0_STRING = "Lever matched to light"
TASK_1_STRING = "Lever mismatched to light"
TASK_2_STRING = "Right lever is correct"
TASK_3_STRING = "Left lever is correct"

def task_0_lever_and_light_match():
	print "Task 0: Lever and light match"

def task_1_lever_and_light_mismatch():
	print "Task 1: Lever and light are mismatched"

def task_2_right_lever_correct():
	print "Task 2: Right lever is correct"

def task_3_left_lever_correct():
	print "Task 3: Left lever is correct"

Task = namedtuple('Task', 'index function string')
task_0 = Task(0, task_0_lever_and_light_match, TASK_0_STRING)
task_1 = Task(1, task_1_lever_and_light_mismatch, TASK_1_STRING)
task_2 = Task(2, task_2_right_lever_correct, TASK_2_STRING)
task_3 = Task(3, task_3_left_lever_correct, TASK_3_STRING)

# Create a dictionary for the tasks where index is the key.
task_dict = {0:task_0, 1:task_1, 2:task_2, 3:task_3}

#-----------------------------------------------------------------------
#
#-----------------------------------------------------------------------

# Use Broadcom pin number scheme
GPIO.setmode(GPIO.BCM)

for current_pair in pair_list:
	GPIO.setup(current_pair.light_pin, GPIO.OUT)
	GPIO.setup(current_pair.lever_pin, GPIO.IN)

# Seed the random number generator with system time (default)
random.seed()

for i in range(0, NUM_TASKS):
	random_task_index = random.randint(0, NUM_TASKS-1)
	cur_task = task_dict.get(random_task_index)

	# If the random index chosen has already been done, try again
	while (None == cur_task):
		random_task_index = random.randint(0, NUM_TASKS-1)
		cur_task = task_dict.get(random_task_index)

	(cur_task.function)()

	# Remove the task from the dictionary now that it's complete
	task_dict.pop(random_task_index)

print "Test complete."

GPIO.cleanup()
