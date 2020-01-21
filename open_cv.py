import cv2
import numpy as np
import math
from constants import *

# code based on:
# https://github.com/aquibjaved/Multiple-Color-Tracking-using-opencv-and-python-in-Real-Time/blob/master/color.py


class OpenCV:
    def __init__(self):
        self.row = 0
        self.col = 0
        self.stonesAt = np.zeros((ROWS, COLUMNS))
        self.cap = cv2.VideoCapture(0)

    # capturing video through webcam

    def capture(self):

        _, img2 = self.cap.read()

        SCREEN_HEIGHT = ROWS * 100
        SCREEN_WIDTH = COLUMNS * 100
        img = cv2.resize(img2, (SCREEN_WIDTH, SCREEN_HEIGHT))

        xx = 0
        yy = 0
        # draw the grid
        while xx < SCREEN_WIDTH:
            cv2.line(img, (xx, 0), (xx, SCREEN_HEIGHT), color=(0, 255, 0), lineType=cv2.LINE_AA, thickness=1)
            xx += 100

        while yy < SCREEN_HEIGHT:
            cv2.line(img, (0, yy), (SCREEN_WIDTH, yy), color=(0, 255, 0), lineType=cv2.LINE_AA, thickness=1)
            yy += 100

        # converting to HSV (hue-saturation-value)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # defining the range of red color
        red_lower = np.array([160, 150, 111], np.uint8)
        red_upper = np.array([180, 255, 255], np.uint8)

        # finding the range of red in the image
        red = cv2.inRange(hsv, red_lower, red_upper)

        # Morphological transformation, Dilation
        kernal = np.ones((5, 5), "uint8")
        red = cv2.dilate(red, kernal)

        # Tracking the Red Color
        (contours, hierarchy) = cv2.findContours(red, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if (area > 300):
                x, y, w, h = cv2.boundingRect(contour)
                img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)

                # mapping the size of the screen to the amount of rows and columns and give the position
                # of the red object
                self.row = math.ceil(self.map(y + 0.5 * h, 1, SCREEN_HEIGHT, 6, 0))
                self.col = math.ceil(self.map(x + 0.5 * w, 1, SCREEN_WIDTH, 0, 7))

                cv2.putText(img, "row:" + str(self.row) + ",column:" + str(self.col), (x, y), cv2.FONT_HERSHEY_SIMPLEX,
                            0.7,
                            (0, 0, 255))

        # print(stonesAt)
        cv2.imshow("Color Tracking", img)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            self.cap.release()
            cv2.destroyAllWindows()

    def get_new_stone(self):
        # if stone/ red object is detected (after button pressed), return column
        return self.col - 1

    def map(self, value, value_min, value_max, scale_min, scale_max):  # function to map/scale (here: screen size )
        # getting the length of the range
        value_range = value_max - value_min
        scale_range = scale_max - scale_min

        # scaling the value by the scaling factor
        scaled_value = float(value - value_min) / float(value_range)

        return scale_min + (scaled_value * scale_range)
