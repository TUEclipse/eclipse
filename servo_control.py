# Servo Control
import time
import wiringpi

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

def move_servo():

	while True:
		angle = int(raw_input("How many degrees? "))
		# Pulse width given in milliseconds
                pulse_width = 133 + int(0.888*angle)
               	if angle >= 0:
			wiringpi.pwmWrite(18,pulse_width)
        		time.sleep(delay_period)
		if angle <= 0:
			wiringpi.pwmWrite(18,pulse_width)
                        time.sleep(delay_period)	
			

def main():

	move_servo()


if __name__ == "__main__":
	main()
