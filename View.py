import cv2
import numpy as np
from tkinter import *
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.widgets import Button


class View:
    def __init__(self, image):
        self.image = image

    def draw_nonset_cards(list_cards):
        pass

    def draw_set_cards(list_cards):
        pass

    def _draw_rectangle(card, color):
        """
        Draws a rectangle on the image

        Args:
            card: A Card object
            color: A tuple of the color to draw the rectangle
        """
        # Extract coordinates from card object
        # push int to array of points
        pts = np.array([[10, 5], [20, 30], [70, 20], [50, 10]], np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(self.image, [pts], True, color)

    def new_image(*args):
        print("test")

    def show(self):
        fig = plt.figure()
        plt.imshow(self.image)
        axes = plt.axes([0.81, 0.000001, 0.1, 0.075])
        bnext = Button(axes, "Add", color="yellow")
        bnext.on_clicked(self.new_image)
        plt.show()


if __name__ == "__main__":
    # test code
    img = cv2.imread("boards/1.jpg")
    view = View(img)
    view.show()
