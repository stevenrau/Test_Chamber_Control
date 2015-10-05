# Test Chamber Control

Task Definitions:
----------------
-> Task 0: Task in which the lever matches the light

-> Task 1: Task in which the lever is mismatched with the light

-> Task 2: Task in which only the right lever is correct

-> Task 3: Task in which only the left lever is correct

How To Use:
------------
(1) To start the program (start a new testing session) you can either:

	(a) Double-click the "Test Chamber Control" icon on the desktop, OR
	(b) Via the console, navigate to ~/repos/Test_Chamber_Control/chamber_control and
            run the command 'sudo ./chamber_control.py'

(2) Once the program is running, the current task being run and trial progress will
    be printed to the screen. If you wish to quit the session before it completes,
    pressing "ctl-c" will kill the program. If any lights are on when you do this,
    they will remain on until the power source is removed or the program is run again.

(3) At the end of the session, a prompt will appear asking if you would like to exit
    or view a stats summary. If you want to:

	(a) View the stats summary, type "stats" and press enter
        (b) Exit the program, type "exit" and press enter

(4) Once the sessions completes, all statistics gathered will be saved in a folder
    named "Test_Results" located in the top level of the home directory.

(5) Within the "Test_Results" folder, a directory will be created for each session,
    named based on the date-time when the session was run.

(6) Within the session-specific folder, there will be 6 files containing tab-delimeted
    statistics about the test and individual trials.
