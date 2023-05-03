"""
This module handles the attributes of a particular card.

Attributes:
    contour: location of the card within the original image's reference frame
    comparative: binary comparison values for determining if three cards form a
        set
"""
from cv2 import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter


class Card:
    def __init__(self, card_img, contour):
        """
        Initialize a new card object using a cropped card image and a contour.

        Args:
            card_img: a card image that is cropped and warped to be rectangular,
                counteracting the effects of perspective
            contour: a numpy array of points in the contour format of OpenCV
                that represents the card's bounds within the external reference
                frame
        """
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
        """
        Return a numpy array of points in the contour format of OpenCV that
        represents the card's bounds within the external reference frame.
        """
        return self._contour

    @property
    def comparative(self):
        """
        Return an integer with the binary representation of this card's
        attributes, as generated by _create_comparative().
        """
        return self._comparative

    def classify(self):
        """
        Pre-process a card image through scaling, contrast, cropping,
        thresholding, and contour detection. Then, find the card's attributes,
        accounting for variability across detected contours.
        """
        im = self._im
        scale = 0.75
        size = (250, 120)
        margins = (20, 10)
        dimensions = (
            size[0] * scale,
            size[1] * scale,
            margins[1] * scale,
            margins[0] * scale,
            (size[1] - margins[1]) * scale,
            (size[0] - margins[0]) * scale,
        )
        dimensions = tuple(int(dimension) for dimension in dimensions)
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
        cropped_image = im[
            dimensions[2] : dimensions[4], dimensions[3] : dimensions[5]
        ]
        cropped_image2 = im2[
            dimensions[2] : dimensions[4], dimensions[3] : dimensions[5]
        ]
        thresh = cv.cvtColor(cropped_image.copy(), cv.COLOR_BGR2GRAY)
        cv.adaptiveThreshold(
            thresh,
            255,
            cv.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv.THRESH_BINARY,
            301,
            2,
            thresh,
        )
        cv.threshold(thresh, 127, 255, cv.THRESH_BINARY_INV, thresh)
        contours, _ = cv.findContours(
            thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE
        )
        # areas = [cv.contourArea(cnt) for cnt in contours]
        # contours = [cnt for _, cnt in sorted(zip(areas, contours))]
        # contours.reverse()
        # contours=contours[:3]

        self._find_number(contours)

        self._find_color(cropped_image)

        fills = []
        shapes = []
        for contour in contours:
            fills.append(self._find_fill(cropped_image2, contour))
            shapes.append(self._find_shape(contour))
        if not fills:
            fills = [""]
        if not shapes:
            shapes = [""]
        self._shape = Counter(shapes).most_common(1)[0][0]
        self._fill = Counter(fills).most_common(1)[0][0]

    def _find_fill(self, processed_image, contour):
        """
        Detect the fill of a card using an eroded contour mask and pixel
        brightness averaging.

        Args:
            processed_image: the pre-processed image of the card with medium
                contrast
            contour: one of the detected image contours

        Returns:
            The calculated fill of the card on the scale of solid, liquid, and
            gas (solid fill, partial fill, no fill).
        """
        mask = np.zeros(processed_image.shape)
        cv.drawContours(mask, [contour], 0, (255, 0, 0), -1)
        erosion_size = 8
        element = cv.getStructuringElement(
            cv.MORPH_ELLIPSE,
            (2 * erosion_size + 1, 2 * erosion_size + 1),
            (erosion_size, erosion_size),
        )
        erosion_dst = np.uint8(cv.erode(mask, element))
        erosion_dst = cv.cvtColor(erosion_dst, cv.COLOR_BGR2GRAY)
        processed_image = cv.bitwise_and(
            processed_image,
            processed_image,
            mask=erosion_dst,
        )
        processed_image = cv.cvtColor(processed_image, cv.COLOR_BGR2GRAY)
        counter = 0
        sum = 0
        for row in processed_image:
            for pixel in row:
                if 1 < pixel < 254:
                    sum += pixel
                    counter += 1
        if counter == 0:
            avg = 0
        else:
            avg = sum / counter
        if counter < cv.contourArea(contour) / 100 or avg == 0:
            return "gas"
        elif avg < 160:
            return "solid"
        else:
            return "liquid"

    def _find_shape(self, contour):
        """
        Detect the shape of a card using the number of sides and convexity of
        detected contours.

        Args:
            contour: one of the detected image contours

        Returns:
            The calculated shape of the card: diamond, oval, squiggle.
        """
        approx = cv.approxPolyDP(
            contour, 0.025 * cv.arcLength(contour, True), True
        )
        if len(approx) == 4:
            return "diamond"
        else:
            if cv.isContourConvex(approx):
                return "oval"
            else:
                return "squiggle"

    def _find_number(self, contours):
        """
        Detect the number of symbols on a card using the number of detected
        contours.

        Args:
            contours: the detected image contours
        """
        self._number = len(contours)

    def _find_color(self, processed_image):
        """
        Detect the color of a card using the HSV color-space and pixel values.
        The options are red, green, and purple.

        Args:
            processed_image: the pre-processed image of the card with high
                contrast
        """
        hsv = cv.cvtColor(processed_image, cv.COLOR_BGR2HSV)
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
        """
        Create the binary comparative for the card object using the calculated
        attributes.

        A binary representation is a 12-bit integer composed bitwise as follows:
            0: is it red?
            1: is it green?
            2: is it purple?
            3: is it a single symbol?
            4: is it a double symbol?
            5: is it a triple symbol?
            6: is it an oval?
            7: is it a squiggle?
            8: is it a diamond?
            9: is it solid fill?
            10: is it liquid fill?
            11: is it gas fill?
        """
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
