#!/usr/bin/python

import time
import random
import os
import RPi.GPIO as GPIO
from collections import namedtuple

#-----------------------------------------------------------------------
# Global var and constant defs
#-----------------------------------------------------------------------

MIN_NUM_TRIALS = 5
REQ_NUM_CONSEC_SUCCESS = 3

total_num_trials = 0
task_0_num_trials = 0
task_1_num_trials = 0
task_2_num_trials = 0
task_3_num_trials = 0

#-----------------------------------------------------------------------
# General-use function defs
#-----------------------------------------------------------------------

def get_opposite_pair(pair):

	if (RIGHT_LIGHT_PIN == pair.light_pin):
		opposite_pair = left_pair
	else:
		opposite_pair = right_pair

	return opposite_pair


def dispense_pellet():

	GPIO.output(PELLET_DISPENSER_PIN, GPIO.HIGH)
	time.sleep(1)
	GPIO.output(PELLET_DISPENSER_PIN, GPIO.LOW)


def run_random_correct_lever_trials(light_lever_match):

	consecutive_successes = 0
	task_success = False
	task_num_trials = 0

	#Repeat trial until 10 consecutive successes have been made after a minimum of 30 trials
	while ((not task_success) or (task_num_trials < MIN_NUM_TRIALS)):
		light_wait_time = random.randint(1, 5)
		time.sleep(light_wait_time)

		random_pair = random.choice(pair_list)
		cur_rand_light = random_pair.light_pin
		if (light_lever_match):
			correct_lever = random_pair.lever_pin
			incorrect_lever = (get_opposite_pair(random_pair)).lever_pin
		else:
			correct_lever = (get_opposite_pair(random_pair)).lever_pin
			incorrect_lever = random_pair.lever_pin

		# Turn on the current random light
		GPIO.output(cur_rand_light, GPIO.HIGH)

		trial_response = False

		while (not trial_response):
			if (GPIO.input(correct_lever) == 1):
				trial_response = True
				consecutive_successes += 1
				dispense_pellet()
			elif (GPIO.input(incorrect_lever) == 1):
				trial_response = True
				consecutive_successes = 0

		task_num_trials += 1
		GPIO.output(cur_rand_light, GPIO.LOW)

		#If the lever is still being pressed, wait to continue until it's released
		while (GPIO.input(RIGHT_LEVER_PIN) or GPIO.input(LEFT_LEVER_PIN)):
			pass

		if (consecutive_successes >= REQ_NUM_CONSEC_SUCCESS):
			task_success = True

	return task_num_trials



def run_one_correct_lever_trials(correct_pair):

	consecutive_successes = 0
	task_success = False
	task_num_trials = 0

	if correct_pair.lever_pin == RIGHT_LEVER_PIN:
		incorrect_pair = left_pair
	else:
		incorrect_pair = right_pair

	#Repeat trial until 10 consecutive successes have been made after a minimum of 30 trials
	while ((not task_success) or (task_num_trials < MIN_NUM_TRIALS)):
		light_wait_time = random.randint(1, 5)
		time.sleep(light_wait_time)

		#Pick a random light and turn it on
		cur_rand_light = (random.choice(pair_list)).light_pin
		GPIO.output(cur_rand_light, GPIO.HIGH)

		trial_response = False

		while (not trial_response):
			if (GPIO.input(correct_pair.lever_pin) == 1):
				trial_response = True
				consecutive_successes += 1
				dispense_pellet()
			elif (GPIO.input(incorrect_pair.lever_pin) == 1):
				trial_response = True
				consecutive_successes = 0

		task_num_trials += 1
		GPIO.output(cur_rand_light, GPIO.LOW)

		#If the lever is still being pressed, wait to continue until it's released
		while (GPIO.input(RIGHT_LEVER_PIN) or GPIO.input(LEFT_LEVER_PIN)):
			pass

		if (consecutive_successes >= REQ_NUM_CONSEC_SUCCESS):
			task_success = True

	return task_num_trials

#-----------------------------------------------------------------------
# Pin defs
#-----------------------------------------------------------------------

LEFT_LIGHT_PIN = 17
LEFT_LEVER_PIN = 18   #TODO: Change to lever operation instead of button
RIGHT_LIGHT_PIN = 22
RIGHT_LEVER_PIN = 23  #TODO: Change to lever operation instead of button
PELLET_DISPENSER_PIN = 4

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
	global task_0_num_trials
	task_0_num_trials = run_random_correct_lever_trials(True)
	print "Total task 0 num trials", task_0_num_trials


def task_1_lever_and_light_mismatch():
	print "Task 1: Lever and light are mismatched"
	global task_1_num_trials
	task_1_num_trials = run_random_correct_lever_trials(False)
	print "Total task 1 num trials", task_1_num_trials


def task_2_right_lever_correct():
	print "Task 2: Right lever is correct"
	global task_2_num_trials
	task_2_num_trials = run_one_correct_lever_trials(right_pair)
	print "Total task 2 num trials", task_2_num_trials


def task_3_left_lever_correct():
	print "Task 3: Left lever is correct"
	global task_3_num_trials
	task_3_num_trials = run_one_correct_lever_trials(left_pair)
	print "Total task 3 num trials", task_3_num_trials


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

GPIO.setup(PELLET_DISPENSER_PIN, GPIO.OUT)

# Seed the random number generator with system time (default)
random.seed()

for i in range(0, NUM_TASKS):

	print ""

	random_task_index = random.randint(0, NUM_TASKS-1)
	cur_task = task_dict.get(random_task_index)

	# If the random index chosen has already been done, try again
	while (None == cur_task):
		random_task_index = random.randint(0, NUM_TASKS-1)
		cur_task = task_dict.get(random_task_index)

	(cur_task.function)()

	# Remove the task from the dictionary now that it's complete
	task_dict.pop(random_task_index)

dispense_pellet()

print "\nTest complete."

GPIO.cleanup()
