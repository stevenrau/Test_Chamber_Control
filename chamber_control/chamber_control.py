#!/usr/bin/python

import time
import datetime
import random
import os
import RPi.GPIO as GPIO
from collections import namedtuple

#-----------------------------------------------------------------------
# Global var and constant defs
#-----------------------------------------------------------------------

NUM_TASKS = 4
MIN_NUM_TRIALS = 5
REQ_NUM_CONSEC_SUCCESS = 3
MAX_NUM_TOTAL_TRIALS = MIN_NUM_TRIALS * NUM_TASKS

total_num_trials = 0
task_0_num_trials = 0
task_1_num_trials = 0
task_2_num_trials = 0
task_3_num_trials = 0

test_date_and_time = ""
total_test_time_sec = 0.0

task_0_time_sec = 0.0
task_1_time_sec = 0.0
task_2_time_sec = 0.0
task_3_time_sec = 0.0

#-----------------------------------------------------------------------
# General-use function defs
#-----------------------------------------------------------------------

def get_opposite_pair(pair):

	if (RIGHT_LIGHT_PIN == pair.light_pin):
		opposite_pair = left_pair
	else:
		opposite_pair = right_pair

	return opposite_pair


def update_task_stats_list(task_id, trial_info):

	global task_stats_dict
	stats_list = task_stats_dict.get(task_id)
	stats_list.append(trial_info)

def update_global_trials_stats_list(trial_info):

	global global_trial_stats_list
	global_trial_stats_list.append(trial_info)


def dispense_pellet():

	GPIO.output(PELLET_DISPENSER_PIN, GPIO.HIGH)
	time.sleep(1)
	GPIO.output(PELLET_DISPENSER_PIN, GPIO.LOW)


def run_random_correct_lever_trials(light_lever_match, task_id):

	global total_num_trials
	consecutive_successes = 0
	task_success = False
	task_num_trials = 0

	#Repeat trial until 10 consecutive successes have been made after a minimum of 30 trials
	while ((not task_success) or (task_num_trials < MIN_NUM_TRIALS)):

		#If we've reached the maximum allowed total num trials, return
		if (total_num_trials >= MAX_NUM_TOTAL_TRIALS):
			print "Abandoning task because max number of total trials was reached"
			return task_num_trials

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

		start = time.clock()

		while (not trial_response):
			if (GPIO.input(correct_lever) == 1):
				trial_response = True
				trial_success = True
				consecutive_successes += 1
				dispense_pellet()
			elif (GPIO.input(incorrect_lever) == 1):
				trial_response = True
				trial_success = False
				consecutive_successes = 0

		end = time.clock()
		total_trial_time = (end - start)
		print "Trial", total_num_trials, ": %s." % "Success" if trial_success else "Failure. ", "Time elapsed: %.2f" % total_trial_time, "seconds."

		if (consecutive_successes >= REQ_NUM_CONSEC_SUCCESS):
			task_success = True

		total_num_trials += 1
		task_num_trials += 1
		GPIO.output(cur_rand_light, GPIO.LOW)

		#Create the trial stats tuple and use it to update the stats lists
		trial_info = Trial_Info(total_num_trials-1, task_id, trial_success, total_trial_time)
		update_task_stats_list(task_id, trial_info)
		update_global_trials_stats_list(trial_info)


		#If the lever is still being pressed, wait to continue until it's released
		while (GPIO.input(RIGHT_LEVER_PIN) or GPIO.input(LEFT_LEVER_PIN)):
			pass


	return task_num_trials



def run_one_correct_lever_trials(correct_pair, task_id):

	global total_num_trials
	consecutive_successes = 0
	task_success = False
	task_num_trials = 0

	if correct_pair.lever_pin == RIGHT_LEVER_PIN:
		incorrect_pair = left_pair
	else:
		incorrect_pair = right_pair

	#Repeat trial until 10 consecutive successes have been made after a minimum of 30 trials
	while ((not task_success) or (task_num_trials < MIN_NUM_TRIALS)):

		#If we've reached the maximum allowed total num trials, return
		if (total_num_trials >= MAX_NUM_TOTAL_TRIALS):
			print "Abandoning task because max number of total trials was reached"
			return task_num_trials

		light_wait_time = random.randint(1, 5)
		time.sleep(light_wait_time)

		#Pick a random light and turn it on
		cur_rand_light = (random.choice(pair_list)).light_pin
		GPIO.output(cur_rand_light, GPIO.HIGH)

		trial_response = False

		start = time.clock()

		while (not trial_response):
			if (GPIO.input(correct_pair.lever_pin) == 1):
				trial_response = True
				trial_success = True
				consecutive_successes += 1
				dispense_pellet()
			elif (GPIO.input(incorrect_pair.lever_pin) == 1):
				trial_response = True
				trial_success = False
				consecutive_successes = 0

		end = time.clock()
		total_trial_time = (end - start)
		print "Trial", total_num_trials, ": %s." % "Success" if trial_success else "Failure. ", "Time elapsed: %.2f" % total_trial_time, "seconds."

		if (consecutive_successes >= REQ_NUM_CONSEC_SUCCESS):
			task_success = True

		total_num_trials += 1
		task_num_trials += 1
		GPIO.output(cur_rand_light, GPIO.LOW)

		#Create the trial stats tuple and use it to update the stats lists
		trial_info = Trial_Info(total_num_trials-1, task_id, trial_success, total_trial_time)
		update_task_stats_list(task_id, trial_info)
		update_global_trials_stats_list(trial_info)

		#If the lever is still being pressed, wait to continue until it's released
		while (GPIO.input(RIGHT_LEVER_PIN) or GPIO.input(LEFT_LEVER_PIN)):
			pass


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
TASK_0_STRING = "Task 0: \"Lever matched to light\""
TASK_1_STRING = "Task 1: \"Lever mismatched to light\""
TASK_2_STRING = "Task 2: \"Right lever is correct\""
TASK_3_STRING = "Task 3: \"Left lever is correct\""

