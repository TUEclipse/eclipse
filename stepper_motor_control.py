import RPi.GPIO as GPIO
import time # including module to implement delays

# Clockwise
#1001
#0011
#0110
#1100

# Function that will turn the stepper motor clockwise
def turn_right():

# Defining which GPIO pins were used on the Raspberry Pi
	x = 1
	a = 31
	b = 33
	c = 35
	d = 37

	while (x > 0):
		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(a, GPIO.OUT)
		GPIO.setup(b, GPIO.OUT)
		GPIO.setup(c, GPIO.OUT)
		GPIO.setup(d, GPIO.OUT)

		GPIO.output(a, True)
		GPIO.output(b, False)
		GPIO.output(c, False)
		GPIO.output(d, True)
		time.sleep(.0035)

		GPIO.output(a, True)
		GPIO.output(b, True)
		GPIO.output(c, False)
		GPIO.output(d, False)
		time.sleep(.0035)

		GPIO.output(a, False)
		GPIO.output(b, True)
		GPIO.output(c, True)
		GPIO.output(d, False)
		time.sleep(.0035)

		GPIO.output(a, False)
 		GPIO.output(b, False)
       	GPIO.output(c, True)
       	GPIO.output(d, True)
		time.sleep(.0035)

# Function that will turn the stepper motor counterclockwise
def turn_left():

# Defining which GPIO pins were used on the Raspberry Pi
	x = 1
	a = 31
	b = 33
    c = 35
    d = 37

    while (x > 0):
        GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BOARD)
        GPIO.setup(a, GPIO.OUT)
        GPIO.setup(b, GPIO.OUT)
        GPIO.setup(c, GPIO.OUT)
        GPIO.setup(d, GPIO.OUT)

	    GPIO.output(a, False)
	    GPIO.output(b, False)
	    GPIO.output(c, True)
		GPIO.output(d, True)
		time.sleep(.0035)
	
		GPIO.output(a, False)
        GPIO.output(b, True)
        GPIO.output(c, True)
        GPIO.output(d, False)
        time.sleep(.0035)

		GPIO.output(a, True)
		GPIO.output(b, True)
		GPIO.output(c, False)
		GPIO.output(d, False)
		time.sleep(.0035)

		GPIO.output(a, True)
		GPIO.output(b, False)
		GPIO.output(c, False)
		GPIO.output(d, True)
		time.sleep(.0035)
		
turn_left()
GPIO.cleanup()
