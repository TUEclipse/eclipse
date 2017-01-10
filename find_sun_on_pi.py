import os
import sys
# import libs
import cv2
#import numpy as np
import time
# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import imutils
# import the necessary packages
#from webcamvideostream import WebcamVideoStream

from threading import Thread
import cv2

class WebcamVideoStream:
	def __init__(self, src=0):
		# initialize the video camera stream and read the first frame
		# from the stream
		self.stream = cv2.VideoCapture(src)
		(self.grabbed, self.frame) = self.stream.read()

		# initialize the variable used to indicate if the thread should
		# be stopped
		self.stopped = False

	def start(self):
		# start the thread to read frames from the video stream
		t = Thread(target=self.update, args=())
		t.daemon = True
		t.start()
		return self

	def update(self):
		# keep looping infinitely until the thread is stopped
		while True:
			# if the thread indicator variable is set, stop the thread
			if self.stopped:
				return

			# otherwise, read the next frame from the stream
			(self.grabbed, self.frame) = self.stream.read()

	def read(self):
		# return the frame most recently read
		return self.frame

	def stop(self):
		# indicate that the thread should be stopped
		self.stopped = True


class VideoStream:
	def __init__(self, src=0, usePiCamera=False, resolution=(320, 240), framerate=32):
		if usePiCamera:
			from pivideostream import PiVideoStream

			self.stream = PiVideoStream(resolution=resolution, framerate=framerate)
		else:
			self.stream = WebcamVideoStream(src=src)

	def start(self):
		return self.stream.start()
	
	def update(self):
		self.stream.update()

	def read(self):
		return self.stream.read()

	def stop(self):
		self.stream.stop()

from imutils.video import VideoStream
import datetime
import argparse
import imutils
import time
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-p", "--picamera", type=int, default=-1, help="whether the PiCamera being used")
args = vars(ap.parse_args())

#video stream
vs = VideoStream(usePiCamera=args["picamera"] > 0).start()
time.sleep(2.0)

# begin streaming
# Creating a VideoCapture object while also specifying which camera will be used for the purpose
# of capturing the video using hte input parameter 0.
cap = cv2.VideoCapture(0)

while True:

    frame = vs.read()
    frame = imutils.resize(frame, width=400)
	
    # initialize the camera and grab a reference to the raw camera capture
#    camera = PiCamera()
 #   rawCapture = PiRGBArray(camera)
 
    # allow the camera to warmup
  #  time.sleep(0.1)
 
    # grab an image from the camera
   # camera.capture(rawCapture, format="bgr")
   # image = rawCapture.array

    # display the image on screen and wait for a keypress
 #   cv2.imshow("Image", image)
 #   cv2.waitKey(0)
 

    #cap=cv2.VideoCapture(camera)

    #ret,frame = cap.read()
    #_, frame = cap.read()

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
    out, threshold = cv2.threshold(blur, brightest_value - 10, 230, cv2.THRESH_BINARY)
    thr = threshold.copy()
    print out
    # Resize frame for ease
    # cv2.resize(thr, (300, 300))
    # Find contours in thresholded frame
    edged = cv2.Canny(threshold, 50, 150)

    # First one is source image, second is contour retrieval mode, third is contour approximation method. And it outputs
    # the contours and hierarchy. contours is a Python list of all the contours in the image. Each individual contour
    # is a Numpy array of (x,y) coordinates of boundary points of the object.
    lightcontours, hierarchy = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Attempting to  find the circle created by the torch illumination on the wal
    circles = cv2.HoughCircles(threshold, cv2.cv.CV_HOUGH_GRADIENT, 1.0, 20,
                               param1=10,
                               param2=15,
                               minRadius=20,
                               maxRadius=100, )

    # Checking if the list of contours is greater than 0 and if any circles are detected
    if (len(lightcontours)):
        # Finding the maxmimum contour, this is assumed to be the light beam
        maxcontour = max(lightcontours, key=cv2.contourArea)
        # Avoiding random spots of brightness by making sure the contour is reasonably sized
        if cv2.contourArea(maxcontour) :
            (x, final_y), radius = cv2.minEnclosingCircle(maxcontour)
            cv2.circle(frame, (int(x), int(final_y)), int(radius), (0, 255, 0), 4)
            cv2.rectangle(frame, (int(x) - 5, int(final_y) - 5), (int(x) + 5, int(final_y) + 5), (0, 128, 255), -1)
            # Display frames and exit
    cv2.imshow('light', thr)
    cv2.imshow('frame', frame)
    cv2.waitKey(4)
    key = cv2.waitKey(1)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
