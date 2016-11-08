import RPi.GPIO as GPIO
GPIO.setwarnings(False)

a = 31
b = 33
c = 35
d = 37

#	GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(a, GPIO.OUT)
GPIO.setup(b, GPIO.OUT)
GPIO.setup(c, GPIO.OUT)
GPIO.setup(d, GPIO.OUT)
	
GPIO.output(a, False)
GPIO.output(b, False)
GPIO.output(c, False)
GPIO.output(d, False)
GPIO.cleanup()	
