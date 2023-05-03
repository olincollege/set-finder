"""
Module to read webcam input
"""
from cv2 import cv2
import numpy as np
from v4l2py import Device
import matplotlib.pyplot as plt


class Controller:
    """
    Class for reading webcam input

    Attributes:
        cam: The index of the camera to read from.
    """

    def __init__(self, index=0):
        self.i = index

    def get_image(self):
        """
        Return a OpenCV array specifying an image at that time
        """
        cam = cv2.VideoCapture(
            self.i,
            apiPreference=cv2.CAP_ANY,
            params=[cv2.CAP_PROP_HW_ACCELERATION, cv2.VIDEO_ACCELERATION_ANY],
        )
        _, frame = cam.read()
        cam.release()
        return frame


if __name__ == "__main__":
    # Colors will be not correct because of BGR encoding in OpenCV
    control = Controller(0)
    image = control.get_image()
    plt.figure()
    plt.imshow(image)
    plt.show()
