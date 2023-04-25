import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import random
import math


class Card:
    def __init__(self, card_img, contour):
        self._im = card_img
        self._contour = contour
        self.classify()

    @property
    def contour(self):
        return self._contour

    def classify(self):
        im = self._im
        height, width, _ = im.shape
        im = cv.resize(im, (250, 120))

        # hsv = cv.cvtColor(im, cv.COLOR_BGR2HSV)
        # greenMask = cv.inRange(hsv, (26, 10, 30), (97, 100, 255))

        # hsv[:,:,1] = greenMask

        # back = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        im = cv.convertScaleAbs(im, alpha=1.5)

        wpad = int(width / 50)
        hpad = int(height / 50)
        cropped_image = im[hpad : height - hpad, wpad : width - wpad]
        thresh = cv.cvtColor(cropped_image.copy(), cv.COLOR_BGR2GRAY)
        # cv.threshold(cropped_image,63,255,cv.THRESH_BINARY,thresh)
        # thresh=cv.bitwise_not(thresh)
        cv.adaptiveThreshold(
            thresh,
            255,
            cv.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv.THRESH_BINARY,
            9,
            2,
            thresh,
        )
        contours, hierarchy = cv.findContours(
            thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE
        )
        area = []
        for cnt in contours:
            area.append(cv.contourArea(cnt))
        area.sort(reverse=True)

        edgecountavg = 0
        counter = 0
        for idx, cnt in enumerate(contours):
            curarea = cv.contourArea(cnt)
            if 1000 < curarea < width * height / 4:
                approx = cv.approxPolyDP(
                    cnt, 0.025 * cv.arcLength(cnt, True), True
                )
                edgecountavg += len(approx)
                # print(cv.isContourConvex(approx))
                # x, y, w, h = cv.boundingRect(
                #     cnt
                # )  # offsets - with this you get 'mask'
                # cv.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 2)
                # # cv2.imshow('cutted contour',img[y:y+h,x:x+w])
                # print(
                #     "Average color (BGR): ",
                #     np.array(cv.mean(im[y : y + h, x : x + w])).astype(
                #         np.uint8
                #     ),
                # )
                # cv.drawContours(im, contours, idx, (255, 0, 0), 1)
                counter += 1

        # plt.imshow(cv.cvtColor(im, cv.COLOR_BGR2RGB))
        self._find_color()

        edgecountavg = edgecountavg / counter

        if edgecountavg < 5:
            print(f"Diamond {edgecountavg}")
        elif edgecountavg < 8:
            print(f"Circle {edgecountavg}")
        else:
            print(f"Squiggle {edgecountavg}")

        print(f"{math.ceil(counter/2)} Symbols")
        print("------------------------")

    def _find_color(self):
        # hsv = cv.cvtColor(self._im, cv.COLOR_BGR2HSV)
        # hsv = cv.convertScaleAbs(hsv, alpha=1.5)

        background_color = self._im[30][30][0]
        # print(background_color)
        avg_color_per_row = np.average(self._im, axis=0)
        avg_color = np.average(avg_color_per_row, axis=0)[0] - background_color

        index = np.argmax(avg_color)

        if index == 2:
            print(f"Red {index}")
        elif index == 1:
            print(f"Green {index}")
        elif index == 0:
            print(f"Blue {index}")
