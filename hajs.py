__author__ = 'plizonczyk'

import cv2
import imutils
import numpy as np

#
# hog = cv2.HOGDescriptor()
# hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
#
#
# def detect_human(frame):
#     found = hog.detectMultiScale(frame)
#     out = np.zeros(frame.shape, np.uint8)
#     np.copyto(out, frame)
#     for finding in found:
#         if len(finding) == 0 or len(finding[0]) != 4:
#             continue
#         data = finding[0]
#         pt1 = int(data[0]), int(data[1])
#         pt2 = int(data[2]), int(data[3])
#         # import ipdb; ipdb.set_trace()
#         cv2.rectangle(out, pt1, pt2, (0, 255, 0), 5)
#         # cv2.rectangle(out, (50, 50), (250, 250), (0, 255, 0), 5)
#     cv2.imshow('hummies', out)
#     return found
#
#
# hand_cascade = cv2.CascadeClassifier('hand_cascade2.xml')
#
# def detect_hand(frame):
#     found = hog.detectMultiScale(frame)
#     out = np.zeros(frame.shape, np.uint8)
#     np.copyto(out, frame)
#     for finding in found:
#         if len(finding) == 0 or len(finding[0]) != 4:
#             continue
#         data = finding[0]
#         pt1 = int(data[0]), int(data[2])
#         pt2 = int(data[1]), int(data[3])
#         print pt1, pt2
#         # import ipdb; ipdb.set_trace()
#         cv2.rectangle(out, pt1, pt2, (0, 255, 0), 5)
#         # cv2.rectangle(out, (50, 50), (250, 250), (0, 255, 0), 5)
#     cv2.imshow('hummies', out)
#     return found

def main():
    cap = cv2.VideoCapture(0)

    try:
        while True:
            ret, frame = cap.read()

            blurred = np.zeros((frame.shape[0], frame.shape[1]), np.uint8)
            # TODO: balans bieli
            cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY, blurred)
            cv2.blur(frame, (35, 35), blurred)
            __, blurred = cv2.threshold(blurred, 120, 210, cv2.THRESH_BINARY)

            cv2.imshow('Basic', frame)

            try:
                __, contours, __ = cv2.findContours(blurred, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
            except ValueError:
                contours, __ = cv2.findContours(blurred, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
            cv2.drawContours(frame, contours, -1, (255, 0, 0), 3)

            max_area = 0
            biggest_contour = None

            for contour in contours:
                area = cv2.contourArea(contour)
                if area > max_area:
                    max_area = area
                    biggest_contour = contour

            x, y, w, h = cv2.boundingRect(biggest_contour)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0))
            cv2.imshow('Rectanble', frame)

            hull = cv2.convexHull(biggest_contour, returnPoints=False)
            defects = cv2.convexityDefects(biggest_contour, hull)

            import ipdb; ipdb.set_trace()

            # print hsv[240, 320]
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        # When everything done, release the capture
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()