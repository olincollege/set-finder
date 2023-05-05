"""
Module to read user input
"""
import math
import os
import cv2
import numpy as np
from image import Image


class Controller:
    """
    Class for reading webcam input
    """

    def __init__(self):
        """
        Instantiate the controller with a blank image
        """
        self.image = 255 * np.ones((1, 1, 3), dtype=np.uint8)

    def read_image(self, path):
        """
        Read the image from a file.

        Args:
            path: a string representing the filepath of the image.
        """
        if not os.path.exists(path):
            raise TypeError()
        self.image = cv2.imread(path)

    def get_image(self):
        """
        Return the image converted to the RGB colorspace and resized to fit the
        window
        """
        return self._correct_color(self._resized_image())

    def _resized_image(self):
        """
        Resize the image to fit in the window
        """
        factor = 640 / self.image.shape[0]
        dim = (int(self.image.shape[1] * factor), 640)
        return cv2.resize(self.image, dim, interpolation=cv2.INTER_AREA)

    def _correct_color(self, image):
        """
        Helper function to convert image color
        """
        return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    def draw_nonset_cards(self, list_cards):
        """
        Draws cards on the image in black.

        Args:
            list_cards: A list of Card objects representing the non-SET cards.
        """
        for card in list_cards:
            self._draw_rectangle(card, (255, 255, 255), 3)

    def draw_set_cards(self, sets):
        """
        Draws cards on the image in green.

        Args:
            list_cards: A list of list of Card objects representing the SET
            cards.
        """
        i = 1
        card_counter = {}
        for cards in sets:
            hsv_color = cv2.cvtColor(
                np.array(
                    [[[(30 * i + math.sqrt(10 * i)) % 179, 255, 255]]],
                    dtype=np.uint8,
                ),
                cv2.COLOR_HSV2BGR,
            )
            color = (
                int(hsv_color[0][0][0]),
                int(hsv_color[0][0][1]),
                int(hsv_color[0][0][2]),
            )
            i += 1
            for card in cards:
                self._draw_rectangle(card, color, card_counter.get(card, 0))
                card_counter[card] = card_counter.get(card, 0) + 1

    def _draw_rectangle(self, card, color, ring_count):
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
        contour = np.matmul(trans, contour)
        contour = np.matmul(dilate, contour)
        contour = np.matmul(untrans, contour)
        contour = np.reshape(
            np.transpose(np.delete(contour, 2, axis=0)),
            (4, 1, 2),
            order="C",
        ).astype(int)
        cv2.drawContours(self.image, [contour], 0, color, thickness)

    def generate_image_overlay(self):
        """
        Generate the SET detection overlay for the GUI.
        """
        print("Processing...")
        image = Image(self.image)
        print("finding cards")
        image.create_cards()
        print("finding sets")
        image.find_sets()
        print("drawing cards")
        # self.draw_nonset_cards(im.get_cards_nonset())
        self.draw_set_cards(image.get_cards_set())