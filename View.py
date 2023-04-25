"""
Module to contain user display functions.
"""
import cv2
from tkinter import *
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from Card import Card

class View:
    """
    Class for displaying Set boards.

    Attributes:
        image: A cv2.Mat type image showing the 
    """
    def __init__(self, image):
        self.image = image

    def draw_nonset_cards(self,list_cards):
        """
        Draws cards on the image in black.

        Args:
            list_cards: A list of Card objects representing the nonset cards.
        """
        for card in list_cards:
            self._draw_rectangle(card,(255,255,255))

    def draw_set_cards(self,list_cards):
        """
        Draws cards on the image in green.

        Args:
            list_cards: A list of Card objects representing the set cards.
        """
        for card in list_cards:
            self._draw_rectangle(card,(0,255,0))

    def _draw_rectangle(self,card: Card, color):
        """
        Draws a rectangle on the image.

        Args:
            card: A Card object.
            color: A tuple of the color to draw the rectangle.
        """
        # Extract coordinates from card object
        # push int to array of points
        pts = card.contour()
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(self.image, [pts], True, color)

    def new_image():
        """'
        Run program again to capture image.
        """
        print("test")

    def show(self):
        """
        Display board state to the user.
        """
        fig = plt.figure()
        plt.imshow(self.image)
        axes = plt.axes([0.81, 0.000001, 0.1, 0.075])
        bnext = Button(axes, "New")
        bnext.on_clicked(self.new_image)
        plt.show()


if __name__ == "__main__":
    # Code to check if view is working
    img = cv2.imread("boards/1.jpg")
    view = View(img)
    view.show()
