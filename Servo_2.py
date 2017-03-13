# Servo Control
import time
import wiringpi

class Servo:

	def __init__(self,y_raw):
        	self.y_raw = y_raw


	# use 'GPIO naming'
	wiringpi.wiringPiSetupGpio()

	# set #18 to be a PWM output
	wiringpi.pinMode(18, wiringpi.GPIO.PWM_OUTPUT)

	# set the PWM mode to milliseconds stype
	wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)

	# divide down clock
	wiringpi.pwmSetClock(192)
	wiringpi.pwmSetRange(2000)

	delay_period = 0.01

	# Side-note 210 is 2.1 ms
	# pulse = 213 (90 degrees to the right from the reference)
	# pulse = 53 (90 degrees to the left from the reference)	
	# pulse = 133 (reference)

	# one degree of movement corresponds to 0.888 ms


	def move_servo(self):

		print "Y_Poisition", self.y_raw
		
                if self.y_raw >= 150:
			angle = int((self.y_raw - 150) * 41.4/300)
                	# Pulse width given in millisecond
			print "Inside 1st if angle = ",angle
                	pulse_width = 133 + int(0.888*angle)
                        wiringpi.pwmWrite(18,pulse_width)
                        time.sleep(Servo.delay_period)
                elif self.y_raw <= 150:
                        angle = int((self.y_raw - 150) * 41.4/300)
                	# Pulse width given in milliseconds
			print "Inside 2nd if angle = ",angle
                	pulse_width = 133 + int(0.888*angle)
			wiringpi.pwmWrite(18,pulse_width)
                        time.sleep(Servo.delay_period)




if __name__ == "__main__":
        main()


