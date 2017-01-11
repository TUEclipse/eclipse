#!/usr/local/bin/python

import sys
import os
import time

#Initial value corresponding to 180 degree point
initial_val = 257

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
