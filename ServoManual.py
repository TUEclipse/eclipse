#!/usr/bin/python2
import time
import wiringpi
import os 

# Defining class for manual servo control
class ServoManual:
	
	# Defining class constructor 
	def __init__(self):
		pass        

        # Using GPIO naming
	wiringpi.wiringPiSetupGpio()

	# Defining pin 18 of the Raspberry Pi to be a PWM output
	wiringpi.pinMode(18, wiringpi.GPIO.PWM_OUTPUT)

	# Setting the PWM mode to milliseconds
	wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)

        # Dividing down clock
        # Pin 18 on the Raspberry Pi declared for the purpose of being a PWM output requires a
        # frequency of 50 Hz for the servo to operate properly.
        # If pwmClock is 192 and pwmRange is 2000 the PWM frequency would be 50 Hz
        # PWM frequency = 19,200,000 Hz / pwmClock / pwmRange = 50 Hz
	wiringpi.pwmSetClock(192)
	wiringpi.pwmSetRange(2000)

	# Defining delay period (given in milliseconds)
	delay_period = 0.01

	# Defining angle by which the servo motor will move up or down  
	# when the corresponding arrow key is pressed by the user
	angle = 10

	# Defining default servo angle
	default = 0

	# Defining angle limit for the servo
	angle_limit = 90

	# Side-note 210 is 2.1 ms
	# pulse = 213 (90 degrees to the right from the reference)
	# pulse = 53 (90 degrees to the left from the reference)	
	# pulse = 133 (reference)

	# one degree of movement corresponds to 0.888 ms

	# Defining a function that writes a list to a text file.
        # This function is used as a means of providing memory to keep track of the position 
	# associated with the servo motor.
        def write_to_temp_file_servo(self,value):

       	        # Opening/creating temporary text file if it does not exist
                try:
                        with open("mem2.txt", 'w') as f:
                                f.write('%d' %int(value))
                except IOError:

                        # Letting the user know that an IO error has occurred
                        print 'Cannot open storage file for writing'
                else:

                        # Closing the opened file
                        f.close()


	# Defining a function used to move the servo motor down 
	def servo_control_down(self):

                # Checking if text file used for memory by the program exists
                if os.path.isfile('mem2.txt'):

                        try:
                                # Opening storage file for reading
                                fp = open("mem2.txt",'r')

                        except IOError:

                                print 'Cannot open storage file for reading'


			else:
				
				# Obtaining current position of the servo motor
                                current_val = [int(n) for n in fp.read().split()]

				# Defining the new required angle to which the servo motor
				# has to move after a key press
				required_angle = ServoManual.angle + current_val[0]

				# Preventing the servo motor from moving more than 90 degree from rest
				# since the motor can only span 180 degrees of motion
				if required_angle > ServoManual.angle_limit:
					required_angle = ServoManual.angle_limit
				
				# Calculating the required pulse width corresponding to the desired 
				# servo motor angle/position       	
			        pulse_width = 133 + int(0.888*required_angle)
                                time.sleep(0.1)
				
				# Driving the servo motor
				wiringpi.pwmWrite(18,pulse_width)
                                time.sleep(ServoManual.delay_period)

				# Closing file that was opened for reading
                                fp.close()
				
				# Writing new servo position to temporary storage file
                                self.write_to_temp_file_servo(required_angle)
                else:

                        # Creating a text file with the initial/default position of the servo motor
			self.write_to_temp_file_servo(ServoManual.default)
                        try:
                                 # Opening storage file for reading
                                fp = open("mem2.txt",'r')
                        except IOError:

                                print 'Cannot open storage file for reading'

                        else:
				# Calculating the required pulse width corresponding to the desired 
                                # servo motor angle/position 
				pulse_width = 133 + int(0.888*ServoManual.angle)

             			time.sleep(0.1)

				# Driving the servo motor
		   		wiringpi.pwmWrite(18,pulse_width)
                		time.sleep(ServoManual.delay_period)

                                # Closing file that was opened for reading
                                fp.close()
                                self.write_to_temp_file_servo(ServoManual.angle)

	# Defining a function used to move the servo motor up 
	def servo_control_up(self):

                # Checking if text file used for memory by the program exists
                if os.path.isfile('mem2.txt'):

                        try:
                                 # Opening storage file for reading
                                fp = open("mem2.txt",'r')

                        except IOError:

                                print 'Cannot open storage file for reading'


			else:

				# Obtaining current position of the servo motor
                                current_val = [int(n) for n in fp.read().split()]

				# Defining the new required angle to which the servo motor
				# has to move after a key press
				required_angle = current_val[0] - ServoManual.angle 
				
				# Preventing the servo motor from moving more than 90 degree from rest
				# since the motor can only span 180 degrees of motion	
				if required_angle < -ServoManual.angle_limit:
					required_angle = -ServoManual.angle_limit
				      	
				# Calculating the required pulse width corresponding to the desired 
				# servo motor angle/position  
			        pulse_width = 133 + int(0.888*required_angle)

                                time.sleep(0.1)
					
				# Driving the servo motor
				wiringpi.pwmWrite(18,pulse_width)
                                time.sleep(ServoManual.delay_period)
				
				# Closing file that was opened for reading
                                fp.close()

				# Writing new servo position to temporary storage file
                                self.write_to_temp_file_servo(required_angle)
                else:

                        # Creating a text file with the initial/default position of the servo motor
			self.write_to_temp_file_servo(ServoManual.default)
                        try:
                                 # Opening storage file for reading
                                fp = open("mem2.txt",'r')
                        except IOError:

                                print 'Cannot open storage file for reading'

                        else:
			
				# Calculating the required pulse width corresponding to the desired 
                                # servo motor angle/position 
				pulse_width = 133 + int(0.888*-ServoManual.angle)

             			time.sleep(0.1)
				
				# Driving the servo motor
		   		wiringpi.pwmWrite(18,pulse_width)
                		time.sleep(ServoManual.delay_period)

                                # Closing file that was opened for reading
                                fp.close()
				
				# Writing new servo position to the temporary storage file
                                self.write_to_temp_file_servo(-ServoManual.angle)



if __name__ == "__main__":
        main()


