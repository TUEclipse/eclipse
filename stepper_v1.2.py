#!/usr/local/bin/python
import sys
import os

# Function that writes a list to a text file.
# This function is used as a means of providing the shuffle player 
# with memory.
def write_to_temp_file(value):
	# Opening/creating temporary text file if it does not exist
        try: 
                with open("list.txt", 'w') as f:
	                f.write(value + '\n')
        except IOError:
                # Letting the user know that an IO error has occured
                print 'Cannot open storage file for writing'
        else:
                # Closing the opened file
                print "File closed"
                f.close()



def main():
	steps = raw_input("How many steps forward? ")
	write_to_temp_file(steps)
	print steps

	# Checking if text file used for memory by the program exists
	if os.path.isfile('list.txt'):
		# Checking if the file used to store the song list ("list.txt") is empty	
		# If text file is empty a new list of random songs is generated and the path
		# for each of the songs is written to the "list.txt" file
		if os.path.getsize('list.txt') == 0:
			write_to_temp_file(steps)
		# If the text file is not empty which signifies its existence the file is read line by line
		if os.path.getsize('list.txt') != 0:	
		
			try:
				# Opening text file used to store the song list for reading
				fp = open("list.txt",'r')
			except IOError:
				print 'Cannot open storage file for reading'
			else:
				# Generating a list of all the song paths read in from the storage text file (list.txt)
				val = [line.rstrip('\n') for line in fp]
				# Closing file that was opened for reading
				fp.close()
				time.sleep(0.1)
				# Deleting the song which was just played from the current list of song paths
				del song_list[i]
				# Writing modified list (with a member/song path deleted) to the text file storing the paths to the songs
				write_to_temp_file(song_list)
				# Starting the process over again
				# Moving on to next song
	else:

		# Generating a random list of songs the path to which is provided by the user via the command line
		# This is performed if the temporary storage file "list.txt" does not exit
		write_to_temp_file(val)
if __name__=="__main__":
	main()
