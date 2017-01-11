#!/usr/local/bin/python2

import RPi.GPIO as GPIO
import time
import sys
import os

# This delay value is in milliseconds
delay = 4 

# Initial value corresponding to 180 degree point
initial_val = 257

# Setting up the pins 
coil_A_1_pin = 31
coil_A_2_pin = 33
coil_B_1_pin = 35
coil_B_2_pin = 37
 
 
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(coil_A_1_pin, GPIO.OUT)
GPIO.setup(coil_A_2_pin, GPIO.OUT)
GPIO.setup(coil_B_1_pin, GPIO.OUT)
GPIO.setup(coil_B_2_pin, GPIO.OUT)
 
def forward(delay, steps):  
        for i in range(0, steps):
                setStep(1, 0, 1, 0)
                time.sleep(delay)
                setStep(0, 1, 1, 0)
                time.sleep(delay)
                setStep(0, 1, 0, 1)
                time.sleep(delay)
                setStep(1, 0, 0, 1)
                time.sleep(delay)
 
def backwards(delay, steps):  
        for i in range(0, steps):
                setStep(0, 0, 1, 1)
                time.sleep(delay)
                setStep(0, 1, 1, 0)
                time.sleep(delay)
                setStep(1, 1, 0, 0)
                time.sleep(delay)
                setStep(1, 0, 0, 1)
                time.sleep(delay)
            
def setStep(w1, w2, w3, w4):
        GPIO.output(coil_A_1_pin, w1)
        GPIO.output(coil_A_2_pin, w2)
        GPIO.output(coil_B_1_pin, w3)
        GPIO.output(coil_B_2_pin, w4)
     
def clear():
        setStep(0, 0, 0, 0)



def main():

        while True:
                delay = 4 # This delay value is in milliseconds
                steps = raw_input("How many steps forward? ")
                forward(int(delay) / 1000.0, int(steps))
                steps = raw_input("How many steps backwards? ")
                backwards(int(delay) / 1000.0, int(steps))
                clear()



# Function that writes a list to a text file.
# This function is used as a means of providing memory to keep track of the position of the stepper.
def write_to_temp_file(value):
	# Opening/creating temporary text file if it does not exist
        try: 
                with open("mem.txt", 'w') as f:
			f.write('%d' %int(value))
        except IOError:

                # Letting the user know that an IO error has occured
                print 'Cannot open storage file for writing'
        else:
                # Closing the opened file
                print "File closed"
                f.close()

def main():

	steps = raw_input("How many steps forward? ")

	# Checking if text file used for memory by the program exists
	if os.path.isfile('mem.txt'):

		# If the text file is not empty which signifies its existence the file is read line by line
		if os.path.getsize('mem.txt') != 0:	
			
			try:
				# Opening storage file for reading
				fp = open("mem.txt",'r')

			except IOError:

				print 'Cannot open storage file for reading'
			else:

				current_val = [int(n) for n in fp.read().split()]
				val = int(current_val[0]) + int(steps)
			
				# Closing file that was opened for reading
				fp.close()

				write_to_temp_file(val)
	else:
		# Creating a text file with the initial/default position of the stepper motor		
		write_to_temp_file(initial_val)


if __name__=="__main__":
	main()

