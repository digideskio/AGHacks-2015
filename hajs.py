__author__ = 'plizonczyk'

import cv2
import numpy as np
import time
import pyautogui

cap = cv2.VideoCapture(1)
height_offset = 100

pressedDown = 0
pressedUp = 0
pressedLeft = 0
pressedRight = 0


def find_contours(frame, blurred, roi, left=False):
    try:
        __, contours, __ = cv2.findContours(blurred, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    except ValueError:
        contours, __ = cv2.findContours(blurred, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    max_area = 0
    biggest_contour = None

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > max_area:
            max_area = area
            biggest_contour = contour
    
    if biggest_contour is None:
        return

    cv2.drawContours(roi, [biggest_contour], -1, (255, 0, 0), 3)
    x, y, w, h = cv2.boundingRect(biggest_contour)
    # print cv2.contourArea(biggest_contour)

    cv2.rectangle(roi, (x, y), (x+w, y+h), (0, 255, 0))

    if left:
        cx = int(x+w/2)
        cy = int(y+h/2)
	cv2.line(roi, (cx, 0), (cx, roi.shape[0]), (255, 0, 255), 2)
	cv2.line(roi, (0, cy), (roi.shape[1], cy), (255, 0, 255), 2)

    	cv2.imshow('left', roi)
	do_left(cx, cy)
    else:
    	cv2.imshow('right', roi)
        do_right(max_area)


def do_left(cx, cy):
    print (cx, cy)
    if cy < 120 and pressedDown == 0:
	pyautogui.keyDown("down")
	global pressedDown
	pressedDown = 1
	print "DOWN"
    elif  cy > 160 and pressedUp == 0:
	pyautogui.keyDown("up")
	global pressedUp
	pressedUp = 1
	print "UP"
    elif  cx > 180 and pressedLeft == 0:
	pyautogui.keyDown("left")
	global pressedLeft
	pressedLeft = 1
	print "LEFT"
    elif  cx < 140 and pressedRight == 0:
	pyautogui.keyDown("right")
	global pressedRight
	pressedRight = 1
	print "RIGHT"

    else:
	if pressedDown == 1 and cy > 120:
		global pressedDown
		pressedDown = 0
		pyautogui.keyUp("down")
	if pressedUp == 1 and cy < 160:
		global pressedUp
		pressedUp = 0
		pyautogui.keyUp("up")

	if pressedLeft == 1 and cx < 180:
		global pressedLeft
		pressedLeft = 0
		pyautogui.keyUp("Left")

	if pressedRight == 1 and cx > 140:
		global pressedRight
		pressedRight = 0
		pyautogui.keyUp("right")
	
	#pyautogui.keyUp("up")

def do_right(area):
    if area > 50000:
	pass
    else:
        pass


def main():
  
    try:
        while True:
            ret, frame = cap.read()
	    height, width, __ = frame.shape

            blurred = np.zeros((frame.shape[0], frame.shape[1]), np.uint8)
            # TODO: balans bieli
            cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY, blurred)
            cv2.blur(frame, (35, 35), blurred)
            __, blurred = cv2.threshold(blurred, 120, 210, cv2.THRESH_BINARY)

            cv2.imshow('Basic', frame)

	    frameright = frame[height_offset:height,0:width/2]
	    frameleft = frame[height_offset:height,width/2:width]

	    blurredright = blurred[height_offset:height,0:width/2]
	    blurredleft = blurred[height_offset:height,width/2:width]

            find_contours(frame, blurredright, frameright, left=False)
	    find_contours(frame, blurredleft, frameleft, left=True)
	
            # hull = cv2.convexHull(biggest_contour, returnPoints=False)
            # defects = cv2.convexityDefects(biggest_contour, hull)

            # import ipdb; ipdb.set_trace()

            # print hsv[240, 320]
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        # When everything done, release the capture
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
