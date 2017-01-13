#!/usr/local/bin/python2

import RPi.GPIO as GPIO
import time
import sys
import os

class Stepper:

	def __init__(self,x_raw,y_raw):
		self.x_raw = x_raw
                self.y_raw = y_raw
							
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
		 
        def setStep(self,w1, w2, w3, w4):
		GPIO.output(Stepper.coil_A_1_pin, w1)
                GPIO.output(Stepper.coil_A_2_pin, w2)
                GPIO.output(Stepper.coil_B_1_pin, w3)
                GPIO.output(Stepper.coil_B_2_pin, w4)

	def forward(self,delay, steps):
#		print "In forward method"  
		for i in range(0, steps):
	                self.setStep(1, 0, 1, 0)
                        time.sleep(delay)
			self.setStep(0, 1, 1, 0)
	    		time.sleep(delay)
    			self.setStep(0, 1, 0, 1)
    			time.sleep(delay)
		    	self.setStep(1, 0, 0, 1)
	    		time.sleep(delay)
		 
	def backwards(self,delay, steps):
#		print "In backwards method"  
		for i in range(0, steps):
			self.setStep(0, 0, 1, 1)
			time.sleep(delay)
                        self.setStep(0, 1, 1, 0)
                        time.sleep(delay)
                        self.setStep(1, 1, 0, 0)
                        time.sleep(delay)
                        self.setStep(1, 0, 0, 1)
                        time.sleep(delay)					
			 
	def clear(self):
		self.setStep(0, 0, 0, 0)


	def run(self):
		while True:
		    	steps = raw_input("How many steps forward? ")
                        self.forward(int(Stepper.delay) / 1000.0, int(steps))
                        steps = raw_input("How many steps backwards? ")
                        self.backwards(int(Stepper.delay) / 1000.0, int(steps))
                        self.clear()



	# Function that writes a list to a text file.
	# This function is used as a means of providing memory to keep track of the position of the stepper.
	def write_to_temp_file(self,value):
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

	def change_position(self):
		# Horizontal field of view for pi camera: 53.50 +/- 0.13 degrees
		# Convertin pixel value which is the distance from the center pixel (200) 
		degree_val = (self.x_raw-200) * 53.5/400
		steps = int(degree_val * 360/513)
		
		# Positive -- left -- backwards
		if steps > 0:
                        self.backwards(int(Stepper.delay) / 1000.0, abs(steps))
                        self.clear()

		# Negative -- right -- forward
		elif steps < 0:
                        self.forward(int(Stepper.delay) / 1000.0, abs(steps))
                        self.clear()
				
		# Checking if text file used for memory by the program exists
		if os.path.isfile('mem.txt'):
							
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
				self.write_to_temp_file(val)
		
		else:
		
			# Creating a text file with the initial/default position of the stepper motor		
			self.write_to_temp_file(Stepper.initial_val)
		
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
				self.write_to_temp_file(val)
