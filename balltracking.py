from collections import deque
from imutils.video import VideoStream
import numpy as np
import matplotlib
import argparse
import cv2
import imutils
import time
from matplotlib import pyplot as plt

#construct argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help = "path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64, help="max buffer size")
args = vars(ap.parse_args())

#ddefine lower and upper boundary of green
greenLower = (40, 100, 63)
greenUpper = (80, 255, 255)
pts = deque(maxlen=args["buffer"])

#if a video path is not supplied, grab the reference to the webcam
if not args.get("video", False):
    vs = VideoStream(src=0).start()
else:
    vs = cv2.VideoCapture(args["video"])

time.sleep(2.0)

#keep looping
while True:
    frame=vs.read()
    
    frame=frame[1] if args.get("video", False) else frame

    if frame is None:
        break

    frame = cv2.blur(frame,(5,5))
    frame = imutils.resize(frame, width=600)
    blurred = cv2.GaussianBlur(frame, (11,11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, greenLower, greenUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    

    #find contours in the mask and initialize the current (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    center = None

    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"]/M["m00"]), int(M["m01"]/M["m00"]))

        """if radius > 10:
            cv2.circle(frame, (int(x), int(y)), int(radius), (0,255,255),2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)"""

    pts.appendleft(center)

    for i in range(1, len(pts)):
        if pts[i - 1] is None or pts[i] is None:
            continue

        thickness = int(np.sqrt(args["buffer"]/float(i+1))*2.5)
        cv2.line(frame, pts[i-1], pts[i], (0,0,255), thickness)

    for i in range(len(cnts)):
        x, y, w, h = cv2.boundingRect(cnts[i])
        cv2.rectangle(frame, (x,y),(x+w, y+h),(0,0,255),2)
        

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

if not args.get("video", False):
    vs.stop()
else:
    vs.release()

cv2.destroyAllWindows()