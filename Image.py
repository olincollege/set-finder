import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import random
import Card


class Image:
    def __init__(self, img):
        self.im = img
        self.simple_contours = []
        self.cards = []
        self.sets = []
        self.cards_in_sets = set()

    def _find_all_contours(self):
        imgray = cv.cvtColor(self.im, cv.COLOR_BGR2GRAY)
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
        height, width, _ = self.im.shape
        area = []
        for cnt in self.contours:
            area.append(cv.contourArea(cnt))
        area.sort(reverse=True)
        minumum = 0
        maximum = 0
        for index in range(len(area) - 1):
            if index > 30:
                break
            if area[index] >= (height * width) / 12:
                maximum = index
            if area[maximum + 1] / area[index] < 10:
                minumum = index
        self.contours = [
            cnt
            for cnt in self.contours
            if (area[minumum] + 1 < cv.contourArea(cnt) < area[maximum] - 1)
        ]

    def _filter_by_polygon(self):
        for cnt in self.contours:
            approx = cv.approxPolyDP(cnt, 0.03 * cv.arcLength(cnt, True), True)
            if len(approx) == 4 and cv.isContourConvex(approx):
                self.simple_contours.append(approx)

    # def _crop(self, board_image, contours):
    #     pass

    def _warp_perspective(self, card_contour):
        approx = np.float32([[item[0][0], item[0][1]] for item in card_contour])
        cardh = int(np.linalg.norm(approx[1] - approx[0]))
        cardw = int(np.linalg.norm(approx[2] - approx[1]))
        transform = np.float32([[0, 0], [0, cardh], [cardw, cardh], [cardw, 0]])
        matrix = cv.getPerspectiveTransform(approx, transform)
        result = cv.warpPerspective(self.im, matrix, (cardw, cardh))
        card = self._rotate_card(cardw, cardh, result)

    def _rotate_card(self, cardw, cardh, card):
        if cardh > cardw:
            return np.rot90(card)
        return card

    def create_cards(self):
        self._find_card_contours()
        self._filter_contours_by_area()
        self._filter_by_polygon()
        for card_contour in self.simple_contours:
            self.cards.append(Card(self._warp_perspective(card_contour)))

    def find_sets(self):
        for index1, card1 in enumerate(self.cards):
            for index2, card2 in enumerate(self.cards):
                for index3, card3 in enumerate(self.cards):
                    if (
                        index1 != index2
                        and index1 != index3
                        and index2 != index3
                        and self._is_set(card1, card2, card3)
                    ):
                        self.sets.append([card1, card2, card3])
                        self.cards_in_sets.add(index1)
                        self.cards_in_sets.add(index2)
                        self.cards_in_sets.add(index3)

    def _deduplicate_cards(self, cards):
        comparative = set()
        duplicates = []
        for index, card in enumerate(self.cards):
            if card.comparative() in comparative:
                duplicates.append(index)
            comparative.add(card.comparative())
        for index in sorted(duplicates, reverse=True):
            del self.cards[index]

    def _is_set(self, card1, card2, card3):
        return 0b000000000000 == ~(
            card1.comparative()
            ^ card2.comparative()
            ^ card3.comparative()
            ^ ~(card1.comparative() | card2.comparative() | card3.comparative())
        )

    def get_cards_nonset(self):
        return [
            card
            for index, card in enumerate(self.cards)
            if index not in self.cards_in_sets
        ]

    def get_cards_set(self):
        return self.sets
