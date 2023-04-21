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
        for cnt in self.contours:
            if not (
                area[minumum] + 1 < cv.contourArea(cnt) < area[maximum] - 1
            ):
                self.contours.remove(cnt)

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
        pass

    def _deduplicate_cards(self, cards):
        pass

    def _is_set(self, card1, card2, card3):
        pass

    def get_cards_nonset(self):
        pass

    def get_cards_set(self):
        pass
