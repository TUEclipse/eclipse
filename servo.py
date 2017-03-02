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


while True:
#        for pulse in range(50, 250, 1):
#                wiringpi.pwmWrite(18, pulse)
#                time.sleep(delay_period)
#        for pulse in range(250, 50, -1):
#                wiringpi.pwmWrite(18, pulse)
#                time.sleep(delay_period)

	wiringpi.pwmWrite(18,93)
	time.sleep(delay_period)
	
