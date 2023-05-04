"""
This module handles the global frame of the SET game and SET-finding.
"""
import cv2 as cv
import numpy as np
from card import Card


class Image:
    """
    This class holds the SET board, detects, and keeps track of the cards that
    are in it.
    """
    def __init__(self, img):
        """
        Initialize a new Image instance using a full board image.

        Args:
            img: a full board image of a SET game
        """
        self.image = img
        self.contours = []
        self.simple_contours = []
        self.cards = []
        self.sets = []
        self.cards_in_sets = set()

    def _find_card_contours(self):
        """
        Find all the contours in the image for potential cards using grayscale
        and thresholding.
        """
        imgray = cv.cvtColor(self.image, cv.COLOR_BGR2GRAY)
        cv.adaptiveThreshold(
            imgray,
            255,
            cv.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv.THRESH_BINARY,
            99,
            2,
            imgray,
        )
        cv.adaptiveThreshold(
            imgray,
            255,
            cv.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv.THRESH_BINARY,
            9,
            2,
            imgray,
        )
        self.contours, _ = cv.findContours(
            imgray, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE
        )

    def _filter_contours_by_area(self):
        """
        Filter the detected contours by area to eliminate ones that are too
        large and too small.

        A contour that is greater than 1/12 of the image area is too large and
        a contour that is smaller that 1/10 of the largest potential contour is
        too small.
        """
        height, width, _ = self.image.shape
        area = []
        for cnt in self.contours:
            area.append(cv.contourArea(cnt))
        area.sort(reverse=True)
        minimum = -1
        maximum = -1
        for index, current_area in enumerate(area):
            if index > 30:
                break
            if current_area >= (height * width) / 12:
                maximum = index
            if area[maximum + 1] / current_area < 10:
                minimum = index + 1
        if maximum == -1:
            max_area = height * width
        else:
            max_area = area[maximum]
        if minimum == len(area):
            min_area = 0
        else:
            min_area = area[minimum]
        self.contours = [
            cnt
            for cnt in self.contours
            if (min_area < cv.contourArea(cnt) < max_area)
        ]

    def _filter_by_polygon(self):
        """
        Filter the contours by the ones that have four sides and are convex and
        save the contour as a simplified four-point representation.
        """
        for cnt in self.contours:
            approx = cv.approxPolyDP(cnt, 0.03 * cv.arcLength(cnt, True), True)
            if len(approx) == 4 and cv.isContourConvex(approx):
                self.simple_contours.append(approx)

    def _warp_perspective(self, card_contour):
        """
        Warp the perspective of the card to eliminate the effects of perspective
        in the original image and attempt to rotate the card horizontally.

        Args:
            card_contour: the simplified four-point contour of the detected card

        Returns:
            An image of the card cropped and perspective-corrected.
        """
        # pylint: disable=unsubscriptable-object
        approx = np.float32([[item[0][0], item[0][1]] for item in card_contour])
        cardh = int(np.linalg.norm(approx[1] - approx[0]))
        cardw = int(np.linalg.norm(approx[2] - approx[1]))
        transform = np.float32([[0, 0], [0, cardh], [cardw, cardh], [cardw, 0]])
        matrix = cv.getPerspectiveTransform(approx, transform)
        result = cv.warpPerspective(self.image, matrix, (cardw, cardh))
        card = self._rotate_card(cardw, cardh, result)
        return card

    def _rotate_card(self, cardw, cardh, card):
        """
        Rotate a card if it is sideways.

        This method works a majority of the time, excepting highly-skewed
        perspective scenarios.

        Args:
            cardw: width of the card in pixels
            cardh: height of the card in pixels
            card: image of the card before rotation

        Returns:
            A rotated version of the card if it is sideways; otherwise, returns
            the non-rotated card.
        """
        if cardh > cardw:
            return np.rot90(card)
        return card

    def create_cards(self):
        """
        Creates all detected Card instances after performing contour detection,
        filtering, and perspective correction.
        """
        self._find_card_contours()
        self._filter_contours_by_area()
        self._filter_by_polygon()
        for card_contour in self.simple_contours:
            self.cards.append(
                Card(self._warp_perspective(card_contour), card_contour)
            )

    def find_sets(self):
        """
        Find all SETs among the detected cards after filtering duplicates
        through brute force and then add them to a list.
        """
        self._deduplicate_cards()
        for index1, card1 in enumerate(self.cards):
            for index2, card2 in enumerate(self.cards):
                for index3, card3 in enumerate(self.cards):
                    if (
                        index1 != index2
                        and index1 != index3
                        and index2 != index3
                        and self._is_set(card1, card2, card3)
                    ):
                        found_set = {card1, card2, card3}
                        if found_set not in self.sets:
                            self.sets.append(found_set)
                            self.cards_in_sets.add(index1)
                            self.cards_in_sets.add(index2)
                            self.cards_in_sets.add(index3)

    def _deduplicate_cards(self):
        """
        Remove the duplicate cards detected based on equal comparative
        representations.
        """
        comparative = set()
        duplicates = []
        for index, card in enumerate(self.cards):
            if card.comparative in comparative:
                duplicates.append(index)
            comparative.add(card.comparative)
        for index in sorted(duplicates, reverse=True):
            del self.cards[index]

    def _is_set(self, card1, card2, card3):
        """
        Compare three cards to detect if they form a SET.

        The binary comparatives are compared logically as follows:
        NOT (A XOR B XOR C XOR NOT (A OR B OR C))

        Args:
            card1: the first card to be compared
            card2: the second card to be compared
            card3: the third card to be compared

        Returns:
            A boolean representing if the three cards form a SET.
        """
        return 0b000000000000 == ~(
            card1.comparative
            ^ card2.comparative
            ^ card3.comparative
            ^ ~(card1.comparative | card2.comparative | card3.comparative)
        )

    def get_cards_nonset(self):
        """
        Returns the cards that are not in any SETs.
        """
        return [
            card
            for index, card in enumerate(self.cards)
            if index not in self.cards_in_sets
        ]

    def get_cards_set(self):
        """
        Returns a list of 3-card sets representing the SETs discovered.
        """
        return self.sets
