import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
import random
import math


class Card:
    def __init__(self, card_img, contour):
        self._im = card_img
        self._contour = contour
        self._color = ""
        self._shape = ""
        self._number = 0
        self._fill = ""
        self.classify()
        self._create_comparative()

    @property
    def contour(self):
        return self._contour

    @property
    def comparative(self):
        return self._comparative

    def classify(self):
        im = self._im
        scale=0.75
        dimensions=(250*scale,120*scale,10*scale,20*scale,110*scale,230*scale)
        dimensions=tuple(int(dimension) for dimension in dimensions)
        im = cv.resize(im, (dimensions[0], dimensions[1]))
        im2 = im.copy()
        while (
            im2[dimensions[2]][dimensions[3]][0] != 255
            or im2[dimensions[2]][dimensions[3]][1] != 255
            or im2[dimensions[2]][dimensions[3]][2] != 255
            or im2[dimensions[4]][dimensions[5]][0] != 255
            or im2[dimensions[4]][dimensions[5]][1] != 255
            or im2[dimensions[4]][dimensions[5]][2] != 255
        ):
            im2 = cv.convertScaleAbs(im2, alpha=1.05)
        im = cv.convertScaleAbs(im2, alpha=1.3)
        cropped_image = im[dimensions[2]:dimensions[4], dimensions[3]:dimensions[5]]
        cropped_image2 = im2[dimensions[2]:dimensions[4], dimensions[3]:dimensions[5]]
        thresh = cv.cvtColor(cropped_image.copy(), cv.COLOR_BGR2GRAY)
        cv.adaptiveThreshold(
            thresh,
            255,
            cv.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv.THRESH_BINARY,
            101,
            2,
            thresh,
        )
        cv.threshold(thresh, 127, 255, cv.THRESH_BINARY_INV, thresh)
        contours, _ = cv.findContours(
            thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE
        )

        self._find_number(contours)

        self._find_color(cropped_image)

        fills=[]
        shapes=[]
        for contour in contours:
            fills.append(self._find_fill(cropped_image2, contour))
            shapes.append(self._find_shape(contour))
        if not fills:
            fills=[""]
        if not shapes:
            shapes=[""]
        self._shape=Counter(shapes).most_common(1)[0][0]
        self._fill=Counter(fills).most_common(1)[0][0]
        

    def _find_fill(self, cropped_image2, contours):
        mask = np.zeros(cropped_image2.shape)
        cv.drawContours(mask, [contours], 0, (255, 0, 0), -1)
        erosion_size = 8
        element = cv.getStructuringElement(
            cv.MORPH_ELLIPSE,
            (2 * erosion_size + 1, 2 * erosion_size + 1),
            (erosion_size, erosion_size),
        )
        erosion_dst = np.uint8(cv.erode(mask, element))
        erosion_dst = cv.cvtColor(erosion_dst, cv.COLOR_BGR2GRAY)
        cropped_image2 = cv.bitwise_and(
            cropped_image2,
            cropped_image2,
            mask=erosion_dst,
        )
        cropped_image2 = cv.cvtColor(cropped_image2, cv.COLOR_BGR2GRAY)
        counter = 0
        sum = 0
        for row in cropped_image2:
            for pixel in row:
                if 1 < pixel < 254:
                    sum += pixel
                    counter += 1
        if counter == 0:
            avg = 0
        else:
            avg = sum / counter
        if counter<cv.contourArea(contours)/100 or avg == 0:
            return "gas"
        elif avg < 160:
            return "solid"
        else:
            return "liquid"

    def _find_shape(self, contour):
        approx = cv.approxPolyDP(contour, 0.025 * cv.arcLength(contour, True), True)
        if len(approx) == 4:
            return "diamond"
        else:
            if cv.isContourConvex(approx):
                return "oval"
            else:
                return "squiggle"

    def _find_number(self, contours):
        self._number = len(contours)

    def _find_color(self, cropped_image):
        hsv = cv.cvtColor(cropped_image, cv.COLOR_BGR2HSV)
        r = 0
        p = 0
        g = 0
        for row in hsv:
            for pixel in row:
                if pixel[1] > 10:
                    h = pixel[0]
                    if (20 > h > 0) or (170 < h < 179):
                        r += 1
                    elif 40 < h < 80:
                        g += 1
                    elif 130 < h < 160:
                        p += 1
        if r > g and r > p:
            self._color = "red"
        elif g > p:
            self._color = "green"
        else:
            self._color = "purple"

    def _create_comparative(self):
        color = 0
        color += self._color == "red"
        color += 2 * (self._color == "green")
        color += 4 * (self._color == "purple")

        number = 0
        number += self._number == 1
        number += 2 * (self._number == 2)
        number += 4 * (self._number == 3)

        shape = 0
        shape += self._shape == "oval"
        shape += 2 * (self._shape == "squiggle")
        shape += 4 * (self._shape == "diamond")

        fill = 0
        fill += self._fill == "solid"
        fill += 2 * (self._fill == "liquid")
        fill += 4 * (self._fill == "gas")

        self._comparative = color + 8 * number + 64 * shape + 512 * fill