def task_0_lever_and_light_match():
	print TASK_0_STRING
	global task_0_time_sec
	global task_0_num_trials

	task_0_start_time = time.clock()

	task_0_num_trials = run_random_correct_lever_trials(True, 0)

	task_0_time_sec = time.clock() - task_0_start_time
	print "\tTotal task 0 num trials", task_0_num_trials
	print "\tTask 0 time elapsed:"  , datetime.timedelta(seconds = int(task_0_time_sec))


def task_1_lever_and_light_mismatch():
	print TASK_1_STRING
	global task_1_time_sec
	global task_1_num_trials

	task_1_start_time = time.clock()

	task_1_num_trials = run_random_correct_lever_trials(False, 1)

	task_1_time_sec = time.clock() - task_1_start_time
	print "\tTotal task 1 num trials", task_1_num_trials
	print "\tTask 1 time elapsed:"  , datetime.timedelta(seconds = int(task_1_time_sec))


def task_2_right_lever_correct():
	print TASK_2_STRING
	global task_2_time_sec
	global task_2_num_trials

	task_2_start_time = time.clock()

	task_2_num_trials = run_one_correct_lever_trials(right_pair, 2)

	task_2_time_sec = time.clock() - task_2_start_time
	print "\tTotal task 2 num trials", task_2_num_trials
	print "\tTask 2 time elapsed:"  , datetime.timedelta(seconds = int(task_2_time_sec))



def task_3_left_lever_correct():
	print TASK_3_STRING
	global task_3_time_sec
	global task_3_num_trials

	task_3_start_time = time.clock()

	task_3_num_trials = run_one_correct_lever_trials(left_pair, 3)

	task_3_time_sec = time.clock() - task_3_start_time
	print "\tTotal task 3 num trials", task_3_num_trials
	print "\tTask 3 time elapsed:"  , datetime.timedelta(seconds = int(task_3_time_sec))


Task = namedtuple('Task', 'index function string')
task_0 = Task(0, task_0_lever_and_light_match, TASK_0_STRING)
task_1 = Task(1, task_1_lever_and_light_mismatch, TASK_1_STRING)
task_2 = Task(2, task_2_right_lever_correct, TASK_2_STRING)
task_3 = Task(3, task_3_left_lever_correct, TASK_3_STRING)

# Create a dictionary for the tasks where index is the key.
task_dict = {0:task_0, 1:task_1, 2:task_2, 3:task_3}

#-----------------------------------------------------------------------
# Stats defs
#-----------------------------------------------------------------------

Trial_Info = namedtuple('Trial_Info', 'trial_num task_id success time')
global_trial_stats_list = []
task_0_trial_stats_list = []
task_1_trial_stats_list = []
task_2_trial_stats_list = []
task_3_trial_stats_list = []

task_stats_dict = {0:task_0_trial_stats_list, 1:task_1_trial_stats_list, 2:task_2_trial_stats_list, 3:task_3_trial_stats_list}

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

test_date_and_time = time.strftime("%c")
print test_date_and_time

test_start_time = time.clock()

for i in range(0, NUM_TASKS):

	print ""

	random_task_index = random.randint(0, NUM_TASKS-1)
	cur_task = task_dict.get(random_task_index)

	# If the random index chosen has already been done, try again
	while (None == cur_task):
		random_task_index = random.randint(0, NUM_TASKS-1)
		cur_task = task_dict.get(random_task_index)

	if ((total_num_trials + MIN_NUM_TRIALS) > MAX_NUM_TOTAL_TRIALS):
		print "Not running", cur_task.string, "becuase the trial limit will be reached before task completion."
	else:
		(cur_task.function)()

	#TODO: Remove this. It's only here to show stats gathering is working
	stats = task_stats_dict.get(random_task_index)
	for info in stats:
		print info.trial_num, info.task_id, info.success, info.time

	# Remove the task from the dictionary now that it's complete
	task_dict.pop(random_task_index)


print "\nTest complete."

test_end_time = time.clock()
total_test_time_sec = test_end_time - test_start_time

#TODO: Get rid of this? Or put in a separate function if we want a stats summary
print "Total test time:", datetime.timedelta(seconds = int(total_test_time_sec))

for info in global_trial_stats_list:
	print info.trial_num, info.task_id, info.success, info.time


GPIO.cleanup()
