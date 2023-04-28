"""
Module to contain user display functions.
"""
import cv2
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from Card import Card
from Image import Image
from Controller import Controller
import random


class View:
    """
    Class for displaying Set boards.

    Attributes:
        image: A cv2.Mat type image showing the full board
    """

    def __init__(self, image):
        self.image = image
        self._drawn_cards = []
        self._controller = Controller(4)
        self.fig = plt.figure()
        self._imag = plt.imshow(cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB))
        self.axes = plt.axes([0.81, 0.000001, 0.1, 0.075])
        self.bnext = Button(self.axes, "New")
        self.bnext.on_clicked(self.new_image)

    def draw_nonset_cards(self, list_cards):
        """
        Draws cards on the image in black.

        Args:
            list_cards: A list of Card objects representing the nonset cards.
        """
        for card in list_cards:
            self._draw_rectangle(card, (255, 255, 255),3)

    def draw_set_cards(self, list_cards):
        """
        Draws cards on the image in green.

        Args:
            list_cards: A list of list of Card objects representing the set cards.
        """
        i = 20
        for set in list_cards:
            color = (
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255),
            )
            for card in set:
                self._draw_rectangle(card, color,i)
            i = i // 2

    def _draw_rectangle(self, card: Card, color,radius):
        """
        Draws a contour on the image.

        Args:
            card: A Card object.
            color: A tuple of the color to draw the rectangle.
        """
        cv2.drawContours(self.image, [card.contour], 0, color, radius)

    def new_image(self,_):
        """'
        Run program again to capture image.
        """
        self.image = self._controller.get_image()
        


    def show(self):
        """
        Display board state to the user.
        """
        self.fig = plt.figure()
        self._imag = plt.imshow(cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB))
        self.axes = plt.axes([0.81, 0.000001, 0.1, 0.075])
        self.bnext = Button(self.axes, "New")
        self.bnext.on_clicked(self.new_image)
        alpha = 3.0 # Contrast control (1.0-3.0)
        beta = 0 # Brightness control (0-100)
        
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
        plt.show()


if __name__ == "__main__":
    # Code to check if view is working
    view = View(cv2.imread("boards/1.jpg"))
    view.show()