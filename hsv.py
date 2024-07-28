import cv2 as cv
import numpy as np

cap = cv.VideoCapture(0)

while (1):

    # Take each frame
    _, frame = cap.read()

    # Convert BGR to HSV
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    import cv2

    cap = cv2.VideoCapture(0)

    cv2.namedWindow('result')

    while True:
        ret, frame = cap.read()
        frame_copy = frame.copy()
        frame_copy = cv2.flip(frame, 1)

        frame_hsv = cv2.cvtColor(frame_copy, cv2.COLOR_BGR2HSV)

        frame_h = frame_hsv[:, :, 0]
        frame_s = frame_hsv[:, :, 1]
        frame_v = frame_hsv[:, :, 2]
        #hsv(27, 28 %, 73 %)

        min_ = (65, 0, 0)
        max_ = (96, 255, 255)

        mask = cv2.inRange(frame_hsv, min_, max_)

        result = cv2.bitwise_and(frame_copy, frame_copy, mask=mask)

        cv2.imshow('mask', mask)
        cv2.imshow('result', result)
        cv2.imshow('or', frame_copy)

        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()