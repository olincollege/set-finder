"""
Module to contain user display functions.
"""
import cv2
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from Card import Card
from Image import Image
from Controller import Controller
import random


class View:
    """
    Class for displaying SET boards.

    Attributes:
        image: A cv2.Mat type image showing the full board
    """

    def __init__(self, image):
        self.image = image
        self._drawn_cards = []
        self._controller = Controller(0)
        self.fig = plt.figure()
        self._imag = plt.imshow(cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB))
        self.axes = plt.axes([0.81, 0.000001, 0.1, 0.075])
        self.bnext = Button(self.axes, "New")
        self.bnext.on_clicked(self.new_image)

    def draw_nonset_cards(self, list_cards):
        """
        Draws cards on the image in black.

        Args:
            list_cards: A list of Card objects representing the non-SET cards.
        """
        for card in list_cards:
            self._draw_rectangle(card, (255, 255, 255), 3)

    def draw_set_cards(self, list_cards):
        """
        Draws cards on the image in green.

        Args:
            list_cards: A list of list of Card objects representing the SET
            cards.
        """
        card_counter = {}
        for set in list_cards:
            color = (
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255),
            )
            for card in set:
                self._draw_rectangle(card, color, card_counter.get(card, 0))
                card_counter[card] = card_counter.get(card, 0) + 1

    def _draw_rectangle(self, card: Card, color, ring_count):
        """
        Draws a contour on the image, offset to not overlap other contours.

        Args:
            card: A Card object.
            color: A tuple of the color to draw the rectangle.
        """
        contour_scale = (
            (size := self.image.shape)[0] * size[1]
        ) / cv2.contourArea(card.contour)
        thickness = int(math.sqrt(size[0] * size[1]) / 50)
        dilation_factor = 0.1 * ring_count * contour_scale / 30
        x_com, y_com = np.average(card.contour, axis=0)[0]
        trans = np.array([[1, 0, -x_com], [0, 1, -y_com], [0, 0, 1]])
        untrans = np.array([[1, 0, x_com], [0, 1, y_com], [0, 0, 1]])
        dilate = np.array(
            [
                [1 + dilation_factor, 0, 1],
                [0, 1 + dilation_factor, 1],
                [0, 0, 1],
            ]
        )
        contour = np.r_[
            np.transpose(np.reshape(np.array(card.contour), (4, 2), order="C")),
            [[1, 1, 1, 1]],
        ]
        translated = np.matmul(trans, contour)
        dilated = np.matmul(dilate, translated)
        reverse_trans = np.matmul(untrans, dilated)
        reshaped = np.reshape(
            np.transpose(np.delete(reverse_trans, 2, axis=0)),
            (4, 1, 2),
            order="C",
        ).astype(int)
        cv2.drawContours(self.image, [reshaped], 0, color, thickness)

    def new_image(self, _):
        """'
        Run program again to capture image.
        """
        self.image = self._controller.get_image()
        alpha = 3.0  # Contrast control (1.0-3.0)
        beta = 0  # Brightness control (0-100)

        manual_result = cv2.convertScaleAbs(self.image, alpha=alpha, beta=beta)
        print("Processing...")
        im = Image(manual_result)
        print("finding cards")
        im.create_cards()
        print("finding sets")
        im.find_sets()
        # print(im.get_cards_nonset())
        print("drawing cards")
        # self.draw_nonset_cards(im.get_cards_nonset())
        self.draw_set_cards(im.get_cards_set())
        # print(im.get_cards_set())
        self._imag.set_data(cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB))
        print("Done")
        plt.draw()

    def show(self):
        """
        Display board state to the user.
        """
        plt.show()


if __name__ == "__main__":
    # Code to check if view is working
    view = View(cv2.imread("boards/1.jpg"))
    view.show()
