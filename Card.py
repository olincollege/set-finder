import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
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
        self._find_number()
        self._find_shape()
        self._find_color()
        self._find_fill()

        edgecountavg = edgecountavg / counter

        # if edgecountavg < 5:
        #     self._shape = "diamond"
        # elif edgecountavg < 8:
        #     self._shape = "oval"
        # else:
        #     self._shape = "squiggle"
        # print(self._shape)

        # self._number = math.ceil(counter / 2)

        # print(self._number)

    def _find_fill(self):
        im = self._im
        im = cv.resize(im, (250, 120))
        im2 = im.copy()
        im = cv.convertScaleAbs(im, alpha=1.5)
        while (
            im2[10][10][0] != 255
            or im2[10][10][1] != 255
            or im2[10][10][2] != 255
        ):
            im2 = cv.convertScaleAbs(im2, alpha=1.01)
        cropped_image = im[10:110, 20:230]
        cropped_image2 = im2[10:110, 20:230]
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
        contours, hierarchy = cv.findContours(
            thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE
        )
        mask = np.zeros(cropped_image2.shape)
        cv.drawContours(mask, contours, 0, (255, 0, 0), -1)
        erosion_size = 8
        element = cv.getStructuringElement(
            cv.MORPH_ELLIPSE,
            (2 * erosion_size + 1, 2 * erosion_size + 1),
            (erosion_size, erosion_size),
        )
        erosion_dst = np.uint8(cv.erode(mask, element))
        erosion_dst = cv.cvtColor(erosion_dst, cv.COLOR_BGR2GRAY)
        # cropped_image = np.uint8(cropped_image)
        # print(np.uint8(cropped_image).shape)
        # print(np.uint8(erosion_dst).shape)
        # cv.threshold(erosion_dst, 127, 255, cv.THRESH_BINARY, erosion_dst)
        cropped_image2 = cv.bitwise_and(
            cropped_image2,
            cropped_image2,
            mask=erosion_dst,
        )
        # fig = plt.figure()
        # plt.imshow(cv.cvtColor(cropped_image2, cv.COLOR_BGR2RGB))
        # plt.imshow(cv.cvtColor(self._im, cv.COLOR_BGR2RGB))
        cropped_image2 = cv.cvtColor(cropped_image2, cv.COLOR_BGR2GRAY)
        counter = 0
        sum = 0
        for row in cropped_image2:
            for pixel in row:
                if 1 < pixel < 250:
                    sum += pixel
                    counter += 1
        if counter == 0:
            avg = 0
        else:
            avg = sum / counter
        # print(avg)
        if avg > 240 or avg == 0:
            self._fill = "gas"
        elif avg < 180:
            self._fill = "solid"
        else:
            self._fill = "liquid"

    def _find_shape(self):
        im = self._im
        im = cv.resize(im, (250, 120))
        im = cv.convertScaleAbs(im, alpha=1.5)
        cropped_image = im[10:110, 20:230]
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
        contours, hierarchy = cv.findContours(
            thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE
        )
        for cnt in contours:
            approx = cv.approxPolyDP(cnt, 0.025 * cv.arcLength(cnt, True), True)
            # print(f"{len(approx)},{cv.isContourConvex(approx)}")
            if len(approx) == 4:
                self._shape = "diamond"
            else:
                if cv.isContourConvex(approx):
                    self._shape = "oval"
                else:
                    self._shape = "squiggle"
            self._area = cv.contourArea(cnt)
        # cv.drawContours(cropped_image, contours, -1, (255, 0, 0), 1)
        # # print(len(contours))
        # fig = plt.figure()
        # plt.imshow(cropped_image)

    def _find_number(self):
        im = self._im
        im = cv.resize(im, (250, 120))
        im = cv.convertScaleAbs(im, alpha=1.5)
        cropped_image = im[10:110, 20:230]
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
        contours, hierarchy = cv.findContours(
            thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE
        )
        # cv.drawContours(cropped_image, contours, -1, (255, 0, 0), 1)
        # print(len(contours))
        # fig = plt.figure()
        # plt.imshow(cropped_image)
        self._number = len(contours)

    def _find_color(self):
        im = self._im
        im = cv.resize(im, (250, 120))
        im = cv.convertScaleAbs(im, alpha=1.5)
        cropped_image = im[10:110, 20:230]
        hsv = cv.cvtColor(cropped_image, cv.COLOR_BGR2HSV)

        # fig = plt.figure()
        # plt.imshow(cv.cvtColor(hsv, cv.COLOR_HSV2RGB))

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
