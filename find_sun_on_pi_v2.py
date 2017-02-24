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

# defaults to using the PiCamera
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--picamera", type=int, default=-1, help="whether the PiCamera being used")
args = vars(ap.parse_args())

vs = VideoStream(usePiCamera=args["picamera"] > 0).start()  # starts video capture using PiCamera
time.sleep(2.0)


def main(argv):
    bright_values = {} # creates an array of the brightest values
    count = 0

    while True:
        if count == 7: # looks for 7 different spots
            break

        frame = vs.read() # reads the frame from the OpenCV object
        frame = imutils.resize(frame, width=400) # resizing the frame in case frame was changed previously

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
        out, threshold = cv2.threshold(blur, brightest_value - 10, 230, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        time.sleep(1)

        if os.path.isfile('mem.txt'): # finds txt file
            fp = open("mem.txt", 'r')
            current_val = [int(n) for n in fp.read().split()] # reads current position
            print "current_val", current_val[0], "out", out
            bright_values[int(current_val[0])] = out # found the brightest value and storing

        else:
            bright_values[257] = out

        count = count + 1 # counter to happen 7 times

        t = Stepper(0, 0)
        t.change_position_scan() # moves stepper to scan

    print bright_values
    i = 0

    for w in sorted(bright_values, key=bright_values.get, reverse=True): # sorts the 7 brightest values
        if i > 0:
            break
        print w, bright_values[w] # prints all values
        required_pos = w
        i = i + 1

    print "required_pos", required_pos
    t.return_to_bright_spot(required_pos) # found required spot

    while True:

        frame = vs.read()
        frame = imutils.resize(frame, width=400)

        # Converting captured frame to monochrome
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Blurring the image using the GaussianBlur() method of the opencv object
        blur = cv2.GaussianBlur(gray, (9, 9), 0)

        # Using an opencv method to identify the threshold intensities and locations
        (darkest_value, brightest_value, darkest_loc, brightest_loc) = cv2.minMaxLoc(blur)
        print "Brightest Value:", brightest_value
        # Threshold the blurred frame accordingly
        # First argument is the source image, which is the grayscale image. Second argument is the threshold value
        # which is used to classify the pixel values. Third argument is the maxVal which represents the value to be given
        # if pixel value is more than (sometimes less than) the threshold value
        out2, threshold2 = cv2.threshold(blur, brightest_value - 10, 230, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        out, threshold = cv2.threshold(blur, brightest_value - 10, 230, cv2.THRESH_BINARY)
        thr = threshold.copy()
        print "out value:", out2
        # Resize frame for ease
        # cv2.resize(thr, (300, 300))
        # Find contours in thresholded frame
        edged = cv2.Canny(threshold, 50, 150)

        # First one is source image, second is contour retrieval mode, third is contour approximation method. And it outputs
        # the contours and hierarchy. Contours is a Python list of all the contours in the image. Each individual contour
        # is a Numpy array of (x,y) coordinates of boundary points of the object.
        lightcontours, hierarchy = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Checking if the list of contours is greater than 0 and if any circles are detected
        if (len(lightcontours)):
            # Finding the maxmimum contour, this is assumed to be the light beam
            maxcontour = max(lightcontours, key=cv2.contourArea)
            # Avoiding random spots of brightness by making sure the contour is reasonably sized
            if cv2.contourArea(maxcontour):
                (x, final_y), radius = cv2.minEnclosingCircle(maxcontour) # drawing circle

                print "x value:", x, "y value:", final_y

                t = Stepper(x, final_y)
                t.change_position()
                cv2.circle(frame, (int(x), int(final_y)), int(radius), (0, 255, 0), 4)
                cv2.rectangle(frame, (int(x) - 5, int(final_y) - 5), (int(x) + 5, int(final_y) + 5), (0, 128, 255), -1) # creating frame
                # Display frames and exit
            #       cv2.imshow('light', thr)
        cv2.imshow('frame', frame) # showing frame
        cv2.waitKey(4)
        key = cv2.waitKey(1)

        if cv2.waitKey(1) & 0xFF == ord('q'): # q TERMINATES PROGRAM
            break
    cap.release()
    cv2.destroyAllWindows() # KILLS ALL WINDOWS


if __name__ == '__main__':
    main(sys.argv)
