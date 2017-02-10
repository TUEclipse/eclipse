import os
import sys
import cv2
import time
from picamera.array import PiRGBArray
from picamera import PiCamera
from WebcamVideoStream import WebcamVideoStream
from VideoStream import VideoStream
import imutils
from threading import Thread
import cv2
from imutils.video import VideoStream
import datetime
import argparse
from Stepper import Stepper

ap = argparse.ArgumentParser()
ap.add_argument("-p", "--picamera", type=int, default=-1, help="whether the PiCamera being used")
args = vars(ap.parse_args())

vs = VideoStream(usePiCamera=args["picamera"] > 0).start()
time.sleep(2.0)

bright_values = {}
count = 0

while True:
	if count == 7:
		break

        frame = vs.read()
        frame = imutils.resize(frame, width=400)
	
        # Converting captured frame to monochrome
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Blurring the image using the GaussianBlur() method of the opencv object
        blur = cv2.GaussianBlur(gray, (9, 9), 0)

        # Using an opencv method to identify the threshold intensities and locations
        (darkest_value, brightest_value, darkest_loc, brightest_loc) = cv2.minMaxLoc(blur)
        # Threshold the blurred frame accordingly
        # First argument is the source image, which is the grayscale image. Second argument is the threshold value
        # which is used to classify the pixel values. Third argument is the maxVal which represents the value to be given
        # if pixel value is more than (sometimes less than) the threshold value
        out, threshold = cv2.threshold(blur, brightest_value - 10, 230, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

	time.sleep(1)
	if os.path.isfile('mem.txt'):
		fp = open("mem.txt",'r')
                current_val = [int(n) for n in fp.read().split()]
 		print "current_val",current_val[0],"out",out 
		bright_values[int(current_val[0])] = out
					
	else:
        	bright_values[257] = out
	
        count = count + 1
	
	t=Stepper(0,0)
#	t.backwards(int(Stepper.delay) / 1000.0, int(73))
	t.change_position_scan()

print bright_values
i = 0
for w in sorted(bright_values, key=bright_values.get, reverse=True):
	if i > 0:
		break
	print w, bright_values[w]
	required_pos = w
	i = i + 1

print "required_pos",required_pos
t.return_to_bright_spot(required_pos)




